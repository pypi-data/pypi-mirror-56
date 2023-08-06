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
"""cubicweb-saem-ref test for views."""

import io
import json
import os
from datetime import date
from tempfile import NamedTemporaryFile
import unittest

from yams.schema import role_name

from cubicweb.devtools import PostgresApptestConfiguration
from cubicweb.devtools.testlib import CubicWebTC

from cubicweb_skos.rdfio import default_graph

from cubicweb_saem_ref.views.widgets import process_incomplete_date
from cubicweb_saem_ref.views.authorityrecord import SortableListViewMixin

import testutils


def setUpModule():
    testutils.startpgcluster(__file__)


def eid_from_ark(ark):
    name = ark.rsplit('/', 1)[-1]
    num = ''.join(c for c in name if c.isdigit())
    return int(num)


class SetDateTC(unittest.TestCase):

    def test_set_date_month_beginning(self):
        self.assertEqual(date(1997, 6, 5), process_incomplete_date("5/6/1997"))
        self.assertEqual(date(1997, 6, 5), process_incomplete_date("5/6/97"))
        self.assertEqual(date(2012, 6, 5), process_incomplete_date("5/6/12"))
        self.assertEqual(date(1997, 6, 1), process_incomplete_date("6/1997"))
        self.assertEqual(date(1997, 1, 1), process_incomplete_date("1997"))
        # XXX: behavior has changed in dateutil with dayfirst=True
        # https://github.com/dateutil/dateutil/commit/2d42e046d55b9fbbc0a2f41ce83fb8ec5de2d28b
        self.assertIn(process_incomplete_date("1997/6/5"), [date(1997, 6, 5),  # dateutil<=2.5.1
                                                            date(1997, 5, 6),  # dateutil>=2.5.2
                                                            ])

    def test_set_date_month_end(self):
        self.assertEqual(date(1994, 8, 28), process_incomplete_date("28/08/1994", True))
        self.assertEqual(date(1994, 8, 31), process_incomplete_date("08/1994", True))
        self.assertEqual(date(1994, 2, 28), process_incomplete_date("1994/02", True))
        self.assertEqual(date(1994, 12, 31), process_incomplete_date("1994", True))

    def test_set_date_failure(self):
        with self.assertRaises(ValueError) as cm:
            process_incomplete_date("31/02/2012")
        self.assertIn("day is out of range for month", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            process_incomplete_date("20/14/2015")
        self.assertIn("month must be in 1..12", str(cm.exception))

        with self.assertRaises(ValueError) as cm:
            process_incomplete_date("20")


class FuncViewsTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    def test_citation_view(self):
        with self.admin_access.cnx() as cnx:
            bob = testutils.authority_record(cnx, u'bob')
            mandate = cnx.create_entity('Mandate', term=u'u',
                                        mandate_agent=bob)
            citation = cnx.create_entity('Citation',
                                         note=u'plop',
                                         reverse_has_citation=mandate)
            citation_uri = cnx.create_entity('Citation',
                                             note=u'plop',
                                             uri=u'http://pl.op/',
                                             reverse_has_citation=mandate)
            cnx.commit()
            without_link_html = citation.view('citation-link')
            with_link_html = citation_uri.view('citation-link')
            self.assertEqual(
                with_link_html,
                u'<a class="truncate" href="http://pl.op/" title="plop">plop</a>')
            self.assertEqual(without_link_html, u'<i class="truncate">plop</i>')

    def test_eac_import_user_has_no_naa(self):
        regid = 'eac.import'
        with self.admin_access.web_request() as req:
            req._ = lambda x: x + u' \xe9'
            output = self.view(regid, req=req, template=None)
            self.assertIn(b'be in an organization', output)
            self.assertIn(b'to access this functionnality', output)
        with self.admin_access.web_request() as req:
            req._ = lambda x: x + u' \xe9'
            authority = req.cnx.create_entity('Organization', name=u'dummy',
                                              ark=u'123/dummy')
            req.user.cw_set(authority=authority)
            req.cnx.commit()
            output = self.view(regid, req=req, template=None)
            self.assertIn(b'have an NAA configured', output)
            self.assertIn(b'to access this functionnality', output)

    def test_eac_import_ok(self):
        regid = 'eac.import'
        fname = 'FRAD033_EAC_00001_simplified.xml'
        with self.admin_access.web_request() as req:
            req.user.cw_set(authority=testutils.authority_with_naa(req.cnx))
            naa = req.cnx.create_entity('ArkNameAssigningAuthority', who=u'EAC', what=1)
            # simply test the form properly render and is well formed
            self.view(regid, req=req, template=None)
            fields = {'file': (fname, io.open(self.datapath('EAC/' + fname), 'rb')),
                      'naa': str(naa.eid)}
            req.form = self.fake_form(regid, fields)
            # now actually test the import
            req.view(regid)
            # test AuthorityRecord have been created with a ARK from NAA
            # specified in form params
            arecord = req.find('AuthorityRecord', has_text=u'Gironde. Conseil général').one()
            self.assertTrue(arecord.ark.startswith('1/'), arecord.ark)

    def test_highlight_script_execution(self):
        with self.admin_access.client_cnx() as cnx:
            scheme = testutils.setup_scheme(cnx, u'my thesaurus')
            cnx.commit()
            url = scheme.absolute_url()
        html = self.http_publish(url, data={'highlight': 'toto'})[0].decode('utf-8')
        self.assertIn(
            '$(document).ready(function(){$("h1, h2, h3, h4, h5, table tbody td")'
            '.highlight("toto");});}',
            html)

    def test_highlight_on_rql_plain_text_search_same_etype(self):
        with self.admin_access.client_cnx() as cnx:
            # we need two concepts to get a list view
            scheme = testutils.setup_scheme(cnx, u'my thesaurus', u'toto', u'tata toto')
            concept = scheme.reverse_in_scheme[0]
            cnx.commit()
            ark = concept.ark
        url = 'http://testing.fr/cubicweb/view'
        data = {'rql': 'toto', '__fromsearchbox': '1', 'subvid': 'tsearch'}
        html = self.http_publish(url, data=data)[0].decode('utf-8')
        self.assertIn(
            '<a href="http://testing.fr/cubicweb/ark:/{}?highlight=toto" title="">'.format(ark),
            html)

    def test_skos_negociation(self):
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'musique',
                                       ark_naa=testutils.naa(cnx))
            scheme.add_concept(u'pop')
            cnx.commit()
        with self.admin_access.web_request('conceptscheme',
                                           headers={'Accept': 'application/rdf+xml'}) as req:
            result = self.app_handle_request(req)
            with NamedTemporaryFile(delete=False) as fobj:
                try:
                    fobj.write(result)
                    fobj.close()
                    graph = default_graph()
                    graph.load('file://' + fobj.name, rdf_format='xml')
                finally:
                    os.unlink(fobj.name)

    def test_eac_download_filename(self):
        with self.admin_access.web_request() as req:
            cnx = req.cnx
            agent = testutils.authority_record(cnx, u'jim')
            for ark, expected_filename in (
                (u"", "EAC_{0}.xml".format(agent.eid)),
                (u"ZZZ/4242", "EAC_ZZZ-4242.xml".format(agent.eid)),
            ):
                agent.cw_set(ark=ark)
                view = self.vreg['views'].select('eac.export', req, agent.as_rset())
                view.set_request_content_type()
                self.assertEqual(
                    view._cw.headers_out.getRawHeaders('content-disposition'),
                    ['attachment;filename="{0}"'.format(expected_filename)],
                )

    def test_agent_place_as_concept_view(self):
        with self.admin_access.web_request() as req:
            cnx = req.cnx
            agent_place = cnx.create_entity('AgentPlace', name=u"""çàè€É'"><$""")
            content = agent_place.view('saem.agent_place_as_concept')
            self.assertEqual(content,
                             u"<strong><span>çàè€É&#39;&quot;&gt;&lt;$</span></strong>")

    def test_listitem(self):
        with self.admin_access.web_request() as req:
            entity = req.create_entity('CWGroup', name=u'a')
            content = entity.view('saem.listitem', tabid='blah')
            self.assertIn(entity.view('oneline'), content)
            self.assertIn('__redirectparams=tab%3Dblah&amp', content)

    def test_prov_activities(self):
        with self.admin_access.web_request() as req:
            record = testutils.authority_record(req, u'My record')
            req.create_entity('Activity', agent=u'007', generated=record)
            req.cnx.commit()
            table_html = record.view('prov.activity-generated')
            self.assertIn('admin', table_html)
            self.assertIn('007', table_html)

    def test_related_entities_navigation(self):
        with self.admin_access.web_request() as req:
            ou = testutils.organization_unit(req, u'Archival Dptmt', ['archival'])
            testutils.authority_record(req.cnx, u'bob', reverse_use_authorityrecord=ou)
            testutils.authority_record(req.cnx, u'alice', reverse_use_authorityrecord=ou)
            req.cnx.commit()

            vid = 'saem.ou.authorityrecords'
            view = req.vreg['views'].select(vid, req, rset=ou.as_rset())
            html = view.render()
            nav_link = view.page_navigation_url(None, None, {})

            expected_divid = '{}{}'.format(vid.replace('.', '_'), ou.eid)
            self.assertIn('<div id="{}">'.format(expected_divid), html)
            self.assertIn('#' + expected_divid, nav_link)
            params = json.loads('{{ {} }}'.format(nav_link.split('{')[1].split('}')[0]))
            self.assertEqual(params,
                             {'divid': expected_divid,
                              'vid': vid,
                              'rql': u'Any X WHERE X eid {}'.format(ou.eid)})

    def test_email_address(self):
        with self.admin_access.cnx() as cnx:
            address = cnx.create_entity('EmailAddress', address=u'admin@cubicweb.org')
            self.assertEqual(address.dc_title(), u'admin@cubicweb.org')


class SEDAViewsTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    def test_seda_get_related_version(self):
        """Check that we get correct results when asking for `draft`, `published`, `replaced`
        version of a profile."""
        with self.admin_access.web_request() as req:
            profile1 = testutils.setup_profile(req, title=u'Profile 1')
            req.cnx.commit()
            profile1.cw_adapt_to('IWorkflowable').fire_transition('publish')
            req.cnx.commit()
            profile1.cw_clear_all_caches()
            profile2 = testutils.setup_profile(req, title=u'Profile 2', new_version_of=profile1)
            req.cnx.commit()
            profile2.cw_adapt_to('IWorkflowable').fire_transition('publish')
            req.cnx.commit()
            profile2.cw_clear_all_caches()
            profile3 = testutils.setup_profile(req, title=u'Profile 3', new_version_of=profile2)
            req.cnx.commit()
            profile3.cw_adapt_to('IWorkflowable').fire_transition('publish')
            req.cnx.commit()
            profile3.cw_clear_all_caches()
            profile4 = testutils.setup_profile(req, title=u'Profile 4', new_version_of=profile3)
            req.cnx.commit()

            def unwrap_generator(gen):
                try:
                    return next(iter(gen))
                except StopIteration:
                    return None

            # Draft profile
            box4 = self.vreg['ctxcomponents'].select('saem.seda.relatedprofiles', req,
                                                     entity=profile4)
            self.assertEqual(unwrap_generator(box4.predecessor()).eid, profile3.eid)
            self.assertIsNone(unwrap_generator(box4.current_version(state=u'published')))
            self.assertIsNone(unwrap_generator(box4.current_version(state=u'draft')))
            # Published profile
            box3 = self.vreg['ctxcomponents'].select('saem.seda.relatedprofiles', req,
                                                     entity=profile3)
            self.assertEqual(unwrap_generator(box3.predecessor()).eid, profile2.eid)
            self.assertIsNone(unwrap_generator(box3.current_version(state=u'published')))
            self.assertEqual(unwrap_generator(box3.current_version(state=u'draft')).eid,
                             profile4.eid)
            # Deprecated profile
            box2 = self.vreg['ctxcomponents'].select('saem.seda.relatedprofiles', req,
                                                     entity=profile2)
            self.assertIsNone(unwrap_generator(box2.predecessor()))
            self.assertEqual(unwrap_generator(box2.current_version(state=u'published')).eid,
                             profile3.eid)
            self.assertEqual(unwrap_generator(box2.current_version(state=u'draft')).eid,
                             profile4.eid)
            # Older deprecated profile
            box1 = self.vreg['ctxcomponents'].select('saem.seda.relatedprofiles', req,
                                                     entity=profile1)
            self.assertIsNone(unwrap_generator(box1.predecessor()))
            self.assertEqual(unwrap_generator(box1.current_version(state=u'published')).eid,
                             profile3.eid)
            self.assertEqual(unwrap_generator(box1.current_version(state=u'draft')).eid,
                             profile4.eid)


class ArkViewsTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    def _check_entity_from_path(self, cnx, path, etype, parent_ark=None,
                                **kwargs):
        """Make sure an entity with `etype` and `kwargs` attributes values
        exists and matches ARK identifier found in `path`.
        """
        entity = cnx.find(etype, **kwargs).one()
        self.assertTrue(path.startswith('ark:/'), path)
        self.assertEqual(entity.ark, path[len('ark:/'):])
        if parent_ark is not None:
            self.assertTrue(entity.ark.startswith(parent_ark + '/'),
                            entity.ark)

    def test_ark_authority_record_creation(self):
        with self.admin_access.cnx() as cnx:
            org = testutils.authority_with_naa(cnx)
            naa_eid = org.ark_naa[0].eid
            cnx.commit()
        with self.admin_access.web_request() as req:
            akind = req.cnx.find('AgentKind', name=u'person').one()
            record = self.vreg['etypes'].etype_class('AuthorityRecord')(req)
            record.eid = 'A'
            fields = {
                role_name('record_id', 'subject'): u'test',
                role_name('ark', 'subject'): u'',
                role_name('agent_kind', 'subject'): str(akind.eid),
                role_name('ark_naa', 'subject'): str(naa_eid),
            }
            name = self.vreg['etypes'].etype_class('NameEntry')(req)
            name.eid = 'B'
            name_fields = {
                role_name('parts', 'subject'): u'007',
                role_name('name_entry_for', 'subject'): u'A',
            }
            req.form = self.fake_form('edition', entity_field_dicts=[(record, fields),
                                                                     (name, name_fields)])
            path = self.expect_redirect_handle_request(req)[0]
            self._check_entity_from_path(req, path, 'AuthorityRecord',
                                         record_id=u'test')

    def test_ark_agent_creation(self):
        with self.admin_access.web_request() as req:
            org = testutils.authority_with_naa(req)
            agent = self.vreg['etypes'].etype_class('Agent')(req)
            agent.eid = 'A'
            fields = {role_name('name', 'subject'): u'007',
                      role_name('ark', 'subject'): u'',
                      role_name('authority', 'subject'): str(org.eid)}
            req.form = self.fake_form('edition', entity_field_dicts=[(agent, fields)])
            path = self.expect_redirect_handle_request(req)[0]
            self._check_entity_from_path(req, path, 'Agent',
                                         parent_ark=org.ark,
                                         name=u'007')

    def test_ark_scheme_creation(self):
        with self.admin_access.web_request() as req:
            scheme = self.vreg['etypes'].etype_class('ConceptScheme')(req)
            scheme.eid = 'A'
            fields = {role_name('title', 'subject'): u'test',
                      role_name('ark', 'subject'): u'',
                      role_name('ark_naa', 'subject'): str(testutils.naa(req.cnx).eid)}
            req.form = self.fake_form('edition', entity_field_dicts=[(scheme, fields)])
            path = self.expect_redirect_handle_request(req)[0]
            self._check_entity_from_path(req, path, 'ConceptScheme',
                                         title=u'test')

    def test_ark_concept_creation_form(self):
        # test addition of a concept by specifying in_scheme in form
        with self.admin_access.web_request() as req:
            scheme = req.cnx.create_entity('ConceptScheme', ark_naa=testutils.naa(req.cnx))
            concept = self.vreg['etypes'].etype_class('Concept')(req)
            concept.eid = 'A'
            concept_fields = {role_name('in_scheme', 'subject'): str(scheme.eid),
                              role_name('definition', 'subject'): u'thing',
                              role_name('ark', 'subject'): u''}
            label = self.vreg['etypes'].etype_class('Label')(req)
            label.eid = 'B'
            label_fields = {role_name('label', 'subject'): u'Hello',
                            role_name('label_of', 'subject'): 'A'}
            req.form = self.fake_form('edition', entity_field_dicts=[(concept, concept_fields),
                                                                     (label, label_fields)])
            path = self.expect_redirect_handle_request(req)[0]
            self._check_entity_from_path(req, path, 'Concept',
                                         parent_ark=scheme.ark,
                                         definition=u'thing')

    def test_ark_url_rewrite(self):
        with self.admin_access.web_request() as req:
            rewriter = self.vreg['urlrewriting'].select('schemabased', req)
            _pmid, rset = rewriter.rewrite(req, u'/ark:/JoE/Dalton')
            self.assertEqual(rset.printable_rql(), 'Any X WHERE X ark "JoE/Dalton"')


class AssignArkWebServiceTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    def test_not_authenticated(self):
        with self.new_access('anon').web_request(headers={'Accept': 'application/json'},
                                                 method='POST') as req:
            result = self.app_handle_request(req, 'ark')
            self.assertEqual(json.loads(result.decode('utf-8')),
                             [{'error': 'This service requires authentication.'}])

    def test_authenticated_missing_organization(self):
        with self.admin_access.web_request(
                'ark',
                headers={'Accept': 'application/json'}, method='POST') as req:
            result = self.app_handle_request(req)
            self.assertEqual(json.loads(result.decode('utf-8')),
                             [{'error': 'Missing required "organization" query parameter.'}])

    def test_authenticated_organization_method_not_post(self):
        with self.admin_access.cnx() as cnx:
            org_ark = testutils.authority_with_naa(cnx).ark
        params = {'organization': org_ark}
        with self.admin_access.web_request(
                headers={'Accept': 'application/json'}, **params) as req:
            result = self.app_handle_request(req, 'ark')
            self.assertEqual(json.loads(result.decode('utf-8')),
                             [{'error': 'This service is only accessible using POST.'}])

    def test_authenticated_organization_does_not_exist_method_post(self):
        expected_msg = 'No organization matching identifier "{0}".'
        # Organization does not exist.
        bad_params = {'organization': u'0'}
        with self.admin_access.web_request(
                headers={'Accept': 'application/json'},
                method='POST', **bad_params) as req:
            result = self.app_handle_request(req, 'ark')
            self.assertEqual(json.loads(result.decode('utf-8')),
                             [{'error': expected_msg.format(0)}])
        # Specified ark does not match an Organization entity.
        with self.admin_access.cnx() as cnx:
            agent_ark = testutils.agent(cnx, u'bob').ark
        bad_params = {'organization': agent_ark}
        with self.admin_access.web_request(
                headers={'Accept': 'application/json'},
                method='POST', **bad_params) as req:
            result = self.app_handle_request(req, 'ark')
            self.assertEqual(json.loads(result.decode('utf-8')),
                             [{'error': expected_msg.format(agent_ark)}])

    def test_authenticated_organization_has_no_naa_method_post(self):
        with self.admin_access.cnx() as cnx:
            org_ark = cnx.create_entity(
                'Organization', name=u'dummy', ark=u'123/dummy').ark
            cnx.commit()
        bad_params = {'organization': org_ark}
        with self.admin_access.web_request(
                headers={'Accept': 'application/json'},
                method='POST', **bad_params) as req:
            result = self.app_handle_request(req, 'ark')
            expected_msg = 'Organization "{0}" cannot assign ARK identifiers.'
            self.assertEqual(json.loads(result.decode('utf-8')),
                             [{'error': expected_msg.format(org_ark)}])

    def test_ok(self):
        with self.admin_access.cnx() as cnx:
            org_ark = testutils.authority_with_naa(cnx).ark
            cnx.commit()

        def check_ark(response_body):
            json_response = json.loads(result.decode('utf-8'))
            self.assertEqual(len(json_response), 1)
            self.assertEqual(list(json_response[0].keys()), ['ark'])
            ark = json_response[0]['ark']
            self.assertTrue(testutils.ARK_RGX.match(ark), ark)

        params = {'organization': org_ark}
        with self.admin_access.web_request(
                headers={'Accept': 'application/json'},
                method='POST', **params) as req:
            result = self.app_handle_request(req, 'ark')
            check_ark(result)
        params = {'organization': 'ark:/' + org_ark}
        with self.admin_access.web_request(
                headers={'Accept': 'application/json'},
                method='POST', **params) as req:
            result = self.app_handle_request(req, 'ark')
            check_ark(result)


