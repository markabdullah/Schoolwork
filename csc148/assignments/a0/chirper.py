"""CSC148 Assignment 0

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains the starter code for Assignment 0.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""

from __future__ import annotations
from typing import List, Dict, TextIO, Optional
from datetime import datetime

CHEEP_LENGTH = 100
SENTINEL = 'END_REPLIES'


class Cheep:
    """A class to represent a cheep.

    === Public Attributes ===
    user: The user who wrote this cheep
    date: The day and time this cheep was posted

    === Private Attributes
    _text: The text of the cheep
    _replies: cheeps that are a reply to this cheep

    === Representation Invariants ===
    - len(_text) <= CHEEP_LENGTH
    - _replies is sorted in ascending chronological order and contains only
    cheeps that are newer than this cheep
    """

    user: str
    date: datetime
    _text: str
    _replies: List[Cheep]

    def __init__(self, user: str, text: str, date: datetime = None) -> None:
        """Initialize this cheep to have username <user>, text <text>, and date
        <date>, with empty replies.
        If no date is provided, use the current date and time.
        Text should be truncated to a maximum of CHEEP_LENGTH characters.

        >>> c1 = Cheep('UofT', 'Happy back to school!', \
        datetime(2019, 9, 5, 9, 1, 0))
        >>> c1.user
        'UofT'
        >>> c1._text
        'Happy back to school!'
        >>> c1.date
        datetime.datetime(2019, 9, 5, 9, 1)
        >>> c2 = Cheep('someone', 'A' * (CHEEP_LENGTH - 1) + 'B' * 100)
        >>> c2._text == 'A' * (CHEEP_LENGTH - 1) + 'B'
        True
        """
        self.user = user
        self.date = date
        if date is None:
            self.date = datetime.now()
        self._text = text[:100]
        self._replies = []

    def add_reply(self, reply: Cheep) -> None:
        """Add <reply> to the replies for this cheep, if reply was posted at a
        later date. Otherwise, do not add to replies.

        Replies must be added in chronological order.

        >>> c1 = Cheep('UofT', 'Happy back to school!', \
        datetime(2019, 9, 5, 9, 1, 0))
        >>> c2 = Cheep('a_student', 'First class!', \
        datetime(2019, 9, 5, 11, 1, 0))
        >>> c1.add_reply(c2)
        >>> len(c1._replies)
        1
        >>> t3 = Cheep('a_student', 'Setting my alarm!', \
        datetime(2019, 9, 4, 22, 30, 0))
        >>> c1.add_reply(t3)
        >>> len(c1._replies)
        1
        """
        if self.date >= reply.date:
            return
        pos = 0
        while pos < len(self._replies) and (self._replies[pos].date < reply.date):
            pos += 1
        self._replies.insert(pos, reply)

    def get_repliers(self) -> List[str]:
        """Return a list of users (including duplicates) that replied to
        this cheep, in the order they appear.

        >>> c1 = Cheep('UofT', 'Happy back to school!', \
        datetime(2019, 9, 5, 9, 1, 0))
        >>> c2 = Cheep('a_student', 'First CSC148 lecture!', \
        datetime(2019, 9, 9))
        >>> c1.add_reply(c2)
        >>> t3 = Cheep('a_student', 'Weekend!!', datetime(2019, 9, 7))
        >>> c1.add_reply(t3)
        >>> c4 = Cheep('prof_smith', 'Prepping my lecture', \
        datetime(2019, 9 ,6))
        >>> c1.add_reply(c4)
        >>> c1.get_repliers()
        ['prof_smith', 'a_student', 'a_student']
        """
        repliers = []
        for reply in self._replies:
            repliers.append(reply.user)
        return repliers

    def __contains__(self, keyword: str) -> bool:
        """Return True iff <keyword> is contained in the text of this cheep.

        >>> c1 = Cheep('user1', 'I love cats!')
        >>> 'cat' in c1
        True
        >>> c2 = Cheep('user1', 'A' * CHEEP_LENGTH + 'I love cats!')
        >>> 'cat' in c2
        False
        """
        if keyword in self._text:
            return True
        else:
            return False

    def __str__(self) -> str:
        """Return the string representation of this cheep.

        >>> c1 = Cheep('UofT', 'Happy back to school!', \
        datetime(2019, 9, 5, 9, 1, 0))
        >>> c2 = Cheep('a_student', 'First CSC148 lecture!', \
        datetime(2019, 9, 9))
        >>> c1.add_reply(c2)
        >>> t3 = Cheep('a_student', 'Weekend!!', datetime(2019, 9, 7))
        >>> c1.add_reply(t3)
        >>> c4 = Cheep('prof_smith', 'Prepping my lecture', \
        datetime(2019, 9 ,6))
        >>> c1.add_reply(c4)
        >>> print(c1)
        UofT said: Happy back to school!
        prof_smith replied: Prepping my lecture
        a_student replied: Weekend!!
        a_student replied: First CSC148 lecture!
        """
        string = self.user + " said: " + self._text
        for reply in self._replies:
            string += "\n" + reply.user + " replied: " + reply._text
        return string


class Chirper:
    """A class to represent our social media platform Chirper.

    === Private Attributes ===
    _cheeps: The cheeps in this Chirper instance
    """
    _cheeps: List[Cheep]

    def __init__(self) -> None:
        """Initialize this Chirper to have no cheeps.

        >>> chirper = Chirper()
        >>> len(chirper._cheeps)
        0
        """
        self._cheeps = []

    def post_cheep(self, new_cheep: Cheep) -> None:
        """Add the cheep <new_cheep> to this Chirper.

        >>> c1 = Cheep('UofT', 'Happy back to school!', datetime(2019, 9, 5))
        >>> chirper = Chirper()
        >>> chirper.post_cheep(c1)
        >>> len(chirper._cheeps)
        1
        """
        self._cheeps.append(new_cheep)

    def cheeps_by_year(self) -> Dict[int, List[Cheep]]:
        """Return a dictionary with keys as the years for cheeps in this
        Chirper, and values are the cheeps from that year.

        Years for which there are no cheeps should not appear in the dictionary.

        >>> c1 = Cheep('UofT', 'Happy back to school!', datetime(2019, 9, 5))
        >>> c2 = Cheep('a_user', 'I love summer', datetime(2019, 7, 15))
        >>> t3 = Cheep('user2', 'Pancakes or waffles?', datetime(2017, 5, 15))
        >>> chirper = Chirper()
        >>> chirper.post_cheep(c1)
        >>> chirper.post_cheep(c2)
        >>> chirper.post_cheep(t3)
        >>> chirper.cheeps_by_year() == {2019: [c1, c2], 2017: [t3]}
        True
        """
        years = {}
        for cheep in self._cheeps:
            if cheep.date.year in years:
                years[cheep.date.year].append(cheep)
            else:
                years[cheep.date.year] = [cheep]

        return years

    def read_cheeps(self, f: TextIO) -> None:
        """Read in cheeps from a text file <f>. Every cheep should be stored in
        this Chirper, and cheeps that are replies should also be added to
        the reply list of the cheep they reply to.

        Each line in the file is formatted as:
        user,cheep_text,year,month,day,hour,minute,second
        OR
        a sentinel denoting the end of replies to a cheep, ie. SENTINEL

        There are no commas other than those separating data.
        year to second are all just digits.

        For simplicity, we will assume that reply chirps cannot have their own
        replies.

        Note: no docstring examples for functions or methods that do file IO.
        """
        line = f.readline()
        while line:
            arr = line.split(',')
            year = int(arr[2])
            date = datetime(year)
            cheep = cheep()




    def most_popular_cheep(self) -> Optional[Cheep]:
        """Return the cheep with the most replies, or None if there are no
        cheeps.

        >>> c1 = Cheep('UofT', 'Happy back to school!', \
        datetime(2019, 9, 5, 9, 1, 0))
        >>> c2 = Cheep('a_student', 'First CSC148 lecture!', \
        datetime(2019, 9, 9))
        >>> c1.add_reply(c2)
        >>> t3 = Cheep('a_student', 'Weekend!!', datetime(2019, 9, 7))
        >>> chirper = Chirper()
        >>> chirper.post_cheep(c1)
        >>> chirper.post_cheep(c2)
        >>> chirper.post_cheep(t3)
        >>> chirper.most_popular_cheep() == c1
        True
        """
        # TODO: write the body of this method

    def find_fan(self, user: str) -> List[str]:
        """Return a list with the names of the user (user(s) in case of a tie)
        who replies most frequently to <user>'s cheeps, or the empty list if
        there are no cheeps.

        >>> c1 = Cheep('UofT', 'Happy back to school!', \
        datetime(2019, 9, 5, 9, 1, 0))
        >>> c2 = Cheep('a_student', 'First CSC148 lecture!', \
        datetime(2019, 9, 9))
        >>> c1.add_reply(c2)
        >>> c3 = Cheep('a_student', 'Weekend!!', datetime(2019, 9, 7))
        >>> c1.add_reply(c3)
        >>> c4 = Cheep('prof_smith', 'Prepping my lecture', \
        datetime(2019, 9 ,6))
        >>> c1.add_reply(c4)
        >>> chirper = Chirper()
        >>> chirper.post_cheep(c1)
        >>> chirper.post_cheep(c2)
        >>> chirper.post_cheep(c3)
        >>> chirper.post_cheep(c4)
        >>> chirper.find_fan('UofT')
        ['a_student']
        """
        # TODO: write the body of this method


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['__future__', 'datetime', 'typing',
                                   'python_ta', 'doctest']})
