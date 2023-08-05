"""Abstract Input/Output Converters that produce/consume SyntaxNode graphs"""

from abc import ABCMeta, abstractmethod
from collections import deque
import re
from typing import Dict, Any

from dcggraph import DCGgraph
from dcggraph.search import DCGsearch, PredicateResult

from hilite_syntax.node import ISTART_TOKEN_REGEX, START_TOKEN_REGEX, \
                               END_TOKEN_REGEX, FormatType, SyntaxNode, \
                               RootNode, GroupNode

class InputConverter(metaclass=ABCMeta):
    """
    An object that manages the conversion between some input specification
    and a DCGgraph of SyntaxNodes.
    """

    def __init__(self, token_map: Dict[str, FormatType] = None) -> None:
        """
        :param token_map: maps regexes for token names to highlighting groups.
                          for example {
                            "^COMMENT_": FormatType.Comment,
                            "_KW_": FormatType.Keyword
                          }.
                          Note: re.search is used on token names, not re.match!
        """
        self._token_map = token_map if (token_map is not None) else {}

    def __repr__(self):
        return f"InputConverter()"

    def token_name_to_type(self, token_name: str) -> FormatType:
        """
        returns the token type of the string. InputConverter implementations
        should call this on all tokens to determine its FormatType. If nothing
        matches, then FormatType.NoType is returned
        """
        base_name = re.sub(ISTART_TOKEN_REGEX, "",
                           re.sub(START_TOKEN_REGEX, "",
                                  re.sub(END_TOKEN_REGEX, "", token_name)))
        for key, ftype in self._token_map.items():
            if re.match(key, base_name):
                return ftype
        return FormatType.NoType

    @abstractmethod
    def _generate_graph(self) -> DCGgraph:
        """
        this should not be called by the user directly.
        generates a simple, non-compressed DCGgraph containing SyntaxNodes.
        this
        """

    @staticmethod
    def _compress_graph(graph: DCGgraph) -> DCGgraph:
        """
        compress the graph and returns a new graph. the compressed graph
        filteres out nodes that are FormatType.NoType (except for root)
        """
        def _predicate(node, visited, passed, failed) -> PredicateResult:
            # pylint: disable=unused-argument
            if isinstance(node, RootNode):
                return PredicateResult.PASS
            if isinstance(node, GroupNode):
                # keep groups around, even if they have ftype == NoType!
                if node.is_useless:
                    return PredicateResult.FAIL
                return PredicateResult.PASS
            if node.ftype == FormatType.NoType:
                return PredicateResult.FAIL
            return PredicateResult.PASS

        return DCGsearch(graph, _predicate).compress().graph

    def convert(self) -> DCGgraph:
        """
        generates a compressed, optimized DCGgraph of syntax nodes. This
        should be called directly by the user.
        """
        graph = self._generate_graph()
        root_nodes = filter(lambda n: isinstance(n, RootNode), graph.nodes)
        if len(list(root_nodes)) != 1:
            raise Exception("{self} does not have one RootNode")
        return InputConverter._compress_graph(graph)

class OutputConverter(metaclass=ABCMeta):
    """
    An object that manages the conversion between the DCGgraph of
    SyntaxNodes and the output syntax file string.
    """
    # pylint: disable=too-few-public-methods

    def __repr__(self):
        return f"OutputConverter()"

    @abstractmethod
    def _start(self) -> None:
        """called once at the beginning of convert."""

    @abstractmethod
    def _visit(self, node: SyntaxNode) -> None:
        """
        called for each node visited in the syntax-node graph. The
        implementation should handle any formatting for each node

        The visit order is deterministic, and is based on how high they
        are from the root nodes in the syntax tree, then alphabetically
        for OptionNodes and in list-order for GroupNodes.
        """

    @abstractmethod
    def _end(self) -> Any:
        """
        called once at the end of convert. should generate any output
        to return to the user after all nodes are visited
        """

    def convert(self, graph: DCGgraph) -> str:
        """
        this is called by the user. it converts the input graph into
        an output string. it should be idempotent and deterministic
        (minus any timestamp-dependent output).
        """
        self._start()

        nodes = graph.nodes
        visited = {}
        tovisit = deque(filter(lambda n: isinstance(n, RootNode), nodes))
        if len(tovisit) != 1:
            raise Exception(f"{self} graph does not have 1 RootNode")

        while len(tovisit) > 0:
            node = tovisit.popleft()
            if node.name not in visited:
                visited[node.name] = True
                self._visit(node)
                if hasattr(node, "children"):
                    tovisit.extend(node.children)

        return self._end()