class ListArchivalUnitsServiceTC(CubicWebTC):

    configcls = PostgresApptestConfiguration
    maxDiff = None

    def test_ok(self):
        with self.admin_access.cnx() as cnx:
            org = testutils.authority_with_naa(cnx)
            archival_unit = testutils.organization_unit(
                cnx, u'Archival Dptmt', ['archival'],
                reverse_archival_unit=org,
                authority=org)
            dep_unit = testutils.organization_unit(
                cnx, u'Deposit Dptmt', ['deposit'],
                authority=org)
            deprecated_dep_unit = testutils.organization_unit(
                cnx, u'Deprecated Deposit Dptmt', ['deposit'],
                authority=org)
            testutils.organization_unit(
                cnx, u'Production Dptmt', ['producer'],
                authority=org)
            org2 = testutils.authority_with_naa(cnx, name=u'Another authority',
                                                archival_unit=archival_unit)
            dep2_unit = testutils.organization_unit(
                cnx, u'Org 2 Deposit Dptmt', ['deposit'],
                authority=org2)
            cnx.commit()
            deprecated_dep_unit.cw_adapt_to('IWorkflowable').fire_transition('deprecate')
            cnx.commit()
            # preload attributes accessed in later connection
            org.ark, org2.ark
            archival_unit.ark, dep_unit.ark, deprecated_dep_unit.ark, dep2_unit.ark

        with self.admin_access.web_request(
                headers={'Accept': 'application/json'}) as req:
            result = json.loads(self.app_handle_request(req, 'archival-units').decode('utf-8'))
            expected = [
                {
                    'ark': archival_unit.ark,
                    'name': 'Archival Dptmt',
                    'state': 'published',
                    'url': archival_unit.absolute_url(),
                    'authority': {
                        'ark': org.ark,
                        'name': org.name,
                        'url': org.absolute_url(),
                    },
                    'deposit-units': [
                        {
                            'ark': dep_unit.ark,
                            'name': dep_unit.name,
                            'state': 'published',
                            'url': dep_unit.absolute_url(),
                            'authority': {
                                'ark': org.ark,
                                'name': org.name,
                                'url': org.absolute_url(),
                            },
                        },
                        {
                            'ark': deprecated_dep_unit.ark,
                            'name': deprecated_dep_unit.name,
                            'state': 'deprecated',
                            'url': deprecated_dep_unit.absolute_url(),
                            'authority': {
                                'ark': org.ark,
                                'name': org.name,
                                'url': org.absolute_url(),
                            },
                        },
                        {
                            'ark': dep2_unit.ark,
                            'name': dep2_unit.name,
                            'state': 'published',
                            'url': dep2_unit.absolute_url(),
                            'authority': {
                                'ark': org2.ark,
                                'name': org2.name,
                                'url': org2.absolute_url(),
                            },
                        },
                    ],
                },
            ]
            result[0]['deposit-units'].sort(key=lambda d: list(d))
            expected[0]['deposit-units'].sort(key=lambda d: list(d))
            self.assertEqual(result, expected)


class TimelineViewsTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    def test_timeline_json(self):
        with self.admin_access.cnx() as cnx:
            ar1 = testutils.authority_record(
                cnx, u'1',
                start_date=date(1987, 6, 1), end_date=date(1988, 4, 2))
            ar2 = testutils.authority_record(
                cnx, u'2',
                start_date=date(1989, 1, 1), end_date=date(1990, 4, 3))
            ar3 = testutils.authority_record(
                cnx, u'2',
                start_date=date(1991, 1, 1), end_date=date(1992, 4, 3))
            cnx.create_entity('ChronologicalRelation',
                              description=u'avant avant',
                              chronological_predecessor=ar1,
                              chronological_successor=ar3)
            cnx.create_entity('ChronologicalRelation',
                              description=u'juste avant',
                              chronological_predecessor=ar2,
                              chronological_successor=ar3)
            cnx.commit()
        with self.admin_access.web_request() as req:
            ar3 = req.entity_from_eid(ar3.eid)
            ar2 = req.entity_from_eid(ar2.eid)
            ar1 = req.entity_from_eid(ar1.eid)
            data = json.loads(ar3.view(
                'saem.authorityrecord-timeline-json', w=None).decode('utf-8'))
            predecessors = [x for x in data['timeline']['date']
                            if x['tag'] == u'chronological_predecessor']
            self.assertEqual(len(predecessors), 2)
            self.assertCountEqual([p['headline'] for p in predecessors],
                                  [ar2.view('incontext', w=None),
                                   ar1.view('incontext', w=None)])


