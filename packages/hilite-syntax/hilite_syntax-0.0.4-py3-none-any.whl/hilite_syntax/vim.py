"""Vim Converter and ConverterFactory implementations"""

from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime as dt
import os
import re
import sys
from textwrap import dedent as dd
from typing import List

from hilite_syntax.node import FormatType, SyntaxNode, RootNode, \
                               StringNode, RegexNode, GroupNode
from hilite_syntax.converter import OutputConverter

#=============================================================================
# defaults
#=============================================================================
FORMAT_MAP = {
    FormatType.Normal:      "Normal",

    FormatType.Comment:     "Comment",
    FormatType.MetaComment: "Todo",

    FormatType.Special:     "Special",
    FormatType.Delimiter:   "Delimiter",
    FormatType.Operator:    "Operator",
    FormatType.Group:       "Delimiter",
    FormatType.Keyword:     "Keyword",
    FormatType.Identifier:  "Identifier",

    FormatType.Directive:   "PreProc",

    FormatType.Annotation:  "Underlined",

    FormatType.Constant:    "Constant",
    FormatType.String:      "String",
    FormatType.Char:        "Character",
    FormatType.Bool:        "Boolean",
    FormatType.Number:      "Number",
}

def DEFAULT_OUTDIR():
    """
    this allows vim to automatically pick up the files from $HOME/.vim.
    Lazy-load it in case we want change $HOME after program start
    """
    # pylint: disable=invalid-name
    return f"{os.environ['HOME']}/.vim"

# the number of characters wide we wrap output text at
WRAP_CHARACTERS = 79
# the line continuations starting tokens
NEXTLINE_START = "    \\ "

#=============================================================================
# OutputConverter utility functions
#=============================================================================

def _convert_string_regex(string: str) -> str:
    r"""
    converts a string token into a string suitable for a very-non-magic
    pattern-match in vim, where only the slashes have special meaning: / or \
    """
    def _escape(match):
        return f"\\{match.group(1)}"
    string = re.sub(r"([/\\])", _escape, string)
    return f"\\V{string}"

def _convert_real_regex(string: str) -> str:
    """
    converts a regex token into a regex suitable for a very-magic
    pattern-match in vim. in very-magic, only 0-9a-zA-Z_ have NO special
    meaning. this works just like python, except we need to forbid
    several negative/zero-width group syntaxes
    """
    if re.search(r"[^\\]\(\?.*\)", string):
        raise Exception(f"do not use '(?...)' extensions in: {string}")
    if re.search(r"\\\d+", string):
        raise Exception(f"do not use '\\digit' back-references in: {string}")

    return f"\\v{string}"

#=============================================================================
# converter implementation
#=============================================================================

