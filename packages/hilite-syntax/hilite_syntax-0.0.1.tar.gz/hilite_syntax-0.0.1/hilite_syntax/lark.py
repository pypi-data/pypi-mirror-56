"""Lark LALR Grammar InputConverter implementation"""

from typing import Dict, List, Tuple

from dcggraph import DCGgraph
from lark import Lark

from hilite_syntax import FormatType, InputConverter, RootNode, TokenNode, \
                          StringNode, RegexNode, GroupNode

#=============================================================================

# the default token map used in lark grammar files
DEFAULT_TOKEN_MAP = {
    "NORM_":    FormatType.Normal,

    "COMMENT_": FormatType.Comment,
    "TODO_":    FormatType.MetaComment,
    "NOTE_":    FormatType.MetaComment,

    "DELIM_":   FormatType.Delimiter,
    "OP_":      FormatType.Operator,
    "GROUP_":   FormatType.Group,
    "KW_":      FormatType.Keyword,
    "ID_":      FormatType.Identifier,

    "PREPROC_": FormatType.Directive,
    "MACRO_":   FormatType.Directive,

    "ANNO_":    FormatType.Annotation,

    "CONST_" :  FormatType.Constant,
    "STRING_":  FormatType.String,
    "CHAR":     FormatType.Char,
    "BOOL_":    FormatType.Bool,
    "NUM_":     FormatType.Number,
}

#=============================================================================

# convenience type for mapping dict[from_node][to_node] = True
EdgesMap = Dict[str, Dict[str, bool]]

class LarkLALRInputConverter(InputConverter):
    """
    The Lark LALR input converter converts a Lark grammar string into
    DCGgraph of SyntaxNodes. If the token_map is not supplied, a
    default token_map is used
    """
    def __init__(self, grammar: str,
                 token_map: Dict[str, FormatType] = None) -> None:
        if token_map is None:
            token_map = DEFAULT_TOKEN_MAP
        super().__init__(token_map)
        self._parser = Lark(grammar, parser="lalr")

    def _generate_graph(self) -> DCGgraph:
        """override base-class"""
        serialized = self._parser.serialize()
        graph = DCGgraph()

        # create and add tokens, groups, edges
        tokens = self._parser_to_tokens(serialized)
        (groups, edges) = LarkLALRInputConverter._parser_to_groups(serialized)
        for node in [*tokens, *groups]:
            graph.add_node(node)

        # filter out any edges to dropped tokens/groups
        for (fname, tnames) in edges.items():
            if graph.has_node(fname):
                fnode = graph.get_node(fname)
                for tname in tnames.keys():
                    if graph.has_node(tname):
                        graph.create_edge(fnode, graph.get_node(tname))

        # finally, add the start nodes as children of RootNode
        root = RootNode()
        graph.add_node(root)
        for rule_name in serialized["options"]["start"]:
            graph.create_edge(root, graph.get_node(rule_name))

        return graph

    def _parser_to_tokens(self, serialized) -> List[TokenNode]:
        """converts tokens into objects. this requires LALR parser!"""
        nodes = []
        for token in serialized["parser"]["lexer_conf"]["tokens"]:
            token_name = token["name"]
            pattern_type = token["pattern"]["__type__"]
            pattern_val = token["pattern"]["value"]

            # if this token doesn't get highlighted, don't both with it
            ftype = self.token_name_to_type(token_name)
            if ftype == FormatType.NoType:
                continue
            if pattern_type == "PatternStr":
                nodes.append(StringNode(token_name, pattern_val, ftype))
            elif pattern_type == "PatternRE":
                nodes.append(RegexNode(token_name, pattern_val, ftype))
            else:
                raise Exception(f"token has bad pattern __type__: {token}")

        return nodes

    @staticmethod
    def _parser_to_groups(serialized) -> Tuple[List[GroupNode], EdgesMap]:
        """
        converts rules/branches into groups. this requires LALR parser! Each
        rule has 1+ branches, so each rule will produce 2 levels of GroupNodes,
        while will always be compressed down to at most 1 level, since the
        rule node can never have start/end token nodes (only branches)
        """
        # pylint: disable=too-many-locals
        groups = {}
        edges = {}
        for rule in serialized["rules"]:
            rule_order = rule["order"]
            rule_name = rule["origin"]["name"]
            branch_name = f"{rule_name}_{rule_order}"
            if rule["alias"] is not None:
                branch_name = rule["alias"]
            branch_exps = rule["expansion"]

            if rule_name not in groups:
                groups[rule_name] = GroupNode(rule_name)
                edges[rule_name] = {}
            edges[rule_name][branch_name] = True

            child_names = list(map(lambda e: e["name"], branch_exps))
            start_name = child_names[0] if len(child_names) > 1 else None
            end_name = child_names[-1] if len(child_names) > 1 else None
            groups[branch_name] = GroupNode(branch_name, start_name, end_name)
            edges[branch_name] = {}
            for child_name in child_names:
                edges[branch_name][child_name] = True

        return (list(groups.values()), edges)
