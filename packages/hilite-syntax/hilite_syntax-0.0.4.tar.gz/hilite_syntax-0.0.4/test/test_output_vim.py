#!/usr/bin/env python

import os
import re
import tempfile
from textwrap import dedent as dd
import unittest

from hilite_syntax.vim import VimOutputConverter as VOC
from hilite_syntax.vim import VimOutputConverterCmdlineFactory as VOCF

from hilite_syntax import FormatType

from hilite_syntax.inline import InlineItem, InlineRoot, InlineString, \
                                 InlineRegex, InlineGroup 
from hilite_syntax.inline import InlineInputConverter as IIC

from canonical_test import CANONICAL_INPUT, CANONICAL_INPUT_TOKEN_MAP

class TestVimOutputConverter(unittest.TestCase):
    """tests vim output converter impelmentations"""

    def setUp(self):
        self.maxDiff = None

    def test_defaults(self):
        """test defaults"""

        tempdir = tempfile.mkdtemp()        
        print(f"tempdir= {tempdir}")
        os.environ["HOME"] = tempdir
        voc = VOC(language="test")
        self.assertIsNone(voc.convert(IIC([
            InlineRoot(["K0"]),
            InlineRegex("K0", "K0"),
        ],{
            "^K":FormatType.Comment,
            "^S1":FormatType.Number,
        }).convert()))

        self.assertEqual(voc.language, "test")
        self.assertEqual(voc.exts, ["test"])
        self.assertEqual(voc.outdir, f"{tempdir}/.vim")

        syn_file = f"{tempdir}/.vim/syntax/test.vim"
        ft_file = f"{tempdir}/.vim/ftdetect/test.vim"
        self.assertTrue(os.path.isfile(syn_file))
        self.assertTrue(os.path.isfile(ft_file))

    def test_regex_map(self):
        """test mapping python to vim regexes"""

        tempdir = tempfile.mkdtemp()        
        print(f"tempdir= {tempdir}")
        os.environ["HOME"] = tempdir
        self.assertIsNone(VOC(language="test").convert(IIC([
            InlineRoot(["K0", "K1"]),
            InlineString("K0", "^*/a\\b"),
            InlineRegex("K1", "^*/a\\b"),
        ],{
            "^K":FormatType.Comment,
            "^S1":FormatType.Number,
        }).convert()))

        syn_file = f"{tempdir}/.vim/syntax/test.vim"
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

            syn match test_K0 /\V^*\/a\\\\b/
            hi link test_K0 Comment
            syn match test_K1 /\\v^*/a\\b/
            hi link test_K1 Comment
            """))

        with self.assertRaisesRegex(Exception, "do not use '\(\?\.\.\.\)'"):
            VOC(language="test").convert(IIC([
                InlineRoot(["K0", "K1"]),
                InlineString("K0", r"^*/a\b"),
                InlineRegex("K1", r"^*/a\b(?...)"),
            ],{
                "^K":FormatType.Comment,
                "^S1":FormatType.Number,
            }).convert())

        with self.assertRaisesRegex(Exception, r"do not use '\\digit'"):
            VOC(language="test").convert(IIC([
                InlineRoot(["K0", "K1"]),
                InlineString("K0", r"^*/a\b"),
                InlineRegex("K1", r"^*/a\b\4"),
            ],{
                "^K":FormatType.Comment,
                "^S1":FormatType.Number,
            }).convert())

    def test_canonical(self):
        """compare output to canonical test reference output"""
        tempdir = tempfile.mkdtemp()        
        print(f"tempdir= {tempdir}")
        self.assertIsNone(VOC(language="test", 
                              outdir=tempdir, 
                              exts=["foo", "bar"]).convert(
            IIC(CANONICAL_INPUT, CANONICAL_INPUT_TOKEN_MAP).convert()))

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

            syn match test_K0 /\\vK0/
            hi link test_K0 Comment
            syn match test_S1 /\\VS1/
            hi link test_S1 Number
            syn region test_g7 matchgroup=test_START_K0 start=/\\VK0/ end=/\\vK0Q/
                \\ contains=test_S1,test_g7,test_g8
            syn region test_g8 matchgroup=test_ISTART_K0 start=/\\VK0/ end=/\\vK0Q/
                \\ contains=test_S1,test_g7,test_g8
            hi link test_g8 Comment
            syn match test_END_K0 /\\vK0Q/ contained
            hi link test_END_K0 Comment
            syn match test_START_K0 /\\VK0/ contained
            hi link test_START_K0 Comment
            syn match test_ISTART_K0 /\\VK0/ contained
            hi link test_ISTART_K0 Comment
            """))

    def test_wrap_children(self):
        tempdir = tempfile.mkdtemp()        
        print(f"tempdir= {tempdir}")
        self.assertIsNone(VOC(language="test", outdir=tempdir).convert(IIC([
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
        }).convert()))

        syn_file = f"{tempdir}/syntax/test.vim"
        self.assertTrue(os.path.isfile(syn_file))

        with open(syn_file, "r") as f:
            text = re.sub("Last Generated:.*", "Last Generated:", f.read())
            self.assertEqual(text, dd(
"""            "================================================================
            " AUTO-GENERATED VIM SYNTAX FILE BY hilite_syntax
            " Language:         test
            " Last Generated:
            "================================================================
            if exists("b:current_syntax")
              finish
            endif

            syn region test_g0 matchgroup=test_ISTART_K_0 start=/\Vf/ end=/\Vg/
                \ contains=test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG1,test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG2
                \ ,test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG3,test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG4
                \ ,test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG5
            hi link test_g0 Comment
            syn match test_END_K_0 /\Vg/ contained
            hi link test_END_K_0 Comment
            syn match test_ISTART_K_0 /\Vf/ contained
            hi link test_ISTART_K_0 Comment
            syn match test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG1 /\Va/ contained
            hi link test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG1 Comment
            syn match test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG2 /\Vb/ contained
            hi link test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG2 Comment
            syn match test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG3 /\Vc/ contained
            hi link test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG3 Comment
            syn match test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG4 /\Vd/ contained
            hi link test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG4 Comment
            syn match test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG5 /\Ve/ contained
            hi link test_K_LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGG5 Comment
            """))

class TestLarkLALRInputConverterCmdlineFactory(unittest.TestCase):
    """tests larkLALR cmdline factory impelmentation"""
    
    def test_basic(self):
        tempdir = tempfile.mkdtemp()        

        with self.assertRaises(SystemExit):
            VOCF([])
        with self.assertRaises(SystemExit):
            VOCF(["-h"])
        with self.assertRaises(SystemExit):
            VOCF(["k", "--blah"])

        voc1 = VOCF(["k"])
        voc2 = VOCF(["k", "--outdir", tempdir])
        voc3 = VOCF(["k", "--ext", "a", "--ext", "b"])

        self.assertEqual(voc1.language, "k")
        self.assertEqual(voc1.exts, ["k"])
        self.assertEqual(voc1.outdir, f"{os.environ['HOME']}/.vim")

        self.assertEqual(voc2.language, "k")
        self.assertEqual(voc2.exts, ["k"])
        self.assertEqual(voc2.outdir, tempdir)

        self.assertEqual(voc3.language, "k")
        self.assertEqual(voc3.exts, ["a", "b"])
        self.assertEqual(voc3.outdir, f"{os.environ['HOME']}/.vim")

if __name__ == "__main__":
    unittest.main()
