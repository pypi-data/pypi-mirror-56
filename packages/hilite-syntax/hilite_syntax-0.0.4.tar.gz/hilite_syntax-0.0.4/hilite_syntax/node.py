"""Syntax Highlighting Tree node classes"""

from abc import ABCMeta, abstractmethod
from enum import Enum
import re
from typing import List, Optional

from dcggraph import DCGnode, DCGedge

#============================================================================
# constants
#============================================================================

# the name of the root node. no token/rule/branch can have this name
ROOT_NAME = "___root___"

# if a token name matches these, it is assumed to be a group start/end token
# INHERIT_START is used to color an entire group the same color as the
# start/end tokens. START is just used to highlight the start/end tokens, but
# recognize a syntactically valid group
ISTART_TOKEN_REGEX = "^ISTART_"
START_TOKEN_REGEX = "^START_"
END_TOKEN_REGEX = "^END_"

class FormatType(Enum):
    """
    short list of token types. it is up to the InputConverter to map
    tokens to the correct type from the input specification, and it is up
    to the OutputConverter to highlight appropriately based on the token type

    NOTE: if you add/remove things here, make sure you check all the
    input/output converter implementations for their mappings to/from
    FormatTypes!!!
    """
    # NoType nodes will get filtered out during compression
    NoType = 0

    # non-highlighted, but syntactically important tokens
    Normal = 1

    # meta-comments are things in comments that get alt coloring
    Comment = 10
    MetaComment = 11

    # special symbols (non-alphanumeric typically) used only for syntax
    Special = 20
    Delimiter = 21
    Operator = 22
    Group = 23

    # keywords and identifier tokens are typically mutually-exclusive...
    Keyword = 30
    Identifier = 31

    # meta languages (like `include, @decorator, ...)
    Directive = 40
    Annotation = 41

    # literal datatypes
    Constant = 50
    String = 51
    Char = 52
    Bool = 53
    Number = 54

#============================================================================
# SyntaxNodes
#============================================================================

class SyntaxNode(DCGnode, metaclass=ABCMeta):
    """
    A syntax node is a DCGnode that has extra attributes relevant to our
    application: syntax highlighting for editors based on some input
    specification.
    """

    def __repr__(self):
        return f"SyntaxNode('{self.name}')"

    @abstractmethod
    def clone(self) -> "SyntaxNode":
        """
        override base-class. during graph-compression, the node gets clone()ed
        so we need to override the DCGnode clone method to make sure the
        compressed graph contains SyntaxNodes and not just DDCGnodes
        """

    @property
    def ftype(self) -> FormatType:
        """the FormatType of this token. By default, is NoType"""
        return FormatType.NoType

class RootNode(SyntaxNode):
    """
    The root is a fictional node representing the root of the syntax tree.
    It provides a convenient way of locating the root rules/tokens of the
    design.
    """
    def __init__(self) -> None:
        super().__init__(ROOT_NAME)

    def __eq__(self, other):
        return isinstance(other, RootNode) and super().__eq__(other)

    def __repr__(self):
        return f"RootNode('{self.name}')"

    def clone(self) -> "RootNode":
        """override base-class"""
        return RootNode()

    def add_edge_in(self, edge: DCGedge) -> None:
        """overrides baseclass. disallow root from having input edges"""
        raise Exception(f"{self} cannot have input edges")

    @property
    def children(self) -> List[SyntaxNode]:
        """retuns the SORTED list of child nodes of the root node"""
        return sorted(list(map(lambda e: e.to_node, self.edges_out)),
                      key=lambda n: n.name)

class NonRootNode(SyntaxNode, metaclass=ABCMeta):
    """A non-root syntax-node"""

    def __init__(self, name: str) -> None:
        if name == ROOT_NAME:
            raise Exception(f"non-root name can't be {ROOT_NAME}")
        super().__init__(name)

    def __eq__(self, other):
        return isinstance(other, NonRootNode) and super().__eq__(other)

    def __repr__(self):
        return f"NonRootNode('{self.name}')"

    @abstractmethod
    def clone(self) -> "NonRootNode":
        """override base-class"""

class TokenNode(NonRootNode, metaclass=ABCMeta):
    """A token (terminal symbol) in a syntax highlighting application"""

    def __init__(self, name: str, ftype: FormatType) -> None:
        """initialize the token"""
        super().__init__(name)
        self._ftype = ftype

    def __eq__(self, other):
        return isinstance(other, TokenNode) and \
                (self.ftype == other.ftype) and \
                super().__eq__(other)

    def __repr__(self):
        return f"TokenNode('{self.name}',{self.ftype})"

    @abstractmethod
    def clone(self) -> "NonRootNode":
        """override base-class"""

    def add_edge_out(self, edge: DCGedge) -> None:
        """overrides base class. disallow token from having output edges"""
        raise Exception(f"{self} cannot have output edges")

    @property
    def is_istart(self) -> bool:
        """if this name matches the group-start-and-inherit token regex"""
        return re.match(ISTART_TOKEN_REGEX, self.name) is not None

    @property
    def is_start(self) -> bool:
        """if this name matches the group-start token regex"""
        return re.match(START_TOKEN_REGEX, self.name) is not None

    @property
    def is_end(self) -> bool:
        """if this name matches the group-end token regex"""
        return re.match(END_TOKEN_REGEX, self.name) is not None

    @property
    def base_name(self) -> bool:
        """the name of the token, minus the group-start/group-end parts"""
        return re.sub(ISTART_TOKEN_REGEX, "",
                      re.sub(START_TOKEN_REGEX, "",
                             re.sub(END_TOKEN_REGEX, "", self.name)))

    @property
    def ftype(self) -> FormatType:
        """the FormatType of this token"""
        return self._ftype