class VimOutputConverter(OutputConverter):
    """
    The vim-output-converter converts the graph into a syntax/, ftdetect/
    and doc/ files within a target directory.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, language: str,
                 exts: List[str] = None, outdir: str = None) -> None:
        """
        initialize the vim output.
        :param language: the language that vim will associate to this syntax
        :param exts: the file extensions to associate with the language. by
                     default, *.<language> will be used. do NOT put the
                     '.' in the extension!
        :param outdir: the output directory to write the following:
                            <outdir>/syntax/<language>.vim
                            <outdir>/ftdetect/<language>.vim
                        defaults to $HOME/.vim
        """
        super().__init__()
        self._language = language
        self._exts = exts
        if exts is None or (len(exts) == 0):
            self._exts = [language]
        self._outdir = outdir
        if self._outdir is None:
            self._outdir = DEFAULT_OUTDIR()
        self._outdir = os.path.abspath(self._outdir)

    @property
    def language(self) -> str:
        """the langauge of the syntax file"""
        return self._language

    @property
    def exts(self) -> List[str]:
        """the list of file-extensions for of the language"""
        return self._exts

    @property
    def outdir(self) -> str:
        """the base output directory to write files to"""
        return self._outdir

    def _start(self) -> None:
        """override base-class. Initialize output text"""
        # pylint: disable=attribute-defined-outside-init
        self._lines = [dd(f"""\
            "================================================================
            " AUTO-GENERATED VIM SYNTAX FILE BY hilite_syntax
            " Language:         {self.language}
            " Last Generated:   {dt.isoformat(dt.now())}
            "================================================================
            if exists("b:current_syntax")
              finish
            endif
        """)]

    def _visit(self, node: SyntaxNode) -> None:
        """override base-class"""
        # pylint: disable=too-many-locals,invalid-name,too-many-branches

        vim_name = f"{self.language}_{node.name}"
        root_is_parent = len(list(filter(
            lambda e: isinstance(e.from_node, RootNode),
            node.edges_in))) > 0
        contained = "" if root_is_parent else " contained"

        if isinstance(node, StringNode):
            regex = _convert_string_regex(node.string)
            self._lines.append(f"syn match {vim_name} /{regex}/{contained}")
        elif isinstance(node, RegexNode):
            regex = _convert_real_regex(node.pattern)
            self._lines.append(f"syn match {vim_name} /{regex}/{contained}")
        elif isinstance(node, GroupNode):
            # group start match
            start_token = node.start_token
            if isinstance(start_token, StringNode):
                regex = _convert_string_regex(start_token.string)
                start = f"start=/{regex}/"
            else:
                regex = _convert_real_regex(start_token.pattern)
                start = f"start=/{regex}/"

            # group end match
            end_token = node.end_token
            if isinstance(end_token, StringNode):
                regex = _convert_string_regex(end_token.string)
                end = f"end=/{regex}/"
            else:
                regex = _convert_real_regex(end_token.pattern)
                end = f"end=/{regex}/"

            # always highlight the start/end tokens appropriately
            match = f" matchgroup={self.language}_{start_token.name}"

            # now, write out the group, and all its children in chunks that
            # span 80 character lines
            line = f"syn region {vim_name}{match} {start} {end}{contained}"
            self._lines.append(line)
            nextline = f"{NEXTLINE_START}contains="
            first_child = True
            for child in node.children:
                if (child.name == start_token.name) or \
                        (child.name == end_token.name):
                    # do NOT allow the start/end tokens inside. vim doesn't
                    # handle this properly. see docs below
                    continue
                child_vim_name = f"{self.language}_{child.name}"
                if first_child:
                    nextline += f"{child_vim_name}"
                    first_child = False
                else:
                    nextline += f",{child_vim_name}"

                if len(nextline) > WRAP_CHARACTERS:
                    self._lines.append(nextline)
                    nextline = NEXTLINE_START
            if (nextline != NEXTLINE_START) and not first_child:
                self._lines.append(nextline)

        # finally, for every node, highlight it if it has a coloring
        ftype = node.ftype
        if ftype != FormatType.NoType:
            self._lines.append(f"hi link {vim_name} {FORMAT_MAP[ftype]}")

    def _end(self) -> None:
        """override base-class. initialize the output dirs, and write files"""
        # pylint: disable=invalid-name

        lang = self.language
        vim_ftdetect_file = f"{self.outdir}/ftdetect/{lang}.vim"
        vim_syntax_file = f"{self.outdir}/syntax/{lang}.vim"

        for vim_file in [vim_ftdetect_file, vim_syntax_file]:
            vim_dir = os.path.dirname(vim_file)
            if not os.path.isdir(vim_dir):
                os.makedirs(vim_dir)

        with open(vim_ftdetect_file, "w") as f:
            for ext in self.exts:
                f.write(f"au BufRead,BufNewFile *.{ext} set ft={lang}\n")

        with open(vim_syntax_file, "w") as f:
            f.write("\n".join(self._lines) + "\n")

#============================================================================
# converter_factory implementation
#============================================================================

class ExitCodeArgumentParser(ArgumentParser):
    """exit !0 during arg-parsing. insane this is not the default behavior"""
    def exit(self, status=0, message=None):
        sys.exit(1)

def VimOutputConverterCmdlineFactory(args: List[str]) -> VimOutputConverter:
    """factory for creating VimOutputConverter objects from the cmdline"""
    # pylint: disable=bad-continuation,invalid-name
    parser = ExitCodeArgumentParser(
        prog="vim",
        formatter_class=RawTextHelpFormatter,
        description=dd("""
            generate vim syntax highlighting files. By default, this
            will write to $HOME/.vim so you will be able to immedately
            enjoy your new syntax files after install. This will write
            to the following files:
                <outdir>/syntax/<language>.vim
                <outdir>/ftdetect/<language>.vim

            LIMITATIONS: 
            1) if you use regex tokens, you must NOT use (?...)
               special groupings, or \\num backreferences. These are too
               complicated to map to vim regexes.
            2) self-nested of group-start/end tokens is not highlighted. For
               example, a block comment uses /* and */ for start/end tokens,
               and therefore cannot contain= the /* or */ because if you
               nest /*  /*   */ */, we want it to work as expected:
        """))
    parser.add_argument("language", type=str,
        help="the vim language to associate with the syntax file")
    parser.add_argument("--outdir", type=str,
        help="change the output directory")
    parser.add_argument("--ext", type=str, action="append", dest="exts",
        help="the list of file extension. default is *.<language>")
    parsed = parser.parse_args(args)

    return VimOutputConverter(parsed.language, parsed.exts, parsed.outdir)
