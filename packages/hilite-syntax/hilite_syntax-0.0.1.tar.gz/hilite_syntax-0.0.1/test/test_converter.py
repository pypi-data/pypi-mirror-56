#!/usr/bin/env python

import unittest

from hilite_syntax import FormatType, RootNode, StringNode, RegexNode, \
                          GroupNode

from hilite_syntax.inline import InlineItem, InlineRoot, InlineString, \
                                 InlineRegex, InlineGroup, \
                                 InlineInputConverter, InlineOutputConverter

class TestInlineConverter(unittest.TestCase):
    """tests inline converter impelmentations"""

    def test_single_root(self):
        """single root"""
        with self.assertRaisesRegex(Exception, ".* have one RootNode"):
            InlineInputConverter([]).convert()
        with self.assertRaisesRegex(Exception, ".* exists as RootNode"):
            InlineInputConverter([InlineRoot([]),InlineRoot([])]).convert()
        self.assertEqual(InlineOutputConverter(InlineInputConverter([
            InlineRoot([])
        ]).convert()).convert(), [
            InlineRoot([])
        ])

    def test_basic_token_map_filtering(self):
        """filtering behavior based on a node's FormatType""" 

        # trim if not within root
        self.assertEqual(InlineOutputConverter(InlineInputConverter([
            InlineRoot([]),
            InlineString("S0", "foo")
        ],{"^S":FormatType.Comment}).convert()).convert(), [
            InlineRoot([])
        ])

    def test_filter_out_string_due_to_token_map(self):
        # filter it, its NoType
        self.assertEqual(InlineOutputConverter(InlineInputConverter([
            InlineRoot(["S0"]),
            InlineString("S0", "foo")
        ]).convert()).convert(), [
            InlineRoot([])
        ])

        self.assertEqual(InlineOutputConverter(InlineInputConverter([
            InlineRoot(["S0"]),
            InlineString("S0", "foo")
        ],{"^S":FormatType.NoType}).convert()).convert(), [
            InlineRoot([])
        ])

        # keep it this time, its not NoType!!!
        self.assertEqual(InlineOutputConverter(InlineInputConverter([
            InlineRoot(["S0"]),
            InlineString("S0", "foo")
        ],{"^S":FormatType.Comment}).convert()).convert(), [
            InlineRoot(["S0"]),
            InlineString("S0", "foo")
        ])

    def test_filter_out_when_not_under_root(self):
        # even though its not NoType, its not under Root
        self.assertEqual(InlineOutputConverter(InlineInputConverter([
            InlineRoot([]),
            InlineString("S0", "foo"),
        ],{"^S":FormatType.Comment}).convert()).convert(), [
            InlineRoot([]),
        ])

    def test_basic(self):
        self.assertEqual(InlineOutputConverter(InlineInputConverter([
            InlineRoot(["g0", "g1", "g2", "K0"]),
            InlineGroup("g0", ["S0", "S1"]),
            InlineGroup("g1", ["S0"]),
            InlineGroup("g2", ["S0", "S0", "S1", "g7", "g8"]),
            InlineGroup("g3", ["K0", "K1"]),
            InlineGroup("g4", ["START_K0", "S1", "S0", "START_K0"]),
            InlineGroup("g5", ["START_K0", "END_K0"]),
            InlineGroup("g6", ["END_K0", "START_K0"]),
            InlineGroup("g7", ["START_K0", "g2", "S0", "g2", "END_K0"]),
            InlineGroup("g8", ["ISTART_K0", "g2", "S0", "g2", "END_K0"]),
            InlineString("S0", "S0"),
            InlineString("S1", "S1"),
            InlineRegex("K0", "K0"),
            InlineRegex("K1", "K1"),
            InlineString("START_K0", "K0"),
            InlineString("ISTART_K0", "K0"),
            InlineRegex("END_K0", "K0Q"),
        ],{
            "^K":FormatType.Comment,
            "^S1":FormatType.Number,
        }).convert()).convert(), [
            InlineRoot(["K0", "S1", "g7", "g8"]),
            InlineRegex("K0", "K0"),
            InlineString("S1", "S1"),
            InlineGroup("g7", ["END_K0", "S1", "START_K0", "g7", "g8"]),
            InlineGroup("g8", ["END_K0", "ISTART_K0", "S1", "g7", "g8"]),
            InlineRegex("END_K0", "K0Q"),
            InlineString("START_K0", "K0"),
            InlineString("ISTART_K0", "K0"),
        ])

if __name__ == "__main__":
    unittest.main()
