from abc import (ABC,
                 abstractmethod)
from itertools import chain
from typing import (Generic,
                    Iterable,
                    Iterator,
                    List,
                    MutableSet,
                    Optional,
                    Sequence,
                    Tuple,
                    Union)

from lz.iterating import capacity
from reprit.base import generate_repr

from .hints import (Domain,
                    OtherDomain,
                    Sortable,
                    SortingKey)

NIL = None


class Node(ABC):
    left = NIL  # type: Union['Node', NIL]
    right = NIL  # type: Union['Node', NIL]

    @property
    @abstractmethod
    def value(self) -> Domain:
        """Contained value."""

    @property
    @abstractmethod
    def key(self) -> Sortable:
        """Comparisons key."""


class SimpleNode(Node):
    __slots__ = ('_value', 'left', 'right')

    def __init__(self, value: Domain,
                 *,
                 left: Union['SimpleNode', NIL] = NIL,
                 right: Union['SimpleNode', NIL] = NIL) -> None:
        self._value = value
        self.left = left
        self.right = right

    __repr__ = generate_repr(__init__)

    @property
    def value(self) -> Domain:
        return self._value

    @property
    def key(self) -> Sortable:
        return self._value


class ComplexNode(Node):
    __slots__ = ('_key', '_value', 'left', 'right')

    def __init__(self, key: Sortable, value: Domain,
                 *,
                 left: Union['ComplexNode', NIL] = NIL,
                 right: Union['ComplexNode', NIL] = NIL) -> None:
        self._value = value
        self._key = key
        self.left = left
        self.right = right

    __repr__ = generate_repr(__init__)

    @property
    def value(self) -> Domain:
        return self._value

    @property
    def key(self) -> Sortable:
        return self._key


