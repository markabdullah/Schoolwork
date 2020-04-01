"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the player class hierarchy.
"""

import random
from typing import Optional, Tuple
import pygame
from renderer import Renderer
from block import Block
from goal import Goal

TIME_DELAY = 600


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    renderer:
        The object that draws our Blocky board on the screen
        and tracks user interactions with the Blocky board.
    id:
        This player's number.  Used by the renderer to refer to the player,
        for example as "Player 2"
    goal:
        This player's assigned goal for the game.
    """
    renderer: Renderer
    id: int
    goal: Goal

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.renderer = renderer
        self.id = player_id

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.
        """
        raise NotImplementedError


class HumanPlayer(Player):
    """A human player.

    A HumanPlayer can do a limited number of smashes.

    === Public Attributes ===
    num_smashes:
        number of smashes which this HumanPlayer has performed
    === Representation Invariants ===
    num_smashes >= 0
    """
    # === Private Attributes ===
    # _selected_block
    #     The Block that the user has most recently selected for action;
    #     changes upon movement of the cursor and use of arrow keys
    #     to select desired level.
    # _level:
    #     The level of the Block that the user selected
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0

    # The total number of 'smash' moves a HumanPlayer can make during a game.
    MAX_SMASHES = 1

    num_smashes: int
    _selected_block: Optional[Block]
    _level: int

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        super().__init__(renderer, player_id, goal)
        self.num_smashes = 0

        # This HumanPlayer has done no smashes yet.
        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._selected_block = None

    def process_event(self, board: Block,
                      event: pygame.event.Event) -> Optional[int]:
        """Process the given pygame <event>.

        Identify the selected block and mark it as highlighted.  Then identify
        what it is that <event> indicates needs to happen to <board>
        and do it.

        Return
           - None if <event> was not a board-changing move (that is, if was
             a change in cursor position, or a change in _level made via
            the arrow keys),
           - 1 if <event> was a successful move, and
           - 0 if <event> was an unsuccessful move (for example in the case of
             trying to smash in an invalid location or when the player is not
             allowed further smashes).
        """
        # Get the new "selected" block from the position of the cursor
        block = board.get_selected_block(pygame.mouse.get_pos(), self._level)

        # Remove the highlighting from the old "_selected_block"
        # before highlighting the new one
        if self._selected_block is not None:
            self._selected_block.highlighted = False
        self._selected_block = block
        self._selected_block.highlighted = True

        # Since get_selected_block may have not returned the block at
        # the requested level (due to the level being too low in the tree),
        # set the _level attribute to reflect the level of the block which
        # was actually returned.
        self._level = block.level

        if event.type == pygame.MOUSEBUTTONDOWN:
            block.rotate(event.button)
            return 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if block.parent is not None:
                    self._level -= 1
                return None

            elif event.key == pygame.K_DOWN:
                if len(block.children) != 0:
                    self._level += 1
                return None

            elif event.key == pygame.K_h:
                block.swap(0)
                return 1

            elif event.key == pygame.K_v:
                block.swap(1)
                return 1

            elif event.key == pygame.K_s:
                if self.num_smashes >= self.MAX_SMASHES:
                    print('Can\'t smash again!')
                    return 0
                if block.smash():
                    self.num_smashes += 1
                    return 1
                else:
                    print('Tried to smash at an invalid depth!')
                    return 0

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.

        This method will hold focus until a valid move is performed.
        """
        self._level = 0
        self._selected_block = board

        # Remove all previous events from the queue in case the other players
        # have added events to the queue accidentally.
        pygame.event.clear()

        # Keep checking the moves performed by the player until a valid move
        # has been completed. Draw the board on every loop to draw the
        # selected block properly on screen.
        while True:
            self.renderer.draw(board, self.id)
            # loop through all of the events within the event queue
            # (all pending events from the user input)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 1

                result = self.process_event(board, event)
                self.renderer.draw(board, self.id)
                if result is not None and result > 0:
                    # un-highlight the selected block
                    self._selected_block.highlighted = False
                    return 0


