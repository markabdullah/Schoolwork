"""Lab 5: Linked List Exercises

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code for a linked list implementation with two classes,
LinkedList and _Node.

All of the code from lecture is here, as well as some exercises to work on.
"""
from typing import List, Optional, Callable


class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    === Attributes ===
    item:
        The data stored in this node.
    next:
        The next node in the list, or None if there are
        no more nodes in the list.
    """
    item: object
    next: Optional['_Node']

    def __init__(self, item: object) -> None:
        """Initialize a new node storing <item>, with no next node.
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


class LinkedList:
    """A linked list implementation of the List ADT.
    """
    # === Private Attributes ===
    # _first:
    #     The first node in the linked list, or None if the list is empty.
    _first: Optional[_Node]

    def __init__(self, items: list) -> None:
        """Initialize a new linked list containing the given items.

        The first node in the linked list contains the first item
        in <items>.
        """
        if len(items) == 0:  # No items, and an empty list!
            self._first = None
        else:
            self._first = _Node(items[0])
            current_node = self._first
            for item in items[1:]:
                current_node.next = _Node(item)
                current_node = current_node.next

    # ------------------------------------------------------------------------
    # Non-mutating methods: these methods do not change the list
    # ------------------------------------------------------------------------
    def is_empty(self) -> bool:
        """Return whether this linked list is empty.

        >>> LinkedList([]).is_empty()
        True
        >>> LinkedList([1, 2, 3]).is_empty()
        False
        """
        return self._first is None

    def __str__(self) -> str:
        """Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.

        >>> str(LinkedList([1, 2, 3]))
        '[1 -> 2 -> 3]'
        >>> str(LinkedList([]))
        '[]'
        """
        items = []
        curr = self._first
        while curr is not None:
            items.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'

    def __getitem__(self, index: int) -> object:
        """Return the item at position <index> in this list.

        Raise IndexError if <index> is >= the length of this list.

        >>> linky = LinkedList([100, 4, -50, 13])
        >>> linky[0]          # Equivalent to linky.__getitem__(0)
        100
        >>> linky[2]
        -50
        >>> linky[100]
        Traceback (most recent call last):
        IndexError
        """
        curr = self._first
        curr_index = 0

        while curr is not None and curr_index < index:
            curr = curr.next
            curr_index += 1

        assert curr is None or curr_index == index

        if curr is None:
            raise IndexError
        else:
            return curr.item

    def insert(self, index: int, item: object) -> None:
        """Inserts a new node containing item at position <index>
        Raise IndexError if index > len(self) or index < 0"""
        new_node = _Node(item)
        if index == 0:
            new_node.next = self._first
            self._first = new_node
        else:
            curr = self._first
            curr_index = 0
            while curr is not None and curr_index < (index-1):
                curr = curr.next
                curr_index += 1
            # We know either
            # 1) curr is None
            # 2) curr_index == index-1
            if curr is None:
                raise IndexError
            else:
                new_node.next = curr.next
                curr.next = new_node
        pass

    # -------------------------------------------------------------------------
    # Lab Exercises
    # -------------------------------------------------------------------------
    def __len__(self) -> int:
        """Return the number of elements in this list.

        >>> lst = LinkedList([])
        >>> len(lst)              # Equivalent to lst.__len__()
        0
        >>> lst = LinkedList([1, 2, 3])
        >>> len(lst)
        3
        """
        curr = self._first
        count = 0
        while curr is not None:
            count += 1
            curr = curr.next
        return count

    def __contains__(self, item: object) -> bool:
        """Return whether <item> is in this list.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 3])
        >>> 2 in lst                     # Equivalent to lst.__contains__(2)
        True
        >>> 4 in lst
        False
        """
        curr = self._first
        while curr is not None:
            if item == curr.item:
                return True
            curr = curr.next
        return False

    def __getitem__(self, index: int):
        """
        >>> lst = LinkedList([1, 2, 3])
        >>> lst[1]
        2
        """
        curr = self._first
        curr_index = 0
        while (curr is not None) and (curr_index != index):
            curr = curr.next
            curr_index += 1
        # We know either curr_index == index or curr is None
        assert (curr is None) or (curr_index == index)

        if curr is None:
            raise IndexError
        else:
            return curr.item

    def merge_pairs(self):
        """
        >>> linky = LinkedList([1, 2, 30, 40, 5, 6])
        >>> str(linky)
        '[1 -> 2 -> 30 -> 40 -> 5 -> 6]'
        >>> linky.merge_pairs()
        >>> str(linky)
        '[3 -> 70 -> 11]'
        """
        curr = self._first
        while curr is not None and curr.next is not None:
            curr.item += curr.next.item
            curr.next = curr.next.next
            curr = curr.next

    def count(self, item: object) -> int:
        """Return the number of times <item> occurs in this list.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 1, 3, 2, 1])
        >>> lst.count(1)
        3
        >>> lst.count(2)
        2
        >>> lst.count(3)
        1
        """
        count = 0
        curr = self._first
        while curr is not None:
            if item == curr.item:
                count += 1
            curr = curr.next
        return count

    def index(self, item: object) -> int:
        """Return the index of the first occurrence of <item> in this list.

        Raise ValueError if the <item> is not present.

        Use == to compare items.

        >>> lst = LinkedList([1, 2, 1, 3, 2, 1])
        >>> lst.index(1)
        0
        >>> lst.index(3)
        3
        >>> lst.index(148)
        Traceback (most recent call last):
        ValueError
        """
        count = 0
        curr = self._first
        while curr is not None:
            if item == curr.item:
                return count
            curr = curr.next
            count += 1
        raise ValueError


if __name__ == '__main__':
    # import python_ta
    # python_ta.check_all()
    import doctest
    doctest.testmod()
