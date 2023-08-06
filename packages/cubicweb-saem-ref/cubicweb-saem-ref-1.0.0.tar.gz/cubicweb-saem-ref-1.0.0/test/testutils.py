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
"""cubicweb-saem_ref common test tools"""

from __future__ import print_function

from os.path import join, dirname, exists
import re
import sys

from doctest import Example

from lxml import etree
from lxml.doctestcompare import LXMLOutputChecker

from logilab.common.decorators import monkeypatch

from cubicweb import NoResultError, devtools
from cubicweb.devtools import testlib

from cubicweb_seda import testutils as seda_testutils
from cubicweb_saem_ref import ark


# make some names them appear in this module namespace to ease test API
assertValidationError = seda_testutils.assertValidationError
assertUnauthorized = seda_testutils.assertUnauthorized
create_data_object = seda_testutils.create_data_object


def create_archive_unit(parent, *args, **kwargs):
    """Create a SEDAArchiveTransfer with an "ark_naa" relation set."""
    if 'ark_naa' not in kwargs:
        cnx = kwargs.get('cnx', getattr(parent, '_cw', None))
        assert cnx is not None
        authority = authority_with_naa(cnx)
        authority.cw_clear_all_caches()
        kwargs['ark_naa'] = authority.ark_naa
    return seda_testutils.create_archive_unit(parent, *args, **kwargs)


def _authority(func):
    """Decorator binding an Organization with an NAA configured in
    kwargs['authority'].
    """
    def wrapper(cnx, *args, **kwargs):
        authority = kwargs.get('authority')
        if authority is None:
            kwargs['authority'] = authority_with_naa(cnx)
        else:
            if isinstance(authority, int):
                authority = cnx.entity_from_eid(authority)
            if not authority.ark_naa:
                with cnx.security_enabled(False, False):
                    authority.cw_set(ark_naa=naa(cnx))
        return func(cnx, *args, **kwargs)
    return wrapper


@_authority
def agent(cnx, name, **kwargs):
    """Return an Agent with specified name."""
    return cnx.create_entity('Agent', name=name, **kwargs)


@_authority
def organization_unit(cnx, name, archival_roles=(), **kwargs):
    """Return an OrganizationUnit with specified name and archival roles."""
    roles_eid = [cnx.find('ArchivalRole', name=role)[0][0] for role in archival_roles]
    return cnx.create_entity('OrganizationUnit', name=name,
                             archival_role=roles_eid, **kwargs)


def authority_record(cnx, name, kind=u'person', **kwargs):
    """Return an AuthorityRecord with specified kind and name."""
    kind_eid = cnx.find('AgentKind', name=kind)[0][0]
    if 'ark_naa' not in kwargs:
        authority = authority_with_naa(cnx)
        authority.cw_clear_all_caches()
        kwargs['ark_naa'] = authority.ark_naa
    record = cnx.create_entity('AuthorityRecord',
                               agent_kind=kind_eid, **kwargs)
    cnx.create_entity('NameEntry', parts=name, form_variant=u'authorized',
                      name_entry_for=record)
    return record


def seda_transfer(cnx, **kwargs):
    """Return a 2.0, 1.0, 0.2 compatible SEDATransfer."""
    transfer = setup_profile(cnx)
    cnx.create_entity('SEDAAccessRule',  # mandatory for seda 1.0
                      seda_access_rule=transfer,
                      seda_seq_access_rule_rule=cnx.create_entity(
                          'SEDASeqAccessRuleRule',
                          reverse_seda_start_date=cnx.create_entity('SEDAStartDate')))
    return transfer


def naa(cnx):
    return cnx.find('ArkNameAssigningAuthority', what=0).one()


def authority_with_naa(cnx, name=u'Default authority', **kwargs):
    try:
        authority = cnx.find('Organization', name=name).one()
        assert not kwargs, 'extra kwargs may not be specified for a pre-existing organization'
    except NoResultError:
        return cnx.create_entity('Organization', name=name, ark_naa=naa(cnx), **kwargs)
    if not authority.ark_naa:
        with cnx.security_enabled(False, False):
            authority.cw_set(ark_naa=naa(cnx))
    return authority


ARK_URI_RGX = re.compile(
    r'^ark:/0/%s.{%d}%s(/.{%d})?$'
    % (ark.ARK_PREFIX,
       ark.ARK_NAME_LENGTH - len(ark.ARK_PREFIX) - len(ark.ARK_CONTROLCHAR),
       ark.ARK_CONTROLCHAR, ark.ARK_QUALIFIER_LENGTH),
)


