"""CSC148 Lab 3: Inheritance

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the implementation of a simple number game.
The key class design feature here is *inheritance*, which is used
to enable different types of players, both human and computer, for the game.
"""
import random
from typing import Tuple


class NumberGame:
    """A number game for two players.

    A count starts at 0. On a player's turn, they add to the count an amount
    between a set minimum and a set maximum. The player whose move causes the
    count to be greater than or equal to a set goal amount is the winner.

    The game can have multiple rounds.

    === Attributes ===
    goal:
        The amount to reach in order to win the game.
    min_step:
        The minimum legal move.
    max_step:
        The maximum legal move.
    current:
        The current value of the game count.
    players:
        The two Players.
    turn:
        The turn the game is on, beginning with turn 0.
        If turn is even number, it is players[0]'s turn.
        If turn is any odd number, it is players[1]'s turn.

    === Representation invariants ==
    - turn >= 0
    - 0 <= current <= goal
    - 0 < min_step <= max_step <= goal
    """
    goal: int
    min_step: int
    max_step: int
    current: int
    players: Tuple['Player', 'Player']
    turn: int

    def __init__(self, goal: int, min_step: int, max_step: int,
                 players: Tuple['Player', 'Player']) -> None:
        """Initialize this NumberGame.

        Preconditions:
          - 0 < min_step <= max_step <= goal
        """
        self.goal = goal
        self.min_step = min_step
        self.max_step = max_step
        self.players = players
        self.turn = 0
        self.current = 0

    def play(self) -> None:
        """Play one round of this NumberGame.

        A "round" is one full run of the game, from when the count starts
        at 0 until the goal is reached.
        """
        while self.current < self.goal:
            self.play_one_turn()
        # The player whose turn would be next (if the game weren't over) is
        # the loser.  The one who went one turn before that is the winner.
        winner = self.whose_turn(self.turn - 1)
        print('And {} is the winner!!!'.format(winner.name))

    def whose_turn(self, turn: int) -> 'Player':
        """Return the Player whose turn it is on the given turn number.
        """
        if turn % 2 == 0:
            next_player = self.players[0]
        else:
            next_player = self.players[1]
        return next_player

    def play_one_turn(self) -> None:
        """Play a single turn in this NumberGame.

        Determine whose move it is, get their move, and update the current
        total as well as the number of the turn we are on.
        Print the move and the new total.
        """
        next_player = self.whose_turn(self.turn)
        amount = next_player.move(self.current, self.min_step, self.max_step, \
                                  self.goal)
        self.current += amount
        self.turn += 1

        print(f'{next_player.name} moves {amount}')
        print(f'Total is now {self.current}')


# TODO: Write classes Player, RandomPlayer, UserPlayer, and StrategicPlayer.
class Player():
    """ A player in the number game
    An Abstract class

    move: The ammount the player chooses to move

    === Representation Invariants ===
    min_step <= move <= max_step

    === Attributes ===
    id_: The players id
    """

    name: str

    def __init__(self, id_):
        """Initalizes the player"""
        self.name = id_

    def move(self, current, min_step, max_step, goal):
        """The ammount the player chooses to increment the count
        """
        raise NotImplementedError


class RandomPlayer(Player):
    """A player in the numbergame that does random turns"""
    id_: str

    def __init___(self, id_):
        """Initalizes a random player"""
        super(RandomPlayer, self).__init__(id_)

    def move(self, current, min_step, max_step, goal) -> int:
        """The ammount the player chooses to increment the count
        """
        return random.randint(min_step, max_step)


class UserPlayer(Player):
    """A player in the numbergame that does random turns"""
    id_: str

    def __init___(self, id_):
        """Initalizes a random player"""
        super(UserPlayer, self).__init__(id_)

    def move(self, current, min_step, max_step, goal) -> int:
        """The ammount the player chooses to increment the count
        """
        move = 0
        while not min_step <= move <= max_step:
            move = int(input("What is your move? Move must be between {} and {}"
                             .format(min_step, max_step)))
        return move


class StrategicPlayer(Player):
    """A player in the numbergame that does random turns"""
    id_: str

    def __init___(self, id_):
        """Initalizes a random player"""
        super(StrategicPlayer, self).__init__(id_)

    def move(self, current, min_step, max_step, goal) -> int:
        """The ammount the player chooses to increment the count
        """








def make_player(generic_name: str) -> 'Player':
    """Through user input, construct and return a new Player.

    Allow the user to choose a player name and player type.
    <generic_name> is a placeholder used to identify which player is being made.
    """
    name = input("What is {}'s name? ".format(generic_name))
    return RandomPlayer(name)
    # TODO: Create and return some sort of Player.







def main() -> None:
    """Create and play a NumberGame based on user input settings.
    """
    goal = int(input('Enter goal amount: '))
    minimum = int(input('Enter minimum move: '))
    maximum = int(input('Enter maximum move: '))
    p1 = make_player('p1')
    p2 = make_player('p2')
    while True:
        g = NumberGame(goal, minimum, maximum, (p1, p2))
        g.play()
        again = input('Again? (y/n) ')
        if again != 'y':
            return


if __name__ == '__main__':
    # Uncomment the lines below to check your work using
    # python_ta and doctest.
    # import python_ta
    # python_ta.check_all(config={
    #     'allowed-import-modules': [
    #         'random',
    #         'python_ta',
    #         'doctest',
    #         'typing'
    #     ],
    #     'allowed-io': [
    #         'main',
    #         'make_player',
    #         'move',
    #         'play',
    #         'play_one_turn'
    #     ]
    # })
    # import doctest
    # doctest.testmod()
    main()
