"""Inline InputConverter implementation, mainly for testing"""

from typing import Dict, List, Union, NamedTuple

from dcggraph import DCGgraph

from hilite_syntax import FormatType, InputConverter, OutputConverter, \
                          SyntaxNode, RootNode, StringNode, RegexNode, \
                          GroupNode

#============================================================================

InlineItem = Union["InlineRoot", "InlineString", "InlineRegex", "InlineGroup"]

class InlineRoot(NamedTuple):
    """will be RootNode"""
    children: List[InlineItem]

class InlineString(NamedTuple):
    """will be StringNode"""
    name: str
    string: str

class InlineRegex(NamedTuple):
    """will be RegexNode"""
    name: str
    pattern: str

class InlineGroup(NamedTuple):
    """will be GroupNode"""
    name: str
    children: List[InlineItem]

#============================================================================

class InlineInputConverter(InputConverter):
    """
    The inline-input-converter converts a list of InlineItem into the graph
    """
    def __init__(self, items: List[InlineItem],
                 token_map: Dict[str, FormatType] = None) -> None:
        super().__init__(token_map)
        self._items = items

    def _generate_graph(self) -> DCGgraph:
        """override base-class"""
        # pylint: disable=bad-continuation,cell-var-from-loop
        items = self._items
        graph = DCGgraph()
        edges = {}

        strings = list(filter(lambda i: isinstance(i, InlineString), items))
        regexs = list(filter(lambda i: isinstance(i, InlineRegex), items))
        groups = list(filter(lambda i: isinstance(i, InlineGroup), items))
        roots = list(filter(lambda i: isinstance(i, InlineRoot), items))

        for item in strings:
            graph.add_node(StringNode(item.name, item.string,
                                      self.token_name_to_type(item.name)))
        for item in regexs:
            graph.add_node(RegexNode(item.name, item.pattern,
                                     self.token_name_to_type(item.name)))
        for item in groups:
            node = GroupNode(item.name)
            if len(item.children) > 1:
                node = GroupNode(item.name,
                                 item.children[0], item.children[-1])
            graph.add_node(node)
            edges[node.name] = {}
            for child_name in item.children:
                edges[node.name][child_name] = True

        for item in roots:
            node = RootNode()
            graph.add_node(node)
            edges[node.name] = {}
            for child_name in item.children:
                edges[node.name][child_name] = True

        for fname in edges:
            for tname in edges[fname]:
                graph.create_edge(graph.get_node(fname), graph.get_node(tname))

        return graph

#============================================================================

class InlineOutputConverter(OutputConverter):
    """
    The inline-output-converter converts the graph into a list of InlineItem.
    The output list will be sorted in the order the nodes are visited during
    output generation
    """
    # pylint: disable=too-few-public-methods

    def __init__(self) -> None:
        """initialize the output lines"""
        super().__init__()
        self._items = []

    def _start(self) -> None:
        """override base-class"""
        self._items.clear()

    def _visit(self, node: SyntaxNode) -> None:
        """override base-class"""
        # pylint: disable=bad-continuation
        if isinstance(node, RootNode):
            self._items.append(InlineRoot(
                               list(map(lambda n: n.name, node.children))))
        elif isinstance(node, StringNode):
            self._items.append(InlineString(node.name, node.string))
        elif isinstance(node, RegexNode):
            self._items.append(InlineRegex(node.name, node.pattern))
        elif isinstance(node, GroupNode):
            self._items.append(InlineGroup(node.name,
                list(map(lambda n: n.name, node.children))))
        else:
            raise Exception(f"invalid node {node}")

    def _end(self) -> List[InlineItem]:
        """override base-class"""
        return self._items
