#!/usr/bin/env python

import os
import tempfile
from textwrap import dedent as dd
import unittest

from hilite_syntax.lark import LarkLALRInputConverter as LIC
from hilite_syntax.lark import LarkLALRInputConverterCmdlineFactory as LICF

from hilite_syntax import FormatType

from hilite_syntax.inline import InlineItem, InlineRoot, InlineString, \
                                 InlineRegex, InlineGroup 
from hilite_syntax.inline import InlineOutputConverter as IOC

class TestLarkLALRInputConverter(unittest.TestCase):
    """tests larkLALR converter impelmentations"""

    def test_default_token_map(self):
        self.assertEqual(IOC().convert(LIC(dd("""
            start: NORM_A | START_TODO_A | END_KW_A | ISTART_ID_A | ANNO_A 
            NORM_A:       "a"
            START_TODO_A: "a"
            END_KW_A:     "a"
            ISTART_ID_A:  "a"
            ANNO_A:       /a/
        """)).convert()), [
            InlineRoot(["ANNO_A", "END_KW_A", "ISTART_ID_A", 
                        "NORM_A", "START_TODO_A"]),
            InlineRegex("ANNO_A", "a"),
            InlineString("END_KW_A", "a"),
            InlineString("ISTART_ID_A", "a"),
            InlineString("NORM_A", "a"),
            InlineString("START_TODO_A", "a"),
        ])

    def test_canonical(self):
        """duplicate the canonical test from test_converter"""
        self.assertEqual(IOC().convert(LIC(dd("""
            start: g0 | g1 | g2 | K0
            g0: S0 S1
            g1: S0
            g2: S0 S0 S1 g7 g8
            g3: K0 K1
            g4: START_K0 S1 S0 END_K0
            g5: START_K0 END_K0
            g6: END_K0 START_K0
            g7: START_K0 g2 S0 g2 END_K0
            g8: ISTART_K0 g2 S0 g2 END_K0
            S0: "S0"
            S1: "S1"
            K0: /K0/
            K1: /K1/
            START_K0: "K0"
            ISTART_K0: "K0"
            END_K0: /K0Q/
        """),{
            "^K":FormatType.Comment,
            "^S1":FormatType.Number,
        }).convert()), [
            InlineRoot(["K0", "S1", "g7_0", "g8_0"]),
            InlineRegex("K0", "K0"),
            InlineString("S1", "S1"),
            InlineGroup("g7_0", ["END_K0", "S1", "START_K0", "g7_0", "g8_0"]),
            InlineGroup("g8_0", ["END_K0", "ISTART_K0", "S1", "g7_0", "g8_0"]),
            InlineString("END_K0", "K0Q"),
            InlineRegex("START_K0", "K0"),
            InlineRegex("ISTART_K0", "K0"),
        ])

    def test_branching(self):
        """test branching with aliases"""
        self.assertEqual(IOC().convert(LIC(dd("""
            start: g0 | g1 | g2 | K0
            g0: S0 S1
            g1: S0
            g2: S0 S0 S1 g7
            g3: K0 K1
            g4: START_K0 S1 S0 END_K0
            g5: START_K0 END_K0
            g6: END_K0 START_K0
            g7:   START_K0 g2 S0 END_K0 -> foo1
                | START_K0 S0 g2 END_K0 -> foo2
            S0: "S0"
            S1: "S1"
            K0: /K0/
            K1: /K1/
            START_K0: "K0"
            END_K0: /K0Q/
        """),{
            "^K":FormatType.Comment,
            "^S1":FormatType.Number,
        }).convert()), [
            InlineRoot(["K0", "S1", "foo1", "foo2"]),
            InlineRegex("K0", "K0"),
            InlineString("S1", "S1"),
            InlineGroup("foo1", ["END_K0", "S1", "START_K0", "foo1", "foo2"]),
            InlineGroup("foo2", ["END_K0", "S1", "START_K0", "foo1", "foo2"]),
            InlineString("END_K0", "K0Q"),
            InlineRegex("START_K0", "K0"),
        ])

class TestLarkLALRInputConverterCmdlineFactory(unittest.TestCase):
    """tests larkLALR cmdline factory impelmentation"""
    
    def test_basic(self):
        tempdir = tempfile.mkdtemp()        
        texts = [
            "start: /foo/",
            "start2: /foo/",
            "start: noexist",
        ]
        paths = [
            f"{tempdir}/ok_grammar.lark",
            f"{tempdir}/bad_start.lark",
            f"{tempdir}/bad_grammar.lark",
        ]

        for (text, path) in zip(texts, paths):
            with open(path, "w") as f:
                f.write(text)

        with self.assertRaises(SystemExit):
            LICF(["-h"])
        with self.assertRaises(SystemExit):
            LICF([paths[0], "--blah"])
        with self.assertRaises(FileNotFoundError):
            LICF(["not-a-real-file"])
        with self.assertRaisesRegex(Exception, "undefined rule"):
            LICF([paths[0], "--start", "start2"])
        with self.assertRaisesRegex(Exception, "undefined rule"):
            LICF([paths[1]])
        with self.assertRaisesRegex(Exception, "used but not defined"):
            LICF([paths[2]])

        lic1 = LICF([paths[0]])
        lic2 = LICF([paths[1], "--start", "start2"])

if __name__ == "__main__":
    unittest.main()
