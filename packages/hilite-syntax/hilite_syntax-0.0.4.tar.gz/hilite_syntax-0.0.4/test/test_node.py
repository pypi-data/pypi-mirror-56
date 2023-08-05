#!/usr/bin/env python

import unittest

from dcggraph import *
from hilite_syntax.node import *

class TestNode(unittest.TestCase):
    """tests SyntaxNodes in isolation (without converters)"""

    def test_root_node(self):
        g = DCGgraph()
        n0 = RootNode()
        g.add_node(n0)
        n1 = g.create_node("foo")
        n2 = g.create_node("bar")
        e0 = g.create_edge(n0,n1)
        e0 = g.create_edge(n0,n2)
        with self.assertRaisesRegex(Exception, ".* cannot have input edges"):
            e1 = g.create_edge(n1, n0)

        self.assertEqual(n0.ftype, FormatType.NoType)
        # sorted children
        self.assertEqual(n0.children, [n2,n1])

        #clone
        c = n0.clone()
        self.assertEqual(c.name, n0.name)
        self.assertEqual(len(c.children), 0)

    def test_string_node(self):
        g = DCGgraph()
        r0 = RootNode()
        g.add_node(r0)
        n0 = StringNode("foo",          "0", FormatType.Comment)
        n1 = StringNode("START_foo",    "1", FormatType.Comment)
        n2 = StringNode("END_foo",      "2", FormatType.Comment)
        n3 = StringNode("_START_foo",   "3", FormatType.Comment)
        n4 = StringNode("_END_foo",     "4", FormatType.Comment)

        for node in [n0,n1,n2,n3,n4]:
            g.add_node(node)
            g.create_edge(r0,node)

        with self.assertRaisesRegex(Exception, ".* cannot have output edges"):
            e1 = g.create_edge(n0, n1)

        self.assertEqual(n0.is_start, False)
        self.assertEqual(n1.is_start, True)
        self.assertEqual(n2.is_start, False)
        self.assertEqual(n3.is_start, False)
        self.assertEqual(n4.is_start, False)

        self.assertEqual(n0.is_end,   False)
        self.assertEqual(n1.is_end,   False)
        self.assertEqual(n2.is_end,   True)
        self.assertEqual(n3.is_end,   False)
        self.assertEqual(n4.is_end,   False)

        self.assertEqual(n0.name, "foo")
        self.assertEqual(n1.name, "START_foo")
        self.assertEqual(n2.name, "END_foo")
        self.assertEqual(n3.name, "_START_foo")
        self.assertEqual(n4.name, "_END_foo")

        self.assertEqual(n0.base_name, "foo")
        self.assertEqual(n1.base_name, "foo")
        self.assertEqual(n2.base_name, "foo")
        self.assertEqual(n3.base_name, "_START_foo")
        self.assertEqual(n4.base_name, "_END_foo")

        self.assertEqual(n0.string, "0")
        self.assertEqual(n1.string, "1")
        self.assertEqual(n2.string, "2")
        self.assertEqual(n3.string, "3")
        self.assertEqual(n4.string, "4")

        self.assertEqual(n0.ftype, FormatType.Comment)
        self.assertEqual(n1.ftype, FormatType.Comment)
        self.assertEqual(n2.ftype, FormatType.Comment)
        self.assertEqual(n3.ftype, FormatType.Comment)
        self.assertEqual(n4.ftype, FormatType.Comment)

        self.assertEqual(len(n0.edges_in), 1)
        self.assertEqual(len(n1.edges_in), 1)
        self.assertEqual(len(n2.edges_in), 1)
        self.assertEqual(len(n3.edges_in), 1)
        self.assertEqual(len(n4.edges_in), 1)

        #clone
        c = n0.clone()
        self.assertEqual(c.name, "foo")
        self.assertEqual(len(c.edges_in), 0)

    def test_regex_node(self):
        g = DCGgraph()
        r0 = RootNode()
        g.add_node(r0)
        n0 = RegexNode("foo", "0", FormatType.Comment)
        n1 = RegexNode("START_foo", "1", FormatType.Comment)

        for node in [n0,n1]:
            g.add_node(node)
            g.create_edge(r0,node)

        with self.assertRaisesRegex(Exception, ".* cannot have output edges"):
            e1 = g.create_edge(n0, n1)

        self.assertEqual(n0.is_start, False)
        self.assertEqual(n1.is_start, True)

        self.assertEqual(n0.is_end,   False)
        self.assertEqual(n1.is_end,   False)

        self.assertEqual(n0.base_name, "foo")
        self.assertEqual(n1.base_name, "foo")

        self.assertEqual(n0.pattern, "0")
        self.assertEqual(n1.pattern, "1")

        self.assertEqual(n0.ftype, FormatType.Comment)
        self.assertEqual(n1.ftype, FormatType.Comment)

        #clone
        c = n0.clone()
        self.assertEqual(c.name, "foo")
        self.assertEqual(len(c.edges_in), 0)

    def test_group_node(self):
        g = DCGgraph()
        r0 = RootNode()
        g.add_node(r0)
        n0 = GroupNode("foo", FormatType.Number)
        n1 = GroupNode("foo2", FormatType.Number)
        n2 = GroupNode("bar", FormatType.Number)
        g.add_node(n0)
        g.add_node(n1)
        g.add_node(n2)
        g.create_edge(n0,n1)
        g.create_edge(n1,n0)
        g.create_edge(n0,n2)
        g.create_edge(n1,n2)
        
        # sorted children
        self.assertEqual(n0.children, [n2,n1])
        self.assertEqual(n1.children, [n2,n0])

        self.assertEqual(n0.ftype, FormatType.Number)
        self.assertEqual(n1.ftype, FormatType.Number)

    def test_group_node(self):
        g = DCGgraph()

        t0 = StringNode("foo",        "t0", FormatType.NoType)
        t1 = StringNode("START_foo1", "t1", FormatType.NoType)
        t2 = StringNode("START_foo2", "t2", FormatType.Comment)
        t2i= StringNode("ISTART_foo2","t2", FormatType.Comment)
        t3 = StringNode("START_foo3", "t3", FormatType.String)
        t4 = StringNode("END_foo1",   "t4", FormatType.NoType)
        t5 = StringNode("END_foo2",   "t5", FormatType.Comment)
        t6 = StringNode("END_foo3",   "t6", FormatType.Number)

        g0 = GroupNode("notenough",                 t0.name)
        g1 = GroupNode("nostart",                   t0.name, t6.name)
        g2 = GroupNode("noend",                     t3.name, t0.name)
        g3 = GroupNode("token_strings_nomatch",     t2.name, t6.name)
        g3i= GroupNode("token_strings_nomatch_i",   t2i.name,t6.name)
        g4 = GroupNode("token_types_nomatch",       t3.name, t6.name)
        g5 = GroupNode("match_notype_token",        t1.name, t4.name)
        g6 = GroupNode("match_comment_token",       t2.name, t5.name)
        g6i= GroupNode("match_comment_token_i",     t2i.name,t5.name)


        for node in [g0,g1,g2,g3,g4,g5, t0,t1,t2,t2i,t3,t4,t5,t6]:
            g.add_node(node)

        g.create_edge(g0,t0)

        g.create_edge(g1,t0)
        g.create_edge(g1,t6)

        g.create_edge(g2,t3)
        g.create_edge(g2,t0)

        g.create_edge(g3,t2)
        g.create_edge(g3,t6)
        g.create_edge(g3i,t2i)
        g.create_edge(g3i,t6)

        g.create_edge(g4,t3)
        g.create_edge(g4,t6)

        g.create_edge(g5,t1)
        g.create_edge(g5,t4)

        g.create_edge(g6,t2)
        g.create_edge(g6,t5)
        g.create_edge(g6i,t2i)
        g.create_edge(g6i,t5)

        # children are NOT sorted by name!
        self.assertEqual(g0.children, [t0])
        self.assertEqual(g1.children, [t6,t0])
        self.assertEqual(g2.children, [t3,t0])
        self.assertEqual(g3.children, [t6,t2])
        self.assertEqual(g3i.children,[t6,t2i])
        self.assertEqual(g4.children, [t6,t3])
        self.assertEqual(g5.children, [t4,t1])
        self.assertEqual(g6.children, [t5,t2])
        self.assertEqual(g6i.children,[t5,t2i])

        self.assertEqual(g0.is_useless,  True)
        self.assertEqual(g1.is_useless,  True)
        self.assertEqual(g2.is_useless,  True)
        self.assertEqual(g3.is_useless,  True)
        self.assertEqual(g3i.is_useless, True)
        self.assertEqual(g4.is_useless,  True)
        self.assertEqual(g5.is_useless,  False)
        self.assertEqual(g6.is_useless,  False)
        self.assertEqual(g6i.is_useless, False)

        self.assertEqual(g0.ftype, FormatType.NoType)
        self.assertEqual(g1.ftype, FormatType.NoType)
        self.assertEqual(g2.ftype, FormatType.NoType)
        self.assertEqual(g3.ftype, FormatType.NoType)
        self.assertEqual(g3i.ftype,FormatType.NoType)
        self.assertEqual(g4.ftype, FormatType.NoType)
        self.assertEqual(g5.ftype, FormatType.NoType)
        self.assertEqual(g6.ftype, FormatType.NoType)
        self.assertEqual(g6i.ftype,FormatType.Comment)

        # extra start/end tests
        gn0 = GroupNode("no_either")
        self.assertIsNone(gn0.start_token)
        self.assertIsNone(gn0.end_token)
        self.assertEqual(gn0.ftype, FormatType.NoType)

        gn1 = GroupNode("bad_both", "foo", "foo")
        self.assertIsNone(gn1.start_token)
        self.assertIsNone(gn1.end_token)
        self.assertEqual(gn1.ftype, FormatType.NoType)

        #clone
        c = g0.clone()
        self.assertEqual(c.name, "notenough")
        self.assertEqual(len(c.children), 0)

if __name__ == "__main__":
    unittest.main()
