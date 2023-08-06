# coding: utf-8
# copyright 2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

import io

from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.devtools import PostgresApptestConfiguration

import testutils


def setUpModule():
    testutils.startpgcluster(__file__)


class SKOSImportTC(CubicWebTC):
    configcls = PostgresApptestConfiguration

    def test_datafeed_source(self):
        with self.admin_access.repo_cnx() as cnx:
            url = u'file://%s' % self.datapath('skos.rdf')
            cnx.create_entity('CWSource', name=u'mythesaurus', type=u'datafeed', parser=u'rdf.skos',
                              url=url)
            # create some agent and related objects
            agent = testutils.authority_record(cnx, u'bob')
            function = cnx.create_entity('AgentFunction', name=u'sponge', function_agent=agent)
            cnx.commit()
            # create some external uri and link it to place, function and information entities
            cnx.create_entity('ExternalUri',
                              cwuri=u'http://data.culture.fr/thesaurus/resource/ark:/67717/T1-543',
                              uri=u'http://data.culture.fr/thesaurus/resource/ark:/67717/T1-543',
                              reverse_equivalent_concept=function)
            cnx.commit()
            self.function_eid = function.eid
        dfsource = self.repo.sources_by_uri['mythesaurus']
        # test creation upon initial pull
        with self.repo.internal_cnx() as cnx:
            dfsource.pull_data(cnx, force=True, raise_on_error=True)
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.find(
                'ConceptScheme',
                cwuri='http://data.culture.fr/thesaurus/resource/ark:/67717/Matiere'
            ).one()
            self.assertEqual(scheme.ark, u'67717/Matiere')
            self.assertEqual(set(c.ark for c in scheme.top_concepts),
                             set(['67717/T1-503', '67717/T1-543']))
            self.assertEqual(scheme.cw_adapt_to('IWorkflowable').state, 'draft')
            # ensure the external uri has been replaced by the concept and deleted
            concept = cnx.find('Concept', ark='67717/T1-543').one()
            function = cnx.entity_from_eid(function.eid)
            function.cw_clear_all_caches()
            self.assertEqual(function.equivalent_concept[0].eid, concept.eid)
            # XXX also unique extid  pb when skos import will support externaluri

    def test_skos_source_no_ark(self):
        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity('SKOSSource', name=u'mythesaurus', ark_naa=testutils.naa(cnx),
                              url=u'file://%s' % self.datapath('skos_no_ark.rdf'))
            cnx.commit()
        dfsource = self.repo.sources_by_uri['mythesaurus']
        # test creation upon initial pull
        with self.repo.internal_cnx() as cnx:
            dfsource.pull_data(cnx, force=True, raise_on_error=True)
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.find('ConceptScheme').one()
            scheme_ark = scheme.ark
            self.assertTrue(scheme_ark.startswith('0/rf'))
            concepts = list(scheme.top_concepts)
            self.assertEqual(len(concepts), 2)
            concept_arks = [c.ark for c in concepts]
            self.assertTrue(all(ark.startswith(scheme_ark + '/') for ark in concept_arks),
                            concept_arks)


class LCSVImportTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    def test_cwuri_with_ark(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', ark_naa=testutils.naa(cnx))
            cnx.commit()
            cnx.call_service('lcsv.skos.import', scheme_uri=scheme.cwuri,
                             stream=io.open(self.datapath('lcsv_example_shortened.csv'), 'rb'),
                             delimiter='\t', encoding='utf-8', language_code='es')
            concept1 = cnx.find(
                'Concept', definition="Définition de l'organisation politique de l'organisme").one()
            self.assertTrue(testutils.match_ark_uri(concept1.cwuri),
                            concept1.cwuri)


if __name__ == '__main__':
    import unittest
    unittest.main()
