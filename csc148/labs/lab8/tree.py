"""Lab 8: Trees and Recursion, Tasks 1 & 2

=== CSC148 Fall 2016 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains a few Tree methods that you should implement recursively.
Make sure you understand both the theoretical idea of trees, as well as how
we represent them in our Tree class.
"""
import random  # For Task 2
from typing import Optional, List, Union, Tuple


class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and LinkedListRec
    from Lab 7; the only major difference is that _rest
    has been replaced by _subtrees to handle multiple
    recursive sub-parts.
    """
    # === Private Attributes ===
    # The item stored at this tree's root, or None if the tree is empty.
    _root: Optional[object]
    # The list of all subtrees of this tree.
    _subtrees: List['Tree']

    # === Representation Invariants ===
    # - If self._root is None then self._subtrees is an empty list.
    #   This setting of attributes represents an empty Tree.
    # - self._subtrees may be empty when self._root is not None.
    #   This setting of attributes represents a tree consisting of just one
    #   node.

    def __init__(self, root: object, subtrees: List['Tree']) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If <root> is None, the tree is empty.
        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees

    def prune(self, pred):  # works but must implement correct __eq__ method
        """Return a pruned tree
        >>> t1 = Tree(6, [Tree(8, []), Tree(9, [])])
        >>> t2 = Tree(4, [Tree(11, []), Tree(10, [])])
        >>> t3 = Tree(7, [Tree(3, []), Tree(12, [])])
        >>> t = Tree(5, [t1, t2, t3])
        >>> t3_pruned = Tree(7, [Tree(12, [])])
        >>> def predicate(x): return x > 4
        >>> t.prune(predicate)._subtrees[0] == Tree(5, [t1, t3_pruned])._subtrees[0]
        True
        """
        if pred(self._root) is False:
            return None
        children = []
        for child in self._subtrees:
            pruned = child.prune(pred)
            if pruned is not None:
                children.append(pruned)
        return Tree(self._root, children)

    def is_empty(self) -> bool:
        """Return True if this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of nodes contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1
            for subtree in self._subtrees:
                size += subtree.__len__()  # Could also do size += len(subtree)
            return size

    def count(self, item: object) -> int:
        """Return the number of occurrences of <item> in this tree.
        >>> t = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> t.count(3)
        1
        >>> t.count(100)
        0
        """
        if self.is_empty():
            return 0
        else:
            num = 0
            if self._root == item:
                num += 1
            for subtree in self._subtrees:
                num += subtree.count(item)
            return num

    def __str__(self) -> str:
        """return string representation of this tree"""
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        if self.is_empty():
            return ''
        string = depth * ' ' + str(self._root) + '\n'
        for sub in self._subtrees:
            string += sub._str_indented(depth + 1)
        return string

    # ------------------------------------------------------------------------
    # Lab Exercises
    # ------------------------------------------------------------------------
    def __contains__(self, item: object) -> bool:
        """Return whether <item> is in this tree.

        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> 1 in t  # Same as t.__contains__(1)
        True
        >>> 5 in t
        True
        >>> 4 in t
        False
        """
        if self._root == item:
            return True
        for tree in self._subtrees:
            if item in tree:
                return True
        return False

    def leaves(self) -> list:
        """Return a list of all of the leaf items in the tree.

        >>> Tree(None, []).leaves()
        []
        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> t.leaves()
        [2, 5]
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> rt = Tree(3, [Tree(6, []), Tree(7, [])])
        >>> t = Tree(1, [lt, rt])
        >>> t.leaves()
        [4, 5, 6, 7]
        """
        if self.is_empty():
            return []
        if self._subtrees == []:
            return [self._root]
        leaves = []
        for tree in self._subtrees:
            leaves.extend(tree.leaves())
        return leaves

    def longest_path(self) -> list:
        """returns longest path to the left
        >>> Tree(None, []).longest_path()
        []
        >>> t = Tree(17, [Tree(-2, [Tree(5, []), Tree(6, [Tree(-8, []), Tree(13, [])])]), \
        Tree(3, [Tree(-7, []), Tree(8, [ Tree(9, [])])]), Tree(4, [])])
        >>> t.longest_path()
        [17, -2, 6, -8]
        """
        if self.is_empty():
            return []
        lst = [self._root]
        child = []
        for item in self._subtrees[::-1]:
            x = item.longest_path()
            if len(x) >= len(child):
                child = x
        return lst + child

    def branching_factor(self) -> float:
        """Return the average branching factor of this tree.

        Return 0 if this tree is empty or consists of just a single root node.
        Remember to ignore all 0's coming from leaves in this calculation.

        >>> Tree(None, []).branching_factor()
        0.0
        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> t.branching_factor()
        2.0
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> rt = Tree(3, [Tree(6, []), Tree(7, []), Tree(8, []), Tree(9, []),\
                          Tree(10, [])])
        >>> t = Tree(1, [lt, rt])
        >>> t.branching_factor()
        3.0
        """
        # Note: you'll want to first implement _branching_factor_helper here.
        if self._subtrees == []:
            return 0.0
        num_branch = len(self._subtrees)
        num_nodes = 1
        for tree in self._subtrees:
            values = tree._branching_factor_helper()
            num_branch += values[0]
            num_nodes += values[1]
        return num_branch / num_nodes

    def _branching_factor_helper(self) -> Tuple[int, int]:
        """Return a tuple (x,y) where:

        x is the total branching factor of all non-leaf nodes in this tree, and
        y is the total number of non-leaf nodes in this tree.
        """
        x = len(self._subtrees)
        y = 0
        if self._subtrees != []:
            y += 1
        for tree in self._subtrees:
            values = tree._branching_factor_helper()
            x += values[0]
            y += values[1]
        return (x, y)

    def insert(self, item: object) -> None:
        """Insert <item> into this tree using the following algorithm.

            1. If the tree is empty, <item> is the new root of the tree.
            2. If the tree has a root but no subtrees, create a
               new tree containing the item, and make this new tree a subtree
               of the original tree.
            3. Otherwise, pick a random number between 1 and 3 inclusive.
                - If the random number is 3, create a new tree containing
                  the item, and make this new tree a subtree of the original.
                - If the random number is a 1 or 2, pick one of the existing
                  subtrees at random, and *recursively insert* the new item
                  into that subtree.

        >>> t = Tree(None, [])
        >>> t.insert(1)
        >>> 1 in t
        True
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> rt = Tree(3, [Tree(6, []), Tree(7, []), Tree(8, []), Tree(9, []),\
                          Tree(10, [])])
        >>> t = Tree(1, [lt, rt])
        >>> t.insert(100)
        >>> 100 in t
        True
        """
        if self.is_empty():
            self._root = item
        elif self._subtrees == []:
            self._subtrees = [Tree(item, [])]
        else:
            num = random.randint(1, 3)
            if num == 3:
                self._subtrees.append(Tree(item, []))
            else:
                num = random.randint(0, len(self._subtrees) - 1)
                self._subtrees[num].insert(item)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'random', 'typing', 'python_ta']
    })

    import doctest
    doctest.testmod()