class RandomPlayer(Player):
    """A Random player in the game"""
    def make_move(self, board: Block) -> int:
        """Performs a move at random. If chosen to smash at top level or max
        depth, it will forfeit its turn.

        Return 0 upon successful completion of a move.
        """
        # Choose a random block
        level = random.randint(0, board.max_depth)
        random_x = random.randint(0, board.size)
        random_y = random.randint(0, board.size)
        block = board.get_selected_block((random_x, random_y), level)
        block.highlighted = True
        self.renderer.draw(board, self.id)
        pygame.time.wait(TIME_DELAY)
        move = random.randint(1, 5)  # Perform a random move
        if move == 1:
            block.rotate(1)
        elif move == 2:
            block.rotate(3)
        elif move == 3:
            block.swap(0)
        elif move == 4:
            block.swap(1)
        elif move == 5:
            if 0 < level < board.max_depth:  # Forfeits turn otherwise
                block.smash()
        block.highlighted = False
        self.renderer.draw(board, self.id)
        return 0


class SmartPlayer(Player):
    """A smart player in the game"""
    def __init__(self, renderer: Renderer, player_id: int, goal: Goal,
                 difficulty: int) -> None:
        """Initialize this Player.
        """
        Player.__init__(self, renderer, player_id, goal)
        self.difficulty = difficulty

    def make_move(self, board: Block) -> int:
        """Choose a smart move to play.

        Return 0 upon successful completion of a move.
        """
        moves = []
        # moves is a list of possible moves to choose from
        smartness = {0: 5, 1: 10, 2: 25, 3: 50, 4: 100, 5: 150}
        if self.difficulty <= 5:
            num_moves = smartness[self.difficulty]
        else:
            num_moves = 150
        for _ in range(num_moves):
            moves.append(self._get_random_move(board))

        # Find the move that yields the highest score
        best = moves[0]
        max_ = 0
        for move in moves:
            if move[4] > max_:  # Index 4 of move is the score it yields
                best = move
                max_ = move[4]
        return self._perform_move(best, board)

    def _perform_move(self, move: Tuple, board: Block) -> int:
        """Helper method to perform a move
         Return 0 upon successful completion of a move."""
        #  move is a tuple containing (x, y, level, move, score)
        block = board.get_selected_block((move[0], move[1]), move[2])
        block.highlighted = True
        self.renderer.draw(board, self.id)
        pygame.time.wait(TIME_DELAY)
        if move[3] == 1:
            block.rotate(1)
        elif move[3] == 2:
            block.rotate(3)
        elif move[3] == 3:
            block.swap(0)
        elif move[3] == 4:
            block.swap(1)
        block.highlighted = False
        self.renderer.draw(board, self.id)
        return 0

    def _get_random_move(self, board: Block) -> Tuple[int, int, int, int, int]:
        """Helper method for make_move. Return a tuple describing a random move
         and its resulting score. Return a tuple containing related info to the
         move, in the form (x, y, level, move, score). """
        # === Representation Invariants ===
        # <board> is returned to its original state

        random_x = random.randint(0, board.size)
        random_y = random.randint(0, board.size)
        level = random.randint(0, board.max_depth)
        block = board.get_selected_block((random_x, random_y), level)
        move = random.randint(1, 4)
        if move == 1:
            block.rotate(1)
            score = self.goal.score(board)
            block.rotate(3)
        elif move == 2:
            block.rotate(3)
            score = self.goal.score(board)
            block.rotate(1)
        elif move == 3:
            block.swap(0)
            score = self.goal.score(board)
            block.swap(0)
        else:  # move == 4:
            block.swap(1)
            score = self.goal.score(board)
            block.swap(1)
        return (random_x, random_y, level, move, score)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer',
            'pygame'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
