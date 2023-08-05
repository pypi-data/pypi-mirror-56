#!/usr/bin/env python

import os
import re
import tempfile
from textwrap import dedent as dd
import unittest

from hilite_syntax.vim import VimOutputConverter

from hilite_syntax import FormatType

from hilite_syntax.inline import InlineItem, InlineRoot, InlineString, \
                                 InlineRegex, InlineGroup, \
                                 InlineInputConverter

class TestVimOutputConverter(unittest.TestCase):
    """tests vim output converter impelmentations"""

    def setUp(self):
        self.maxDiff = None

    def test_basic(self):
        tempdir = tempfile.mkdtemp()        
        print(f"tempdir= {tempdir}")
        self.assertIsNone(VimOutputConverter(InlineInputConverter([
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
        }).convert(), 
            language="test", 
            outdir=tempdir, 
            exts=["foo", "bar"]).convert())

        syn_file = f"{tempdir}/syntax/test.vim"
        ft_file = f"{tempdir}/ftdetect/test.vim"
        self.assertTrue(os.path.isfile(syn_file))
        self.assertTrue(os.path.isfile(ft_file))

        with open(ft_file, "r") as f:
            self.assertEqual(f.read(), dd("""\
                au BufRead,BufNewFile *.foo set ft=test
                au BufRead,BufNewFile *.bar set ft=test
            """))

        with open(syn_file, "r") as f:
            text = re.sub("Last Generated:.*", "Last Generated:", f.read())
            self.assertEqual(text, dd("""\
            "================================================================
            " AUTO-GENERATED VIM SYNTAX FILE BY hilite_syntax
            " Language:         test
            " Last Generated:
            "================================================================
            if exists("b:current_syntax")
              finish
            endif

            syn match test_K0 /K0/
            hi link test_K0 Comment
            syn keyword test_S1 S1
            hi link test_S1 Number
            syn region test_g7 matchgroup=test_START_K0 start="K0" end=/K0Q/ contains=
                \\ test_END_K0,test_S1,test_START_K0,test_g7,test_g8
            syn region test_g8 matchgroup=test_ISTART_K0 start="K0" end=/K0Q/ contains=
                \\ test_END_K0,test_ISTART_K0,test_S1,test_g7,test_g8
            hi link test_g8 Comment
            syn match test_END_K0 /K0Q/ contained
            hi link test_END_K0 Comment
            syn keyword test_START_K0 K0 contained
            hi link test_START_K0 Comment
            syn keyword test_ISTART_K0 K0 contained
            hi link test_ISTART_K0 Comment
            """))

    def test_wrap_children(self):
        tempdir = tempfile.mkdtemp()        
        print(f"tempdir= {tempdir}")
        self.assertIsNone(VimOutputConverter(InlineInputConverter([
            InlineRoot(["g0"]),
            InlineGroup("g0", [
                "ISTART_K_0",
                "K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG1",
                "K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG2",
                "K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG3",
                "K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG4",
                "K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG5",
                "END_K_0",
            ]),
            InlineString("K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG1", "a"),
            InlineString("K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG2", "b"),
            InlineString("K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG3", "c"),
            InlineString("K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG4", "d"),
            InlineString("K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG5", "e"),
            InlineString("ISTART_K_0", "f"),
            InlineString("END_K_0", "g"),
        ],{
            "^K":FormatType.Comment,
            "^S1":FormatType.Number,
        }).convert(), 
            language="test", 
            outdir=tempdir).convert())

        syn_file = f"{tempdir}/syntax/test.vim"
        self.assertTrue(os.path.isfile(syn_file))

        with open(syn_file, "r") as f:
            text = re.sub("Last Generated:.*", "Last Generated:", f.read())
            self.assertEqual(text, dd("""\
            "================================================================
            " AUTO-GENERATED VIM SYNTAX FILE BY hilite_syntax
            " Language:         test
            " Last Generated:
            "================================================================
            if exists("b:current_syntax")
              finish
            endif

            syn region test_g0 matchgroup=test_ISTART_K_0 start="f" end="g" contains=
                \\ test_END_K_0,test_ISTART_K_0,test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG1
                \\ ,test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG2,test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG3
                \\ ,test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG4,test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG5
            hi link test_g0 Comment
            syn keyword test_END_K_0 g contained
            hi link test_END_K_0 Comment
            syn keyword test_ISTART_K_0 f contained
            hi link test_ISTART_K_0 Comment
            syn keyword test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG1 a contained
            hi link test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG1 Comment
            syn keyword test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG2 b contained
            hi link test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG2 Comment
            syn keyword test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG3 c contained
            hi link test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG3 Comment
            syn keyword test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG4 d contained
            hi link test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG4 Comment
            syn keyword test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG5 e contained
            hi link test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG5 Comment
            """))

if __name__ == "__main__":
    unittest.main()