ARK_RGX = re.compile(
    r'^0/%s.{%d}%s(/.{%d})?$'
    % (ark.ARK_PREFIX,
       ark.ARK_NAME_LENGTH - len(ark.ARK_PREFIX) - len(ark.ARK_CONTROLCHAR),
       ark.ARK_CONTROLCHAR, ark.ARK_QUALIFIER_LENGTH),
)


ARK_NAME_RGX = re.compile(
    r'^%s.{%d}%s$'
    % (ark.ARK_PREFIX,
       ark.ARK_NAME_LENGTH - len(ark.ARK_PREFIX) - len(ark.ARK_CONTROLCHAR),
       ark.ARK_CONTROLCHAR),
)


def match_ark_uri(text):
    return ARK_URI_RGX.match(text)


def match_ark(text):
    return ARK_RGX.match(text)


def match_ark_name(text):
    return ARK_NAME_RGX.match(text)


def setup_scheme(cnx, title, *labels, **kwargs):
    """Return info new concept scheme"""
    scheme = cnx.create_entity('ConceptScheme', title=title, ark_naa=naa(cnx), **kwargs)
    for label in labels:
        scheme.add_concept(label)
    return scheme


def setup_profile(cnx, **kwargs):
    """Return a minimal SEDA profile."""
    kwargs.setdefault('title', u'Test profile')
    return cnx.create_entity('SEDAArchiveTransfer', ark_naa=naa(cnx), **kwargs)


def concept(cnx, label):
    """Return concept entity with the given preferred label (expected to be unique)."""
    return cnx.execute('Concept X WHERE X preferred_label L, L label %(label)s',
                       {'label': label}).one()


# monkey patch scheme_for_rtype to ensure every scheme is created with a naa set
orig_scheme_for_type = seda_testutils.scheme_for_type


@monkeypatch(seda_testutils)
def scheme_for_type(cnx, rtype, etype, *concept_labels):
    return orig_scheme_for_type(cnx, rtype, etype, *concept_labels, ark_naa=naa(cnx))


class XmlTestMixin(object):
    """Mixin class provinding additional assertion methods for checking XML data."""

    def assertXmlEqual(self, actual, expected):
        """Check that both XML strings represent the same XML tree."""
        checker = LXMLOutputChecker()
        if not checker.check_output(expected, actual, 0):
            message = checker.output_difference(Example("", expected), actual, 0)
            self.fail(message)

    def assertXmlValid(self, xml_data, xsd_filename, debug=False):
        """Validate an XML file (.xml) according to an XML schema (.xsd)."""
        with open(xsd_filename) as xsd:
            xmlschema = etree.XMLSchema(etree.parse(xsd))
        # Pretty-print xml_data to get meaningful line information.
        xml_data = etree.tostring(etree.fromstring(xml_data), pretty_print=True)
        xml_data = etree.fromstring(xml_data)
        if debug and not xmlschema.validate(xml_data):
            print(etree.tostring(xml_data, pretty_print=True))
        xmlschema.assertValid(xml_data)


def startpgcluster(pyfile):
    """Let PostgreSQL cluster be started only once per process and stopped at exit.
    """
    if devtools.DEFAULT_PSQL_SOURCES['system']['db-host'] == 'REPLACEME':
        devtools.startpgcluster(pyfile)
        import atexit
        atexit.register(devtools.stoppgcluster, pyfile)


# speed up tests by using a global configuration ###################################################
_CONFIGS = {}


@monkeypatch(testlib.CubicWebTC, methodname='setUpClass')
@classmethod
def setUpClass(cls):
    try:
        config = _CONFIGS[cls.configcls]
    except KeyError:
        # can't use original implementation, else apphome is not correctly
        # detected
        test_module = sys.modules[cls.__module__]
        test_dir = dirname(test_module.__file__)
        config = cls.configcls('data', join(test_dir, 'data'))
        config.mode = 'test'
        assert exists(config._apphome), config._apphome
        _CONFIGS[cls.configcls] = config
    # force call to init_config which may define a particular setup for the fixture
    cls.init_config(config)
    cls.config = config


class _HCache(dict):
    """Original devtools handler cache prevent caching of several configurations, but that's
    what we're trying to achieve.
    """
    def set(self, config, handler):
        self[config] = handler


devtools.HCACHE = _HCache()
