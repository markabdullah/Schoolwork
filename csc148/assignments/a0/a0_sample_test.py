"""CSC148 Assignment 0: Sample tests

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Assignment 0.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.

Note: this file is to only help you; you will not submit it when you hand in
the assignment.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from datetime import datetime
from io import StringIO
from chirper import Cheep, Chirper

# Contents of a file with two cheeps
# We will use it with StringIO to test file reading methods.
# StringIO allows us to pass an open file within a Python module.
# You can use it in your own testing, but you do not have to.
SHORT_FILE_CONTENTS = 'UofTArtSci,RT @UofT: #UofTGrad18 Fall Convocation ' + \
                      'starts today! Class of 2018_ This Is Your Moment.,' + \
                      '2018,11,05,13,57,41' + '\n' + \
                      'UofTCompSci,Congratulations to all our fall ' + \
                      'graduates!,2018,11,06,20,24,05' + '\nEND_REPLIES'


def test_cheep_attributes() -> None:
    """Test the public attributes of a new cheep."""
    before = datetime.today()
    c = Cheep('a_user', 'I love cats')
    after = datetime.today()
    assert c.user == 'a_user'
    assert before < c.date < after


def test_cheep_one_reply_get_repliers() -> None:
    """Test Cheep.get_repliers for a cheep with a single reply."""
    c = Cheep('a_user', 'I love cats')
    c2 = Cheep('another_user', 'me too!!!')
    assert c.add_reply(c2) is None
    assert c.get_repliers() == ['another_user']


def test_cheep_one_reply_to_str() -> None:
    """Test the string representation of a cheep with a single reply."""
    usr1, text1 = 'a_user', 'I love cats'
    usr2, text2 = 'another_user', 'me too!!!'
    c = Cheep(usr1, text1)
    c2 = Cheep(usr2, text2)
    c.add_reply(c2)
    assert str(c) == '{0} said: {1}\n{2} replied: {3}'.format(usr1, text1,
                                                              usr2, text2)


def test_cheep_contains_not_in_text() -> None:
    """Test Cheep.__contains__ with search keyword not in the text."""
    c = Cheep('a_user', 'I love cats')
    assert 'dogs' not in c


def test_one_cheep_most_popular() -> None:
    """Test Chirper.most_popular on a single cheep."""
    chirper = Chirper()
    c = Cheep('a_user', 'I love cats')
    chirper.post_cheep(c)
    assert chirper.most_popular_cheep() == c


def test_short_file_find_fan() -> None:
    """Test Chirper.find_fan on SHORT_FILE_CONTENTS."""
    chirper = Chirper()
    chirper.read_cheeps(StringIO(SHORT_FILE_CONTENTS))
    assert chirper.find_fan('UofTArtSci') == ['UofTCompSci']


if __name__ == '__main__':
    import pytest
    pytest.main(['a0_sample_test.py'])