@MutableSet.register
class TreeBase(ABC, Generic[Domain]):
    @property
    @abstractmethod
    def root(self) -> Union[Node, NIL]:
        """Root node."""

    @property
    @abstractmethod
    def key(self) -> Optional[SortingKey]:
        """Sorting key."""

    @classmethod
    @abstractmethod
    def from_iterable(cls, values: Iterable[Domain],
                      *,
                      key: Optional[SortingKey] = None) -> 'TreeBase[Domain]':
        """Constructs tree from given iterable using given sorting key."""

    def __len__(self) -> int:
        """Returns number of nodes."""
        return capacity(iter(self))

    def __iter__(self) -> Iterator[Domain]:
        """Returns iterator over values."""
        node = self.root
        queue = []
        while True:
            while node is not NIL:
                queue.append(node)
                node = node.left
            if not queue:
                return
            node = queue.pop()
            yield node.value
            node = node.right

    @abstractmethod
    def __contains__(self, value: Domain) -> bool:
        """Checks if given value is contained in the tree."""

    def __eq__(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree is equal to given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return len(self) == len(other) and self <= other <= self

    def __le__(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree is a subset of given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return (len(self) <= len(other)
                and all(value in other for value in self))

    def __lt__(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree is a strict subset of given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return (len(self) < len(other)
                and self <= other and self != other)

    def __gt__(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree is a strict superset of given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return (len(self) > len(other)
                and self >= other and self != other)

    def __ge__(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree is a superset of given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return (len(self) >= len(other)
                and all(value in self for value in other))

    def __and__(self, other: 'TreeBase[OtherDomain]') -> 'TreeBase[Domain]':
        """Returns intersection of the tree with given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return self.from_iterable((value for value in self if value in other),
                                  key=self.key)

    def __or__(self, other: 'TreeBase[OtherDomain]'
               ) -> 'TreeBase[Union[Domain, OtherDomain]]':
        """Returns union of the tree with given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return self.from_iterable(chain(self, other),
                                  key=self.key)

    def __sub__(self, other: 'TreeBase[OtherDomain]') -> 'TreeBase[Domain]':
        """Returns subtraction of the tree with given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return self.from_iterable((value
                                   for value in self
                                   if value not in other),
                                  key=self.key)

    def __xor__(self, other: 'TreeBase[OtherDomain]'
                ) -> 'TreeBase[Union[Domain, OtherDomain]]':
        """Returns symmetric difference of the tree with given one."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        return (self - other) | (other - self)

    def __iand__(self, other: 'TreeBase[OtherDomain]') -> 'TreeBase[Domain]':
        """Intersects the tree with given one in-place."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        for value in self - other:
            self.discard(value)
        return self

    def __ior__(self, other: 'TreeBase[OtherDomain]'
                ) -> 'TreeBase[Union[Domain, OtherDomain]]':
        """Unites the tree with given one in-place."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        for value in other:
            self.add(value)
        return self

    def __ixor__(self, other: 'TreeBase[OtherDomain]'
                 ) -> 'TreeBase[Union[Domain, OtherDomain]]':
        """Exclusively disjoins the tree with given one in-place."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        if self == other:
            self.clear()
        else:
            for value in other:
                if value in self:
                    self.discard(value)
                else:
                    self.add(value)
        return self

    def __isub__(self, other: 'TreeBase[OtherDomain]') -> 'TreeBase[Domain]':
        """Subtracts from the tree a given one in-place."""
        if not isinstance(other, TreeBase):
            return NotImplemented
        if self == other:
            self.clear()
        else:
            for value in other:
                self.discard(value)
        return self

    def max(self) -> Domain:
        """Returns maximum value from the tree."""
        node = self.root
        if node is NIL:
            raise ValueError('Tree is empty.')
        while node.right is not NIL:
            node = node.right
        return node.value

    def min(self) -> Domain:
        """Returns minimum value from the tree."""
        node = self.root
        if node is NIL:
            raise ValueError('Tree is empty.')
        while node.left is not NIL:
            node = node.left
        return node.value

    @abstractmethod
    def add(self, value: Domain) -> None:
        """Adds given value to the tree."""

    def remove(self, value: Domain) -> None:
        """Removes given value from the tree."""
        if value not in self:
            raise KeyError(value)
        self.discard(value)

    @abstractmethod
    def discard(self, value: Domain) -> None:
        """Removes given value from the tree if it exists."""

    def pop(self) -> Domain:
        """Pops value from the tree."""
        iterator = iter(self)
        try:
            result = next(iterator)
        except StopIteration:
            raise KeyError
        self.discard(result)
        return result

    @abstractmethod
    def popmax(self) -> Domain:
        """Pops maximum value from the tree."""

    @abstractmethod
    def popmin(self) -> Domain:
        """Pops minimum value from the tree."""

    @abstractmethod
    def clear(self) -> None:
        """Clears the tree."""

    def isdisjoint(self, other: 'TreeBase[OtherDomain]') -> bool:
        """Checks if the tree has no intersection with given one."""

        def _are_disjoint(left: TreeBase[Domain],
                          right: TreeBase[OtherDomain]) -> bool:
            for value in left:
                if value in right:
                    return False
            return True

        return (_are_disjoint(self, other)
                if len(self) < len(other)
                else _are_disjoint(other, self))


class Tree(TreeBase[Domain]):
    def __init__(self, root: Union[Node, NIL],
                 *,
                 key: Optional[SortingKey] = None) -> None:
        self._root = root
        self._key = key

    __repr__ = generate_repr(__init__,
                             with_module_name=True)

    @property
    def root(self) -> Union[Node, NIL]:
        return self._root

    @property
    def key(self) -> Optional[SortingKey]:
        return self._key

    def __contains__(self, value: Domain) -> bool:
        node = self._root
        if node is NIL:
            return False
        key = self._to_key(value)
        while node is not NIL:
            if key < node.key:
                node = node.left
            elif node.key < key:
                node = node.right
            else:
                return True
        return False

    def add(self, value: Domain) -> None:
        parent = self._root
        if parent is NIL:
            self._root = self._make_node(value)
            return
        key = self._to_key(value)
        while True:
            if key < parent.key:
                if parent.left is NIL:
                    parent.left = self._make_node(value)
                    return
                else:
                    parent = parent.left
            elif parent.key < key:
                if parent.right is NIL:
                    parent.right = self._make_node(value)
                    return
                else:
                    parent = parent.right
            else:
                return

    def discard(self, value: Domain) -> None:
        parent = self._root
        if parent is NIL:
            return
        key = self._to_key(value)
        if parent.key == key:
            if parent.left is NIL:
                self._root = parent.right
            else:
                node = parent.left
                if node.right is NIL:
                    self._root, node.right = node, self._root.right
                else:
                    while node.right.right is not NIL:
                        node = node.right
                    (self._root, node.right.left, node.right.right,
                     node.right) = (
                        node.right, self._root.left, self._root.right,
                        node.right.left)
            return
        while True:
            if key < parent.key:
                # search in left subtree
                if parent.left is NIL:
                    return
                elif parent.left.key == key:
                    # remove `parent.left`
                    node = parent.left.left
                    if node is NIL:
                        parent.left = parent.left.right
                        return
                    elif node.right is NIL:
                        parent.left, node.right = node, parent.left.right
                    else:
                        while node.right.right is not NIL:
                            node = node.right
                        (parent.left, node.right.left, node.right.right,
                         node.right) = (
                            node.right, parent.left.left, parent.left.right,
                            node.right.left)
                else:
                    parent = parent.left
            else:
                # search in right subtree
                if parent.right is NIL:
                    return
                elif parent.right.key == key:
                    # remove `parent.right`
                    node = parent.right.left
                    if node is NIL:
                        parent.right = parent.right.right
                        return
                    elif node.right is NIL:
                        parent.right, node.right = node, parent.right.right
                    else:
                        while node.right.right is not NIL:
                            node = node.right
                        (parent.right, node.right.left, node.right.right,
                         node.right) = (
                            node.right, parent.right.left, parent.right.right,
                            node.right.left)
                else:
                    parent = parent.right

    def popmax(self) -> Domain:
        node = self._root
        if node is NIL:
            raise KeyError
        elif node.right is NIL:
            self._root = node.left
            return node.value
        else:
            while node.right.right is not NIL:
                node = node.right
            result, node.right = node.right.value, node.right.left
            return result

    def popmin(self) -> Domain:
        node = self._root
        if node is NIL:
            raise KeyError
        elif node.left is NIL:
            self._root = node.right
            return node.value
        else:
            while node.left.left is not NIL:
                node = node.left
            result, node.left = node.left.value, node.left.right
            return result

    def clear(self) -> None:
        self._root = None

    def _make_node(self, value: Domain) -> Node:
        if self._key is None:
            return SimpleNode(value)
        else:
            return ComplexNode(self._key(value), value)

    def _to_key(self, value: Domain) -> Sortable:
        return value if self._key is None else self._key(value)

    @classmethod
    def from_iterable(cls, values: Iterable[Domain],
                      *,
                      key: Optional[SortingKey] = None) -> 'Tree[Domain]':
        values = list(values)
        if not values:
            root = NIL
        elif key is None:
            values = _to_unique_sorted_values(values)

            def to_node(start_index: int, end_index: int) -> SimpleNode:
                middle_index = (start_index + end_index) // 2
                return SimpleNode(values[middle_index],
                                  left=(to_node(start_index, middle_index)
                                        if middle_index > start_index
                                        else NIL),
                                  right=(to_node(middle_index + 1, end_index)
                                         if middle_index < end_index - 1
                                         else NIL))

            root = to_node(0, len(values))
        else:
            items = _to_unique_sorted_items(values, key)

            def to_node(start_index: int, end_index: int) -> ComplexNode:
                middle_index = (start_index + end_index) // 2
                return ComplexNode(*items[middle_index],
                                   left=(to_node(start_index, middle_index)
                                         if middle_index > start_index
                                         else NIL),
                                   right=(to_node(middle_index + 1, end_index)
                                          if middle_index < end_index - 1
                                          else NIL))

            root = to_node(0, len(items))
        return cls(root,
                   key=key)


def tree(*values: Domain, key: Optional[SortingKey] = None) -> Tree[Domain]:
    return Tree.from_iterable(values,
                              key=key)


def _to_unique_sorted_items(values: Sequence[Domain], sorting_key: SortingKey
                            ) -> Sequence[Tuple[Sortable, Domain]]:
    keys_indices = []  # type: List[Tuple[Sortable, int]]
    for key, index in sorted((sorting_key(value), index)
                             for index, value in enumerate(values)):
        while keys_indices and keys_indices[-1][0] == key:
            del keys_indices[-1]
        keys_indices.append((key, index))
    return [(key, values[index]) for key, index in keys_indices]


def _to_unique_sorted_values(values: Sequence[Domain]) -> Sequence[Domain]:
    result = []  # type: List[Domain]
    for value in sorted(values):
        while result and result[-1] == value:
            del result[-1]
        result.append(value)
    return result
