"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Goal class hierarchy.
"""

from typing import List, Tuple
from block import Block


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    colour, anywhere within the Block.
    """

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
           -1  if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        try:
            # pos is negative, hence this call is technically out of bounds
            if pos[0] == -1 or pos[1] == -1:
                blob = 0
            elif visited[pos[0]][pos[1]] != -1:  # Cell has already been visited
                blob = 0
            # Cell hasn't been visited and has goal's colour
            elif board[pos[0]][pos[1]] == self.colour:
                visited[pos[0]][pos[1]] = 1
                blob = 1
                # Check surrounding blocks
                blob += self._undiscovered_blob_size((pos[0] + 1, pos[1]),
                                                     board, visited)
                blob += self._undiscovered_blob_size((pos[0], pos[1] + 1),
                                                     board, visited)
                blob += self._undiscovered_blob_size((pos[0] - 1, pos[1]),
                                                     board, visited)
                blob += self._undiscovered_blob_size((pos[0], pos[1] - 1),
                                                     board, visited)
            else:  # Cell hasn't been visited, but is of wrong colour
                visited[pos[0]][pos[1]] = 0
                blob = 0
        except IndexError:  # Cell is out of bounds for board
            blob = 0
        return blob

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        flat = board.flatten()
        visited = []
        score = 0
        # Make <visited> to be a list with the same structure of <flat>,
        # but with <-1> in all cells
        for i in range(len(flat)):
            visited.append([])
            for _ in range(len(flat)):
                visited[i].append(-1)

        for i in range(len(flat)):
            for j in range(len(flat)):
                score = max(score, self._undiscovered_blob_size((j, i), flat,
                                                                visited))
        return score

    def description(self) -> str:
        """Return a description of this goal.
        """
        return 'Create the largest connected blob with colour'


class PerimeterGoal(Goal):
    """A goal to have to most unit blocks of a given colour on the outer
    perimeter of the board.
    """

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        score = 0
        unit_blocks = board.flatten()
        # Since corner unit cells are worth 2x the score, we need to check
        # those individually, then check the rest of the perimeter.
        for column in range(0, -2, -1):  # First and last column
            for row in range(0, -2, -1):  # First and last row --> Corners
                if unit_blocks[column][row] == self.colour:
                    score += 2  # Corner unit blocks get 2x score
            for row in range(1, len(unit_blocks) - 1):  # rest of the column
                if unit_blocks[column][row] == self.colour:
                    score += 1
        for column in range(1, len(unit_blocks) - 1):  # Center columns
            for row in range(0, -2, -1):  # Top and bottom rows
                if unit_blocks[column][row] == self.colour:
                    score += 1
        return score

    def description(self) -> str:
        """Return a description of this goal.
        """
        return 'Have the most blocks on the boards perimeter with colour'


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
        'max-attributes': 15
    })
