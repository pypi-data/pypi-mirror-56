# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""cubicweb-saem_ref unit tests for entities.skos"""

from cubicweb.devtools import PostgresApptestConfiguration
from cubicweb.devtools.testlib import CubicWebTC

import testutils


def setUpModule():
    testutils.startpgcluster(__file__)


class ConceptSchemeTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    def test_optimized_top_concepts(self):
        with self.admin_access.cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', ark_naa=testutils.naa(cnx))
            c1 = scheme.add_concept(u'blah')
            c1label = c1.preferred_label[0]
            c2 = c1.add_concept(u'blob')
            cnx.commit()
        # open a fresh connection to ensure all cnx caches are empty
        with self.admin_access.cnx() as cnx:
            scheme = cnx.entity_from_eid(scheme.eid)
            scheme.top_concepts_rset  # simply access to the property
            cache = cnx.transaction_data['ecache']
            self.assertIn(c1.eid, cache)
            self.assertIn(c1label.eid, cache)
            # trick to test the entity's caches: kill its ._cw attribute and
            # attempt to fetch attributes/relations
            c1 = cache[c1.eid]
            del c1._cw
            self.assertEqual([x.eid for x in c1.reverse_broader_concept],
                             [c2.eid])
            self.assertEqual([x.eid for x in c1.preferred_label],
                             [c1label.eid])
            self.assertEqual(set(c1.cw_attr_cache), set(['ark', 'cwuri', 'definition', 'example']))
            c1label = cache[c1label.eid]
            self.assertEqual(set(c1label.cw_attr_cache), set(['kind', 'label', 'language_code']))


class ConceptSchemeITreeBaseAdapterTC(CubicWebTC):

    configcls = PostgresApptestConfiguration

    def test_iter_children_does_not_list_nested_concepts(self):
        with self.admin_access.cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', ark_naa=testutils.naa(cnx))
            c1 = scheme.add_concept(u'child1')
            c2 = scheme.add_concept(u'child2')
            c3 = c2.add_concept(u'child2child')
            cnx.commit()
            children = scheme.cw_adapt_to('ITreeBase').iterchildren()
            self.assertIn(c1, children)
            self.assertIn(c2, children)
            self.assertNotIn(c3, children)

    def test_is_leaf_when_contains_no_concepts(self):
        with self.admin_access.cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', ark_naa=testutils.naa(cnx))
            cnx.commit()
            self.assertTrue(scheme.cw_adapt_to('ITreeBase').is_leaf())

            scheme.add_concept(u'child')
            cnx.commit()

            scheme.cw_clear_all_caches()
            self.assertFalse(scheme.cw_adapt_to('ITreeBase').is_leaf())

    def test_jqtree_reparent(self):
        with self.admin_access.cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', ark_naa=testutils.naa(cnx))
            cnx.commit()
            a = scheme.add_concept(u'a')
            b = scheme.add_concept(u'b')
            c = scheme.add_concept(u'c', broader_concept=b)
            cnx.commit()
            c_tree = c.cw_adapt_to('IJQTree')
            c_tree.reparent(a.eid, None)
            cnx.commit()
            c.cw_clear_all_caches()
            self.assertEqual(c.broader_concept, (a, ))
            c_tree.reparent(scheme.eid, None)
            cnx.commit()
            c.cw_clear_all_caches()
            self.assertEqual(c.broader_concept, ())


if __name__ == '__main__':
    import unittest
    unittest.main()
