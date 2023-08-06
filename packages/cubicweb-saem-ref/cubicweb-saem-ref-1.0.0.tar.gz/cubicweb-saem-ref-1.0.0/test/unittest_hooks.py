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
"""cubicweb-saem_ref unit tests for hooks"""

from datetime import datetime, timedelta
from time import mktime
import unittest

import pytz

from cubicweb import ValidationError
from cubicweb.devtools import PostgresApptestConfiguration
from cubicweb.devtools.testlib import CubicWebTC

from cubicweb_saem_ref.hooks import extract_ark

import testutils


def setUpModule():
    testutils.startpgcluster(__file__)


YESTERDAY = datetime.now(tz=pytz.utc) - timedelta(days=1)


class SAEMRefHooksTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    def assertMDNow(self, entity):
        entity.cw_clear_all_caches()
        self.assertAlmostEqual(mktime(entity.modification_date.timetuple()),
                               mktime(datetime.now(tz=pytz.utc).timetuple()), delta=60)

    def resetMD(self, cnx, *entities):
        for entity in entities:
            with cnx.deny_all_hooks_but():
                entity.cw_set(modification_date=YESTERDAY)
        cnx.commit()

    def test_reset_md(self):
        """Ensure `resetMD` method above works."""
        with self.admin_access.repo_cnx() as cnx:
            agent = testutils.authority_record(cnx, u'bob')
            cnx.commit()
            self.resetMD(cnx, agent)
            agent.cw_clear_all_caches()
            self.assertEqual(agent.modification_date, YESTERDAY)

    def test_sync_scheme_md(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'my thesaurus',
                                       ark_naa=testutils.naa(cnx))
            kt_scheme = testutils.scheme_for_type(cnx, 'seda_keyword_type_to', None, u'theme')
            cnx.commit()
            self.resetMD(cnx, scheme)
            c1 = scheme.add_concept(u'concept 1', language_code=u'fr')
            cnx.commit()
            self.assertMDNow(scheme)
            self.resetMD(cnx, scheme)
            lab = cnx.create_entity('Label', label=u'concept 1.1', language_code=u'en',
                                    label_of=c1)
            cnx.commit()
            self.assertMDNow(scheme)
            self.resetMD(cnx, scheme)
            lab.cw_set(label=u'concept 1.1.1')
            cnx.commit()
            self.assertMDNow(scheme)
            self.resetMD(cnx, scheme, c1)
            c2 = c1.add_concept(u'sub concept')
            cnx.commit()
            self.assertMDNow(c1)
            self.assertMDNow(scheme)
            self.resetMD(cnx, scheme, c1, c2)
            c2.add_concept(u'sub-sub concept')
            cnx.commit()
            self.assertMDNow(c2)
            self.assertMDNow(c1)
            self.assertMDNow(scheme)
            self.resetMD(cnx, scheme, c1, c2)
            c2.preferred_label[0].cw_set(label=u'sub concept 2')
            cnx.commit()
            self.assertMDNow(c2)
            self.assertMDNow(c1)
            self.assertMDNow(scheme)

            self.resetMD(cnx, scheme)
            self.resetMD(cnx, kt_scheme)
            cnx.commit()
            scheme.cw_set(code_keyword_type=kt_scheme.reverse_in_scheme[0])
            cnx.commit()
            kt_scheme.cw_clear_all_caches()
            self.assertEqual(kt_scheme.modification_date, YESTERDAY)
            self.assertMDNow(scheme)

    def test_sync_profile_md(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme = testutils.scheme_for_type(cnx, 'seda_rule', 'SEDASeqAccessRuleRule', u'AR038')
            transfer = testutils.setup_profile(cnx)
            unit, unit_alt, unit_alt_seq = testutils.create_archive_unit(transfer)
            cnx.commit()
            transfer.cw_set(modification_date=YESTERDAY)
            cnx.commit()

            # edit composite children
            unit_alt_seq.reverse_seda_title[0].cw_set(title=u'archive name')
            cnx.commit()
            self.assertMDNow(transfer)
            self.resetMD(cnx, transfer)
            self.resetMD(cnx, scheme)
            # edit relation to a composite children
            code = scheme.reverse_in_scheme[0]
            rule_seq = cnx.create_entity('SEDASeqAccessRuleRule',
                                         reverse_seda_start_date=cnx.create_entity('SEDAStartDate'),
                                         seda_rule=code)
            rule = cnx.create_entity('SEDAAccessRule',
                                     seda_access_rule=transfer,
                                     seda_seq_access_rule_rule=rule_seq)
            cnx.commit()
            self.assertMDNow(transfer)
            # should not have touched scheme's date
            self.assertEqual(scheme.modification_date, YESTERDAY)
            self.resetMD(cnx, transfer)
            # edit link from composite children to an entity which is not part of the container
            rule_seq.cw_set(seda_rule=None)
            cnx.commit()
            self.assertMDNow(transfer)
            self.resetMD(cnx, transfer)
            # deletion of a composite children
            rule.cw_delete()
            cnx.commit()
            self.assertMDNow(transfer)
            transfer.cw_adapt_to('IWorkflowable').fire_transition('publish')
            cnx.commit()
            self.resetMD(cnx, transfer)
            # edit link from root to an entity which is not part of the container
            organization_unit = testutils.organization_unit(
                cnx, u'marcel', archival_roles=['deposit'])
            transfer.cw_set(reverse_use_profile=organization_unit)
            cnx.commit()
            self.assertEqual(transfer.modification_date, YESTERDAY)

    def test_externaluri_to_concept(self):
        with self.admin_access.repo_cnx() as cnx:
            # create some authority record and related objects
            agent = testutils.authority_record(cnx, u'bob')
            address = cnx.create_entity('PostalAddress', street=u"1 av. de l'europe",
                                        postalcode=u'31400', city=u'Toulouse')
            place = cnx.create_entity('AgentPlace', place_address=address, place_agent=agent)
            function = cnx.create_entity('AgentFunction', name=u'sponge', function_agent=agent)
            info = cnx.create_entity('LegalStatus', legal_status_agent=agent)
            cnx.commit()
            # create some external uri and link it to place, function and information entities
            exturi = cnx.create_entity('ExternalUri', cwuri=u'http://someuri/someobject',
                                       uri=u'http://someuri/someobject',
                                       reverse_equivalent_concept=[place, function, info])
            cnx.commit()
            # now insert a concept with the external uri as cwuri
            scheme = cnx.create_entity('ConceptScheme', ark_naa=testutils.naa(cnx))
            concept = scheme.add_concept(u'some object', cwuri=u'http://someuri/someobject')
            cnx.commit()
            # ensure the external uri has been replaced by the concept and deleted
            place.cw_clear_all_caches()
            self.assertEqual(place.equivalent_concept[0].eid, concept.eid)
            function.cw_clear_all_caches()
            self.assertEqual(function.equivalent_concept[0].eid, concept.eid)
            info.cw_clear_all_caches()
            self.assertEqual(info.equivalent_concept[0].eid, concept.eid)
            self.assertFalse(cnx.execute('Any X WHERE X eid %(x)s', {'x': exturi.eid}))

    def test_externaluri_to_authorityrecord_subject(self):
        with self.admin_access.repo_cnx() as cnx:
            bob = testutils.authority_record(cnx, u'bob')
            exturi = cnx.create_entity('ExternalUri', cwuri=u'a/b/c', uri=u'a/b/c')
            arelation = cnx.create_entity('AssociationRelation',
                                          association_from=bob,
                                          association_to=exturi)
            cnx.commit()
            alice = testutils.authority_record(cnx, u'alice', cwuri=u'a/b/c')
            cnx.commit()
            arelation.cw_clear_all_caches()
            self.assertEqual(arelation.association_to[0], alice)
            self.assertFalse(cnx.execute('Any X WHERE X eid %(x)s', {'x': exturi.eid}))

    def test_externaluri_to_authorityrecord_object(self):
        with self.admin_access.repo_cnx() as cnx:
            bob = testutils.authority_record(cnx, u'bob')
            exturi = cnx.create_entity('ExternalUri', cwuri=u'a/b/c', uri=u'a/b/c')
            arelation = cnx.create_entity('AssociationRelation',
                                          association_from=exturi,
                                          association_to=bob)
            cnx.commit()
            alice = testutils.authority_record(cnx, u'alice', cwuri=u'a/b/c')
            cnx.commit()
            arelation.cw_clear_all_caches()
            self.assertEqual(arelation.association_from[0], alice)
            self.assertFalse(cnx.execute('Any X WHERE X eid %(x)s', {'x': exturi.eid}))

    def test_user_email(self):
        # EmailAddress belong to the Organisation graph, hence may conflict with hooks when linked
        # to a user. This is a non-regression test checking that no error is raised on attempt to
        # add an email to a user (which is not adaptable to IContained nor IContainer)
        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity('EmailAddress', address=u'admin@cubicweb.org',
                              reverse_use_email=cnx.user.eid)
            cnx.commit()

    def test_sortable_index_is_eid_on_creation(self):
        with self.admin_access.cnx() as cnx:
            arecord = testutils.authority_record(cnx, u'test')
            mandate = cnx.create_entity('Mandate', term=u'casting', mandate_agent=arecord)
            cnx.commit()
            self.assertEqual(mandate.eid, mandate.index)


class ARKGenerationHooksTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    def _check_ark(self, entity, parent_ark=None):
        self.assertTrue(testutils.match_ark(entity.ark), entity.ark)
        if parent_ark is not None:
            self.assertTrue(entity.ark.startswith(parent_ark + '/'),
                            (parent_ark, entity.ark))

    def _check_ark_and_cwuri(self, entity, **kwargs):
        self._check_ark(entity, **kwargs)
        self.assertTrue(testutils.match_ark_uri(entity.cwuri), entity.cwuri)

    def test_external_ark_invalid(self):
        with self.admin_access.cnx() as cnx:
            for ark in [
                u'string/name',  # NAAN is not a number
                u'123',  # Missing Name
            ]:
                with self.subTest(ark=ark):
                    with self.assertRaises(ValidationError) as cm:
                        testutils.authority_record(cnx, u'bob', ark=ark)
                    self.assertIn('malformatted ARK idenfitier', str(cm.exception))

    def test_external_ark_duplicated(self):
        ark = '1/bob/thefirst'
        with self.admin_access.cnx() as cnx:
            cnx.create_entity('Agent', name=u'bob', ark=ark)
            with self.assertRaises(ValidationError) as cm:
                cnx.create_entity('ConceptScheme', ark=ark)
            self.assertIn('already exists', str(cm.exception))

    def test_external_ark_duplicated_generated(self):
        with self.admin_access.cnx() as cnx:
            authority = testutils.authority_with_naa(cnx)
            agent = cnx.create_entity('Agent', name=u'bob', authority=authority)
            with self.assertRaises(ValidationError) as cm:
                cnx.create_entity('ConceptScheme', ark=agent.ark)
            self.assertIn('already exists', str(cm.exception))

    def test_ark_generation_authorityrecord(self):
        with self.admin_access.repo_cnx() as cnx:
            agent = testutils.authority_record(cnx, u'bob')
            cnx.commit()
            self._check_ark_and_cwuri(agent)
            agent = testutils.authority_record(cnx, u'john', ark=u'999/123456')
            cnx.commit()
            self.assertEqual(agent.ark, '999/123456')
            self.assertEqual(agent.cwuri, 'ark:/999/123456')
            agent = testutils.authority_record(cnx, u'alf', cwuri=u'http://someuri/someagent')
            cnx.commit()
            self._check_ark(agent)
            self.assertEqual(agent.cwuri, 'http://someuri/someagent')

    def test_ark_generation_seda_profile(self):
        with self.admin_access.repo_cnx() as cnx:
            profile = testutils.setup_profile(cnx)
            self._check_ark_and_cwuri(profile)

    def test_ark_generation_seda_profile_ark_given(self):
        with self.admin_access.repo_cnx() as cnx:
            profile = testutils.setup_profile(cnx, ark=u'99/124')
            self.assertEqual(profile.ark, '99/124')
            self.assertEqual(profile.cwuri, 'ark:/99/124')

    def test_ark_generation_seda_profile_with_cwuri(self):
        with self.admin_access.repo_cnx() as cnx:
            profile = testutils.setup_profile(
                cnx, cwuri=u'http://example.org/profile/125')
            self._check_ark(profile)
            self.assertEqual(profile.cwuri, 'http://example.org/profile/125')

    def test_ark_generation_seda_archiveunit(self):
        with self.admin_access.repo_cnx() as cnx:
            naa = testutils.naa(cnx)
            unit, _, _ = testutils.create_archive_unit(None, cnx=cnx, ark_naa=naa)
            self._check_ark_and_cwuri(unit)

    def test_ark_generation_seda_archiveunit_in_archivetransfer(self):
        with self.admin_access.repo_cnx() as cnx:
            profile = testutils.setup_profile(cnx)
            unit, _, _ = testutils.create_archive_unit(profile, cnx)
            self._check_ark_and_cwuri(unit)
            self.assertTrue(unit.ark.startswith('0/'), unit.ark)

    def test_ark_generation_concept(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', ark_naa=testutils.naa(cnx))
            concept = scheme.add_concept(u'some object')
            cnx.commit()
            self._check_ark_and_cwuri(scheme)
            self._check_ark_and_cwuri(concept, parent_ark=scheme.ark)
            scheme = cnx.create_entity('ConceptScheme', cwuri=u'http://someuri/somescheme',
                                       ark_naa=testutils.naa(cnx))
            concept = scheme.add_concept(u'some object', cwuri=u'http://someuri/someconcept')
            cnx.commit()
            self._check_ark(scheme)
            self.assertEqual(scheme.cwuri, 'http://someuri/somescheme')
            self._check_ark(concept, scheme.ark)
            self.assertEqual(concept.cwuri, 'http://someuri/someconcept')
            scheme = cnx.create_entity('ConceptScheme', cwuri=u'http://dcf/res/ark:/67717/Matiere',
                                       ark_naa=testutils.naa(cnx))
            concept = scheme.add_concept(u'some object', cwuri=u'http://dcf/res/ark:/67717/1234')
            cnx.commit()
            self.assertEqual(scheme.ark, '67717/Matiere')
            self.assertEqual(scheme.cwuri, 'http://dcf/res/ark:/67717/Matiere')
            self.assertEqual(concept.ark, '67717/1234')
            self.assertEqual(concept.cwuri, 'http://dcf/res/ark:/67717/1234')

    def test_ark_generation_organization_unit(self):
        with self.admin_access.cnx() as cnx:
            authority = testutils.authority_with_naa(cnx)
            orgunit = testutils.organization_unit(
                cnx, u'test', authority=authority)
            cnx.commit()
            self._check_ark(orgunit, authority.ark)


class AuthorityRecordHookTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    def setup_database(self):
        with self.admin_access.cnx() as cnx:
            self.org_eid = testutils.authority_with_naa(cnx).eid
            self.orgunit_eid = testutils.organization_unit(
                cnx, u'test', archival_roles=('archival', ),
                reverse_archival_unit=self.org_eid, authority=self.org_eid).eid
            self.create_user(cnx, u'bob', authority=self.org_eid)
            cnx.commit()

    def test_automatic_use_authorityrecord(self):
        with self.new_access(u'bob').cnx() as cnx:
            arecord = testutils.authority_record(cnx, u'test')
            cnx.commit()
            self.assertEqual(
                [ou.eid for ou in arecord.reverse_use_authorityrecord],
                [self.orgunit_eid])

    def test_automatic_use_authorityrecord_no_archival_unit(self):
        with self.admin_access.cnx() as cnx:
            self.create_user(cnx, u'alice')
            cnx.commit()
        with self.new_access(u'alice').cnx() as cnx:
            arecord = testutils.authority_record(cnx, u'test')
            cnx.commit()
            arecord.cw_clear_all_caches()
            self.assertFalse(arecord.reverse_use_authorityrecord)


class ExtractArkTC(unittest.TestCase):

    configcls = PostgresApptestConfiguration

    def test_ok(self):
        self.assertEqual(extract_ark('http://dcf/res/ark:/67717/1234'), '67717/1234')
        self.assertEqual(extract_ark('http://dcf/res/ark:/67717/1234#something'), '67717/1234')
        self.assertEqual(extract_ark('http://dcf/res/ark:/67717/1234?value'), '67717/1234')
        self.assertEqual(extract_ark('http://dcf/res/ark:/67717/1234/sub'), '67717/1234')
        self.assertEqual(extract_ark('ark:/67717/1234'), '67717/1234')

    def test_ko(self):
        self.assertEqual(extract_ark('http://dcf/res/ark:/67717'), None)
        self.assertEqual(extract_ark('http://someuri/67717/1234'), None)


class EntityLifeCycleTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    def setup_database(self):
        with self.admin_access.repo_cnx() as cnx:
            bob = self.create_user(cnx, u'bob',
                                   authority=testutils.authority_with_naa(cnx))
            cnx.commit()
            self.bob_eid = bob.eid

    def _check_create(self, cnx, eid, msg):
        activity = cnx.find('Activity', type=u'create', used=eid).one()
        self.assertEqual(activity.associated_with[0].eid, cnx.user.eid)
        self.assertEqual(activity.generated[0].eid, eid)
        self.assertEqual(activity.description, msg)

    def _check_modification(self, cnx, eid, msg):
        activity = cnx.find('Activity', type=u'modify', used=eid).one()
        self.assertEqual(activity.associated_with[0].eid, self.bob_eid)
        self.assertEqual(activity.used[0].eid, eid)
        self.assertEqual(activity.generated[0].eid, eid)
        self.assertEqual(activity.description, msg)

    def test_authorityrecord_create_update(self):
        with self.new_access(u'bob').repo_cnx() as cnx:
            authorityrecord = testutils.authority_record(cnx, u'Smith')
            cnx.commit()
            self._check_create(cnx, authorityrecord.eid,
                               'created authorityrecord')
            authorityrecord.cw_set(isni=u'123', record_id=u'Adam')
            cnx.commit()
            self._check_modification(cnx, authorityrecord.eid,
                                     'modified isni, record_id')

    def test_authorityrecord_add_component(self):
        with self.new_access(u'bob').repo_cnx() as cnx:
            authorityrecord = testutils.authority_record(cnx, u'Smith')
            cnx.commit()
            cnx.create_entity('AgentFunction', name=u'secret agent',
                              function_agent=authorityrecord)
            cnx.commit()
            self._check_modification(cnx, authorityrecord.eid,
                                     'added function_agent_object')

    def test_authorityrecord_delete_component(self):
        with self.new_access(u'bob').repo_cnx() as cnx:
            authorityrecord = testutils.authority_record(cnx, u'Smith')
            af = cnx.create_entity('AgentFunction', name=u'secret',
                                   function_agent=authorityrecord)
            cnx.commit()
            af.cw_delete()
            cnx.commit()
            self._check_modification(cnx, authorityrecord.eid,
                                     'removed function_agent_object')

    def test_authorityrecord_update_component(self):
        with self.new_access(u'bob').repo_cnx() as cnx:
            authorityrecord = testutils.authority_record(cnx, u'Smith')
            pn = cnx.create_entity('AgentFunction', name=u'secret agent',
                                   function_agent=authorityrecord)
            cnx.commit()
            pn.cw_set(name=u'boss of secret agents')
            cnx.commit()
            self._check_modification(cnx, authorityrecord.eid,
                                     'modified function_agent_object')

    def test_authorityrecord_add_subcomponent(self):
        with self.new_access(u'bob').repo_cnx() as cnx:
            authorityrecord = testutils.authority_record(cnx, u'Smith')
            cnx.commit()
            address = cnx.create_entity('PostalAddress', street=u"1 av. de l'europe",
                                        postalcode=u'31400', city=u'Toulouse')
            cnx.create_entity('AgentPlace', place_address=address,
                              place_agent=authorityrecord)
            cnx.commit()
            self._check_modification(cnx, authorityrecord.eid,
                                     'added place_address, place_agent_object')

    def test_authorityrecord_delete_subcomponent(self):
        with self.new_access(u'bob').repo_cnx() as cnx:
            authorityrecord = testutils.authority_record(cnx, u'Smith')
            address = cnx.create_entity('PostalAddress', street=u"1 av. de l'europe",
                                        postalcode=u'31400', city=u'Toulouse')
            cnx.create_entity('AgentPlace', place_address=address,
                              place_agent=authorityrecord)
            cnx.commit()
            address.cw_delete()
            cnx.commit()
            self._check_modification(cnx, authorityrecord.eid, 'removed place_address')

    def test_authorityrecord_update_subcomponent(self):
        with self.new_access(u'bob').repo_cnx() as cnx:
            authorityrecord = testutils.authority_record(cnx, u'Smith')
            address = cnx.create_entity('PostalAddress', street=u"1 av. de l'europe",
                                        postalcode=u'31400', city=u'Toulouse')
            cnx.create_entity('AgentPlace', place_address=address,
                              place_agent=authorityrecord)
            cnx.commit()
            address.cw_set(street=u"1 avenue de l'Europe")
            cnx.commit()
            self._check_modification(cnx, authorityrecord.eid,
                                     'modified place_address')

    def test_authorityrecord_multi_modification(self):
        with self.new_access(u'bob').repo_cnx() as cnx:
            authorityrecord = testutils.authority_record(cnx, u'Smith')
            f1 = cnx.create_entity('AgentFunction', name=u'special agent',
                                   function_agent=authorityrecord)
            gc = cnx.create_entity('GeneralContext', content=u'sunglasses',
                                   general_context_of=authorityrecord)
            cnx.commit()
            gc.cw_set(content=u'stetson')
            address = cnx.create_entity('PostalAddress', street=u"1 av. de l'europe",
                                        postalcode=u'31400', city=u'Toulouse')
            cnx.create_entity('AgentPlace', place_address=address,
                              place_agent=authorityrecord)
            f1.cw_delete()
            cnx.create_entity('AgentFunction', name=u'mib',
                              function_agent=authorityrecord)
            authorityrecord.cw_set(isni=u'123', record_id=u'Adam')
            cnx.commit()
            self._check_modification(
                cnx, authorityrecord.eid,
                '* modified function_agent_object, general_context_of_object, isni, record_id\n'
                '* added place_address, place_agent_object')

    def test_authorityrecord2authorityrecord_relation(self):
        with self.new_access(u'bob').repo_cnx() as cnx:
            k = testutils.authority_record(cnx, u'authorityrecord K')
            d = testutils.authority_record(cnx, u'authorityrecord D')
            cnx.commit()
            cnx.create_entity('AssociationRelation', association_from=k, association_to=d)
            cnx.commit()
            self._check_modification(cnx, k.eid, 'added association_from_object')
            self._check_modification(cnx, d.eid, 'added association_to_object')

    def test_no_activity_generated(self):
        with self.admin_access.repo_cnx() as cnx:
            agent = testutils.agent(cnx, u'smith', authority=cnx.find('Organization')[0][0])
            cnx.commit()
            authorityrecord = testutils.authority_record(
                cnx, u'Smith', reverse_authority_record=agent)
            cnx.commit()
            agent.cw_set(name=u'jones')
            cnx.commit()
            self.assertFalse(cnx.find('Activity', type=u'modify',
                                      used=authorityrecord.eid))

    def test_concept(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'my thesaurus',
                                       ark_naa=testutils.naa(cnx))
            cnx.commit()
            # concept scheme creation
            self._check_create(cnx, scheme.eid, 'created conceptscheme')

        with self.new_access(u'bob').repo_cnx() as cnx:
            scheme = cnx.entity_from_eid(scheme.eid)

            concept = scheme.add_concept(u'hello')
            cnx.commit()
            # concept scheme add concept
            self._check_modification(cnx, scheme.eid, 'added in_scheme_object')
            # concept creation
            self._check_create(cnx, concept.eid, 'created concept')
            subconcept = concept.add_concept(u'goodbye')
            cnx.commit()
            # concept add concept
            self._check_modification(cnx, concept.eid, 'added broader_concept_object')
            # subconcept creation
            self._check_create(cnx, subconcept.eid, 'created concept')
            # subconcept creation scheme
            rset = cnx.execute('Activity X ORDERBY X DESC WHERE X type "modify", X used %(x)s',
                               {'x': scheme.eid})
            self.assertEqual(len(rset), 2)
            self.assertEqual(rset.get_entity(0, 0).description, 'added in_scheme_object')

    def test_archive_transfer_create_update(self):
        with self.new_access(u'bob').cnx() as cnx:
            transfer = testutils.setup_profile(cnx)
            cnx.commit()
            self._check_create(cnx, transfer.eid, 'created sedaarchivetransfer')
            transfer.cw_set(title=u'123')
            cnx.commit()
            self._check_modification(cnx, transfer.eid,
                                     'modified title')

    def test_nonregr_concept_container(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'my thesaurus',
                                       ark_naa=testutils.naa(cnx))
            concept = scheme.add_concept(u'hello')
            cnx.commit()
            concept.cw_delete()
            cnx.commit()

    def test_inter_containers(self):
        with self.admin_access.repo_cnx() as cnx:
            scheme = testutils.scheme_for_type(
                cnx, 'seda_rule', 'SEDASeqAccessRuleRule', u'AR038')
            code = scheme.reverse_in_scheme[0]
            transfer = testutils.setup_profile(cnx)
            unit, unit_alt, unit_alt_seq = testutils.create_archive_unit(transfer)
            cnx.commit()

            nb_scheme_activities = len(cnx.find('Activity', used=scheme.eid))
            nb_concept_activities = len(cnx.find('Activity', used=code.eid))
            nb_transfer_activities = len(cnx.find('Activity', used=transfer.eid))

            rule_seq = cnx.create_entity(
                'SEDASeqAccessRuleRule',
                reverse_seda_start_date=cnx.create_entity('SEDAStartDate'),
                seda_rule=code)
            cnx.create_entity(
                'SEDAAccessRule',
                seda_access_rule=transfer,
                seda_seq_access_rule_rule=rule_seq)
            cnx.commit()

            self.assertEqual(len(cnx.find('Activity', used=code.eid)),
                             nb_concept_activities)
            self.assertEqual(len(cnx.find('Activity', used=transfer.eid)),
                             nb_transfer_activities + 1)

            cnx.create_entity('SEDAMimeTypeCodeListVersion',
                              seda_mime_type_code_list_version_from=transfer,
                              seda_mime_type_code_list_version_to=scheme)
            cnx.commit()

            self.assertEqual(len(cnx.find('Activity', used=scheme.eid)),
                             nb_scheme_activities)
            self.assertEqual(len(cnx.find('Activity', used=transfer.eid)),
                             nb_transfer_activities + 2)


class SEDAArchiveTransferHooksTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    def test_profile_deprecated_by_published_successor(self):
        """Test hook deprecating a SEDA Profile upon successor publication."""
        with self.admin_access.repo_cnx() as cnx:
            profile = testutils.setup_profile(cnx)
            cnx.commit()
            workflow = profile.cw_adapt_to('IWorkflowable')
            workflow.fire_transition('publish')
            cnx.commit()
            profile.cw_clear_all_caches()
            self.assertEqual(workflow.state, 'published')
            cloned = cnx.create_entity('SEDAArchiveTransfer', title=u'Clone',
                                       new_version_of=profile,
                                       ark_naa=testutils.naa(cnx))
            cnx.commit()
            cloned.cw_adapt_to('IWorkflowable').fire_transition('publish')
            cnx.commit()
            profile.cw_clear_all_caches()
            self.assertEqual(workflow.state, 'deprecated')

    def test_profile_deprecated_unlinked_from_organization_unit(self):
        with self.admin_access.cnx() as cnx:
            profile = testutils.setup_profile(cnx)
            organization_unit = testutils.organization_unit(
                cnx, u'org', archival_roles=[u'deposit'])
            cnx.commit()
            workflow = profile.cw_adapt_to('IWorkflowable')
            workflow.fire_transition('publish')
            cnx.commit()
            organization_unit.cw_set(use_profile=profile)
            cnx.commit()
            workflow.fire_transition('deprecate')
            cnx.commit()
            self.assertFalse(organization_unit.use_profile)


class ConceptSchemeWorkflowPermissionsTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    def test_cannot_deprecate_used_vocabulary(self):
        with self.admin_access.cnx() as cnx:
            scheme = testutils.scheme_for_type(cnx, u'seda_keyword_type_to', None,
                                               u'type1')
            cnx.commit()
            scheme.cw_adapt_to('IWorkflowable').fire_transition('publish')
            cnx.commit()
            assert scheme.scheme_relation_type
            with self.assertRaises(ValidationError) as cm:
                scheme.cw_adapt_to('IWorkflowable').fire_transition('deprecate')
            cnx.rollback()
            self.assertIn(
                'this concept scheme is used in at least one SEDA constraint',
                str(cm.exception))


if __name__ == '__main__':
    unittest.main()
