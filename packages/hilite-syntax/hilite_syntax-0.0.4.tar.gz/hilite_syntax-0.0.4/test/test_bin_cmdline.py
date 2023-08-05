#!/usr/bin/env python

import subprocess
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

class TestBinCmdline(unittest.TestCase):
    """tests cmdline hilite_syntax"""

    def setUp(self):
        self.maxDiff = None

    def cmd_pass(self, cmd):
        cmd = ["hilite_syntax"] + cmd
        scmd = subprocess.run(cmd, check=True, 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return scmd.stdout.decode('utf-8')

    def cmd_fail(self, cmd):
        cmd = ["hilite_syntax"] + cmd
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(cmd, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # now run without checking so we can return output
        scmd = subprocess.run(cmd, check=False,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return scmd.stdout.decode('utf-8')

    def test_help(self):
        """test help strings"""

        self.assertRegex(self.cmd_fail([]), r"usage: highlight_syntax")
        self.assertRegex(self.cmd_fail([]), r"(?!currently supported)")

        self.assertRegex(self.cmd_fail(["-h"]), r"usage: highlight_syntax")
        self.assertRegex(self.cmd_fail(["-h"]), r"currently supported")

        self.assertRegex(self.cmd_fail(["foo"]), 
                r"arguments are required: converter")

        self.assertRegex(self.cmd_fail(["foo", "lark"]), 
                r"invalid command foo")

        self.assertRegex(self.cmd_fail(["foo", "lark"]), 
                r"invalid command foo")

    def test_help(self):
        """test help strings"""
        self.assertRegex(self.cmd_fail(["help"]), r"required: converter")
        self.assertRegex(self.cmd_fail(["help", "lark"]), r"usage: lark")
        self.assertRegex(self.cmd_fail(["help", "vim"]), r"usage: vim")

    def test_dump(self):
        """test dump"""
        self.assertRegex(self.cmd_fail(["dump"]), r"required: converter")
        self.assertRegex(self.cmd_fail(["dump", "vim"]), 
                r"invalid iconverter vim")
        self.assertRegex(self.cmd_fail(["dump", "lark"]), r"usage: lark")

        # dump lark
        tempdir = tempfile.mkdtemp()        
        larkgrammar = f"{tempdir}/simple.lark"
        with open(larkgrammar, "w") as f:
            f.write(dd("""
                start: START_KW_3 start2 END_KW_3
                start2: KW_1 KW_2
                KW_1: "abc"
                KW_2: /abcd/
                START_KW_3: "abc" "def"
                END_KW_3: "abc" "def"
            """))
        self.assertEqual(self.cmd_pass(["dump", "lark", larkgrammar]), 
            dd("""\
                RegexNode('END_KW_3','abcdef',FormatType.Keyword)
                StringNode('KW_1','abc',FormatType.Keyword)
                RegexNode('KW_2','abcd',FormatType.Keyword)
                RegexNode('START_KW_3','abcdef',FormatType.Keyword)
                RootNode('___root___')
                  'start_0'
                GroupNode('start_0','START_KW_3','END_KW_3')
                  'END_KW_3'
                  'KW_1'
                  'KW_2'
                  'START_KW_3'
            """))
        self.assertEqual(self.cmd_pass(
            ["dump", "lark", "--start", "start2", larkgrammar]), 
            dd("""\
                StringNode('KW_1','abc',FormatType.Keyword)
                RegexNode('KW_2','abcd',FormatType.Keyword)
                RootNode('___root___')
                  'KW_1'
                  'KW_2'
            """))

    def test_lark_to_vim(self):
        """test lark to vim conversion"""

        # dump lark
        tempdir = tempfile.mkdtemp()        
        larkgrammar = f"{tempdir}/simple.lark"
        vimdir = f"{tempdir}/vim"
        with open(larkgrammar, "w") as f:
            f.write(dd("""
                start: KW_1 KW_2
                KW_1: "abc"
                KW_2: "def"
            """))

        self.assertRegex(self.cmd_fail(["input", "lark", "not-a-real-file",
                       "output", "vim", "foo", "--outdir", vimdir]),
                       "No such file")

        self.assertRegex(self.cmd_fail(["input", "lark", 
                            "--start", "foo", larkgrammar,
                       "output", "vim", "foo", "--outdir", vimdir]),
                       "undefined rule")

        self.cmd_pass(["input", "lark", larkgrammar,
                       "output", "vim", "foo", "--outdir", vimdir])
        self.assertEqual(os.path.isfile(f"{vimdir}/syntax/foo.vim"), True)
        with open(f"{vimdir}/ftdetect/foo.vim", "r") as f:
            text = f.read()
            self.assertRegex(text, "\*.foo")


        self.cmd_pass(["input", "lark", larkgrammar, "--start", "start",
                       "output", "vim", "bar", "--ext", "k",
                            "--ext", "j", "--outdir", vimdir])
        self.assertEqual(os.path.isfile(f"{vimdir}/syntax/bar.vim"), True)
        with open(f"{vimdir}/ftdetect/bar.vim", "r") as f:
            text = f.read()
            self.assertRegex(text, "\*.k")
            self.assertRegex(text, "\*.j")

if __name__ == "__main__":
    unittest.main()