class StringNode(TokenNode):
    """This node is a string token type"""

    def __init__(self, name: str, string: str, ftype: FormatType) -> None:
        """initializes is string token"""
        super().__init__(name, ftype)
        self._string = string

    def __eq__(self, other):
        return isinstance(other, StringNode) and \
                (self.string == other.string) and \
                super().__eq__(other)

    def __repr__(self):
        return f"StringNode('{self.name}','{self.string}',{self.ftype})"

    def clone(self) -> "StringNode":
        """override base-class"""
        return StringNode(self.name, self.string, self.ftype)

    @property
    def string(self) -> str:
        """the string literal"""
        return self._string

class RegexNode(TokenNode):
    """This node is a regex token type"""

    def __init__(self, name: str, pattern: str, ftype: FormatType) -> None:
        """initializes is regex token"""
        super().__init__(name, ftype)
        self._pattern = pattern

    def __eq__(self, other):
        return isinstance(other, RegexNode) and \
                (self.pattern == other.pattern) and \
                super().__eq__(other)

    def __repr__(self):
        return f"RegexNode('{self.name}','{self.pattern}',{self.ftype})"

    def clone(self) -> "RegexNode":
        """override base-class"""
        return RegexNode(self.name, self.pattern, self.ftype)

    @property
    def pattern(self) -> str:
        """the regex pattern of this token"""
        return self._pattern

class GroupNode(NonRootNode):
    """
    A group node is a syntax node that can contain other nodes. Originally,
    there were OptionNode (logical or node), and GroupNode (logical and).
    The nice thing about that was it allowed the converters to get really
    precise with the node hierarchy. The issue, however, was the fast-growing
    complexity to manage the cyclic graph with lots of unnecessary nodes.
    Therefore, the Option/Group nodes were merged into a single GroupNode
    that represents a logical, unsorted 'OR' of the child nodes. The
    syntax recognition is less powerful, but the implementation is simpler
    (and much faster).

    NOTE about start_name/end_name: you still need to make sure you
    graph.add_edge(group, start/end_node) after creating the group. The
    group will check if start_name/end_name refer to a valid start/end
    matching token pairs. if so, the group will assume the same ftype as
    the token-pair

    :param start_name: if present, specifies the node-name that starts this
                       group. if not present the group will get flattened
    :param end_name: if present, specifies the node-name that ends this
                     group. if not present the group will get flattened
    """
    def __init__(self, name: str, start_name: str = None,
                 end_name: str = None) -> None:
        super().__init__(name)
        self._start_name = start_name
        self._end_name = end_name

    def __eq__(self, other):
        return isinstance(other, GroupNode) and super().__eq__(other)

    def __repr__(self) -> str:
        args = f"'{self.name}','{self._start_name}','{self._end_name}'"
        return f"GroupNode({args})"

    def clone(self) -> "GroupNode":
        """override base-class. do NOT clone children!!!"""
        return GroupNode(self.name, self._start_name, self._end_name)

    @property
    def start_token(self) -> Optional[TokenNode]:
        """returns the start token-node of this group, if present"""
        if self._start_name is None:
            return None
        matches = list(filter(lambda e: e.name == self._start_name,
                              self.children))
        if (len(matches) == 1) and \
                isinstance(matches[0], TokenNode) and \
                (matches[0].is_start or matches[0].is_istart):
            return matches[0]
        return None

    @property
    def end_token(self) -> Optional[TokenNode]:
        """returns the end token-node of this group, if present"""
        if self._end_name is None:
            return None
        matches = list(filter(lambda e: e.name == self._end_name,
                              self.children))
        if (len(matches) == 1) and \
                isinstance(matches[0], TokenNode) and matches[0].is_end:
            return matches[0]
        return None

    @property
    def children(self) -> List[SyntaxNode]:
        """returns all the SORTED children SyntaxNodes"""
        return sorted(list(map(lambda e: e.to_node, self.edges_out)),
                      key=lambda n: n.name)

    @property
    def is_useless(self) -> bool:
        """
        true if the start_token/end_token are not a matching pair. This just
        means the group cant be recognized by syntax highlighters. The effect
        is that the group will be removed during graph compression
        """
        start = self.start_token
        end = self.end_token
        return (start is None) or (end is None) or \
                (start.base_name != end.base_name) or \
                (start.ftype != end.ftype)

    @property
    def ftype(self) -> FormatType:
        """
        determines FormatType from the start/end nodes. The ftype of the
        group is inherited from the start-token
        """
        start = self.start_token
        if not self.is_useless and start.is_istart:
            return start.ftype
        return FormatType.NoType
