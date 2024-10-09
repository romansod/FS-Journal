"""
test_journal.py

Unit tests for journal_type/*
"""
import unittest
import sys
import os

# Ensure the parent directory is in the system path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#pylint: disable=wrong-import-position
# Testing utilities
from test_utils.test_utilities import DATETIME_PLACEHOLDER
from test_utils.test_utilities import create_x_length_str_a
from test_utils.test_utilities import clean_dt
# Target file for testing
from journal_types.journal import MAX_WIDTH
from journal_types.journal import MAX_NAME_WIDTH
from journal_types.journal import MAX_NOTE_WIDTH
from journal_types.journal import Journal
#pylint: enable=wrong-import-position

class Test(unittest.TestCase):
    """
    Unit tests for journal_type/*

    test_create_journal_neg
    test_create_journal_pos
    test_fprint_name
    test_fprint_desc
    test_fprint_note
    """
    def test_create_journal_neg(self):
        """
        Test constructor of journal object (neg)

        1) Empty Name
        2) Too long

        """
        # 1) Empty Name
        name = ''
        self.assertRaises(ValueError, Journal, name)

        # 2) Too long
        name = create_x_length_str_a(MAX_NAME_WIDTH) + 'a'

        self.assertRaises(ValueError, Journal, name)

        # File or directory must exist:
        # check if file or directory exists

    def test_create_journal_pos(self):
        """
        Test constructor of journal object (pos)

        1) Max length
        2) Initialized Successfully

        """
        # 1) Max length
        name = create_x_length_str_a(MAX_NAME_WIDTH)
        # 2) Initialized Successfully
        t_journal = Journal(name)
        self.assertEqual(name, t_journal.journal_name)
        self.assertEqual('', t_journal.description)
        self.assertEqual('', t_journal.additional_notes)

    def test_fprint_name(self):
        """
        Test the printing of name

        1) Normal name
        2) Max length
        3) Max length -1 with a space printed at end
        4) Max length -2 with a space and one #

        """
        # 1) Normal name
        name = 'Lord of the Fries'
        t_journal = Journal(name)
        self.assertEqual(
            '### Lord of the Fries #########################################################', 
            t_journal.fprint_name())

        # 2) Max length
        name = create_x_length_str_a(MAX_NAME_WIDTH)
        t_journal = Journal(name)
        self.assertEqual('### ' + name, t_journal.fprint_name())

        # 3) Max length - 1 with a space printed at end
        name = create_x_length_str_a(MAX_NAME_WIDTH - 1)
        t_journal = Journal(name)
        self.assertEqual('### ' + name + ' ', t_journal.fprint_name())

        # 4) Max length - 2 with a space and one hash
        name = create_x_length_str_a(MAX_NAME_WIDTH - 2)
        t_journal = Journal(name)
        self.assertEqual('### ' + name + ' #', t_journal.fprint_name())

    def test_fprint_desc(self):
        """
        Test the printing of description

        1) Empty description
        2) Normal description
        3) One newline added because of length
        4) Three newlines added because of length

        """
        name = 'Lord of the Fries'
        t_journal = Journal(name)

        # 1) Empty description
        desc = ''
        t_journal.set_description(desc)
        self.assertEqual('Description:\n', t_journal.fprint_desc())

        # 2) Normal description
        desc = 'Book by George Dorwell'
        t_journal.set_description(desc)
        self.assertEqual('Description:\n  ' + desc, t_journal.fprint_desc())

        # 3) One newline added because of length
        desc = create_x_length_str_a(MAX_WIDTH) + create_x_length_str_a(MAX_WIDTH)
        t_journal.set_description(desc)
        self.assertEqual(
            'Description:\n  ' \
                + create_x_length_str_a(MAX_WIDTH) + '\n  ' \
                + create_x_length_str_a(MAX_WIDTH),
            t_journal.fprint_desc())

        # 4) Three newlines added because of length
        desc = create_x_length_str_a(MAX_WIDTH) \
            + create_x_length_str_a(MAX_WIDTH) \
            + create_x_length_str_a(MAX_WIDTH)

        t_journal.set_description(desc)
        self.assertEqual(
            'Description:\n  ' \
                + create_x_length_str_a(MAX_WIDTH) + '\n  ' \
                + create_x_length_str_a(MAX_WIDTH) + '\n  ' \
                + create_x_length_str_a(MAX_WIDTH),
            t_journal.fprint_desc())

    def test_fprint_note(self):
        """
        Test the printing of additional notes

        1) Empty note
        2) Max length for note

        """
        name = 'Lord of the Fries'
        t_journal = Journal(name)

        # 1) Empty note
        note = ''
        t_journal.append_notes(note)
        self.assertEqual('Additional Notes:\n', t_journal.fprint_note())

        # 2) Max length for note
        note = create_x_length_str_a(MAX_NOTE_WIDTH)
        t_journal.append_notes(note)
        self.assertEqual(
            'Additional Notes:\n'
            + '  [' + DATETIME_PLACEHOLDER + ']\n'
            + '      ' + note,
            clean_dt(t_journal.fprint_note()))

    def test_fprint(self):
        """
        Test all the print functions together
        """
        name = 'Lord of the Fries'
        t_journal = Journal(name)
        t_journal.set_description('A movie about human nature and potatoes')
        t_journal.append_notes('Parody of another movie')
        t_journal.append_notes('No sequel planned')

        self.assertEqual(
            '### Lord of the Fries #########################################################\n'
            + 'Description:\n'
            + '  A movie about human nature and potatoes\n'
            + 'Additional Notes:\n'
            + '  [' + DATETIME_PLACEHOLDER + ']\n'
            + '      Parody of another movie\n'
            + '  [' + DATETIME_PLACEHOLDER + ']\n'
            + '      No sequel planned',
            clean_dt(t_journal.fprint()))

if __name__ == "__main__":
    unittest.main()
        