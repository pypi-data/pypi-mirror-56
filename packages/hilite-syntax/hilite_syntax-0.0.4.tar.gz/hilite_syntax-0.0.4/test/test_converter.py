#!/usr/bin/env python

import unittest

from hilite_syntax.node import FormatType, RootNode, StringNode, RegexNode, \
                               GroupNode

from hilite_syntax.inline import InlineItem, InlineRoot, InlineString, \
                                 InlineRegex, InlineGroup
from hilite_syntax.inline import InlineInputConverter as IIC
from hilite_syntax.inline import InlineOutputConverter as IOC

from canonical_test import CANONICAL_INPUT, CANONICAL_INPUT_TOKEN_MAP, \
                           CANONICAL_OUTPUT

class TestInlineConverter(unittest.TestCase):
    """tests inline converter impelmentations"""

    def test_single_root(self):
        """single root"""
        with self.assertRaisesRegex(Exception, ".* have one RootNode"):
            IIC([]).convert()
        with self.assertRaisesRegex(Exception, ".* exists as RootNode"):
            IIC([InlineRoot([]),InlineRoot([])]).convert()
        self.assertEqual(IOC().convert(IIC([
            InlineRoot([])
        ]).convert()), [
            InlineRoot([])
        ])

    def test_basic_token_map_filtering(self):
        """filtering behavior based on a node's FormatType""" 

        # trim if not within root
        self.assertEqual(IOC().convert(IIC([
            InlineRoot([]),
            InlineString("S0", "foo")
        ],{"^S":FormatType.Comment}).convert()), [
            InlineRoot([])
        ])

    def test_filter_out_string_due_to_token_map(self):
        # filter it, its NoType
        self.assertEqual(IOC().convert(IIC([
            InlineRoot(["S0"]),
            InlineString("S0", "foo")
        ]).convert()), [
            InlineRoot([])
        ])

        self.assertEqual(IOC().convert(IIC([
            InlineRoot(["S0"]),
            InlineString("S0", "foo")
        ],{"^S":FormatType.NoType}).convert()), [
            InlineRoot([])
        ])

        # keep it this time, its not NoType!!!
        self.assertEqual(IOC().convert(IIC([
            InlineRoot(["S0"]),
            InlineString("S0", "foo")
        ],{"^S":FormatType.Comment}).convert()), [
            InlineRoot(["S0"]),
            InlineString("S0", "foo")
        ])

    def test_filter_out_when_not_under_root(self):
        # even though its not NoType, its not under Root
        self.assertEqual(IOC().convert(IIC([
            InlineRoot([]),
            InlineString("S0", "foo"),
        ],{"^S":FormatType.Comment}).convert()), [
            InlineRoot([]),
        ])

    def test_canonical(self):
        """this is the canonical basic test all converters should reproduce"""
        self.assertEqual(
            IOC().convert(
                IIC(CANONICAL_INPUT, CANONICAL_INPUT_TOKEN_MAP).convert()),
            CANONICAL_OUTPUT)

if __name__ == "__main__":
    unittest.main()
