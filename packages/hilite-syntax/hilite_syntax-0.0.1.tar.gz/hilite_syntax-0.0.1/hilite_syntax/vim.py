"""Vim OutputConverter implementation. generates syntax/ftdetect files"""

from datetime import datetime as dt
import os
from textwrap import dedent as dd
from typing import List

from dcggraph import DCGgraph

from hilite_syntax import FormatType, OutputConverter, SyntaxNode, \
                          RootNode, StringNode, RegexNode, GroupNode

#=============================================================================

# map the IR-types into actual hl-groups in vim
# NOTE: is there any benenfit to making this a default, and allowing the
#       user to pass in a format_map?
FORMAT_MAP = {
    FormatType.Normal: "Normal",
    FormatType.Comment: "Comment",
    FormatType.MetaComment: "Todo",
    FormatType.Delimiter: "Delimiter",
    FormatType.Operator: "Operator",
    FormatType.Group: "Delimiter",
    FormatType.Keyword: "Keyword",
    FormatType.Identifier: "Identifier",
    FormatType.Directive: "PreProc",
    FormatType.Annotation: "Underlined",
    FormatType.Constant: "Constant",
    FormatType.String: "String",
    FormatType.Char: "Character",
    FormatType.Bool: "Boolean",
    FormatType.Number: "Number",
}

#=============================================================================

class VimOutputConverter(OutputConverter):
    """
    The vim-output-converter converts the graph into a syntax/, ftdetect/
    and doc/ files within a target directory.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, graph: DCGgraph, language: str,
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
                        defaults to $PWD/vim_hilite_syntax
        """
        super().__init__(graph)
        self._language = language
        self._exts = exts
        if exts is None or (len(exts) == 0):
            self._exts = [f".{language}"]
        self._outdir = outdir
        if self._outdir is None:
            self._outdir = f"{os.getcwd()}/vim_hilite_syntax"
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
            self._lines.append(
                f"syn keyword {vim_name} {node.string}{contained}")
        elif isinstance(node, RegexNode):
            self._lines.append(
                f"syn match {vim_name} /{node.pattern}/{contained}")
        elif isinstance(node, GroupNode):
            # group start match
            start_token = node.start_token
            if isinstance(start_token, RegexNode):
                start = f"start=/{start_token.pattern}/"
            else:
                start = f"start=\"{start_token.string}\""

            # group end match
            end_token = node.end_token
            if isinstance(end_token, RegexNode):
                end = f"end=/{end_token.pattern}/"
            else:
                end = f"end=\"{end_token.string}\""

            # always highlight the start/end tokens appropriately
            match = f" matchgroup={self.language}_{start_token.name}"

            # now, write out the group, and all its children in chunks that
            # span 80 character lines
            line = f"syn region {vim_name}{match} {start} {end}{contained}"
            self._lines.append(line + " contains=")
            NEXTLINE_START = "    \\ "
            nextline = NEXTLINE_START
            first_child = True
            for child in node.children:
                child_vim_name = f"{self.language}_{child.name}"
                if first_child:
                    nextline += f"{child_vim_name}"
                    first_child = False
                else:
                    nextline += f",{child_vim_name}"

                if len(nextline) > 79:
                    self._lines.append(nextline)
                    nextline = NEXTLINE_START
            if nextline != NEXTLINE_START:
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