class BaseViewsTC(CubicWebTC):
    """Test for non-business views."""
    configcls = PostgresApptestConfiguration

    def expected_notfound_html(self, etype, addlink=False, kwargs=None):
        parts = [
            '<div class="searchMessage">No entity of type &quot;{}&quot; yet.'.format(etype)
        ]
        if addlink:
            path = 'add/' + etype
            if kwargs:
                path = '{}?{}'.format(
                    path, '&'.join(['{}={}'.format(k, v) for k, v in kwargs.items()]))
            parts.append(
                ' <a href="http://testing.fr/cubicweb/{}">Create one?</a>'.format(path)
            )
        parts.append('</div>')
        return ''.join(parts)

    def test_noresult_sedalib(self):
        with self.admin_access.web_request() as req:
            result = self.app_handle_request(req, path='/sedalib').decode('utf-8')
            kwargs = {'unit_type': 'unit_content'}
            self.assertIn(self.expected_notfound_html('SEDAArchiveUnit', True, kwargs), result)
        with self.new_access('anon').web_request() as req:
            result = self.app_handle_request(req, path='/sedalib').decode('utf-8')
            self.assertIn(self.expected_notfound_html('SEDAArchiveUnit'), result)

    def test_no_notfound_when_no_entity(self):
        """Check that we do not get 404 at /<etype> when no entity of <etype>
        exists yet.
        """
        with self.admin_access.web_request() as req:
            # Request /bookmark, usually there's none on a fresh instance.
            result = self.app_handle_request(req, path='/bookmark').decode('utf-8')
            self.assertIn(self.expected_notfound_html('Bookmark', True), result)
        with self.new_access('anon').web_request() as req:
            result = self.app_handle_request(req, path='/bookmark').decode('utf-8')
            self.assertIn(self.expected_notfound_html('Bookmark'), result)

    def test_true_404(self):
        """Check 404 is returned on unknown entity type."""
        with self.admin_access.web_request() as req:
            self.app_handle_request(req, path='/zorglub')
            self.assertEqual(req.status_out, 404)


class SortableListViewMixinTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    class FakeListView(object):

        @staticmethod
        def related_rset(entity):
            return entity.related('mandate_agent', role='object')

    class SortableFakeListView(SortableListViewMixin, FakeListView):
        pass

    def test_related_rset_sorted_by_index(self):
        with self.admin_access.cnx() as cnx:
            arecord = testutils.authority_record(cnx, u'record')

            m1 = cnx.create_entity('Mandate', term=u'1', mandate_agent=arecord)
            m2 = cnx.create_entity('Mandate', term=u'2', mandate_agent=arecord)
            m3 = cnx.create_entity('Mandate', term=u'3', mandate_agent=arecord)
            cnx.commit()
            fake_view = self.SortableFakeListView()
            expected = [m1.eid, m2.eid, m3.eid]
            actual = [e.eid for e in fake_view.related_rset(arecord).entities()]
            self.assertEqual(expected, actual)

            m1.cw_set(index=2)
            m2.cw_set(index=3)
            m3.cw_set(index=1)
            cnx.commit()
            expected = [m3.eid, m1.eid, m2.eid]
            actual = [e.eid for e in fake_view.related_rset(arecord).entities()]
            self.assertEqual(expected, actual)


class SortableAjaxControllerTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    def setup_database(self):
        with self.admin_access.cnx() as cnx:
            arecord = testutils.authority_record(cnx, u'record')

            self.eid0 = cnx.create_entity('Mandate', term=u'1', mandate_agent=arecord).eid
            self.eid1 = cnx.create_entity('Mandate', term=u'2', mandate_agent=arecord).eid
            self.eid2 = cnx.create_entity('Mandate', term=u'3', mandate_agent=arecord).eid
            self.eids = [self.eid0, self.eid1, self.eid2]
            cnx.commit()

    def test_sort_relation_targets_sorts_sortable(self):
        sorted_eids = [str(eid) for eid in (self.eid1, self.eid0, self.eid2)]
        with self.remote_calling('sort_relation_targets', 'mandate_agent', sorted_eids) as (_, req):
            indexes = [req.entity_from_eid(eid).index for eid in self.eids]
            self.assertEqual([1, 0, 2], indexes)
        sorted_eids = [str(eid) for eid in (self.eid2, self.eid0, self.eid1)]
        with self.remote_calling('sort_relation_targets', 'mandate_agent', sorted_eids) as (_, req):
            indexes = [req.entity_from_eid(eid).index for eid in self.eids]
            self.assertEqual([1, 2, 0], indexes)


if __name__ == '__main__':
    unittest.main()
