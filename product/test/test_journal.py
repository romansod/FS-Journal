# test_journal.py
import unittest
import re
import sys
import os

# Ensure the parent directory is in the system path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import target file for testing
from journal_types.journal import *


def createXLengthStr_a(length: int) -> str:
    name = ''
    for _ in range(length):
        name += 'a'
    
    return name

class Test(unittest.TestCase):
    def test_create_journal_neg(self):
        # 1) Empty Name
        name = ''
        self.assertRaises(ValueError, Journal, name)

        # 2) Too long
        name = createXLengthStr_a(MAX_NAME_WIDTH) + 'a'

        self.assertRaises(ValueError, Journal, name)

        # File or directory must exist
        # TODO check if file or directory exists

    def test_create_journal_pos(self):
        # 1) Max length
        name = createXLengthStr_a(MAX_NAME_WIDTH)        
        # 2) Initialized Successfully
        t_journal = Journal(name)
        self.assertEqual(name, t_journal.journal_name)
        self.assertEqual('', t_journal.description)
        self.assertEqual('', t_journal.additional_notes)

    def test_fprint_name(self):
        # 1) Normal name
        name = 'Lord of the Fries'
        t_journal = Journal(name)
        self.assertEqual(
            '### Lord of the Fries #########################################################', 
            t_journal.fprint_name())

        # 2) Max length
        name = createXLengthStr_a(MAX_NAME_WIDTH)
        t_journal = Journal(name)
        self.assertEqual('### ' + name, t_journal.fprint_name())

        # 3) Max length - 1 with a space printed at end
        name = createXLengthStr_a(MAX_NAME_WIDTH - 1)
        t_journal = Journal(name)
        self.assertEqual('### ' + name + ' ', t_journal.fprint_name())

        # 4) Max length - 2 with a space and one hash
        name = createXLengthStr_a(MAX_NAME_WIDTH - 2)
        t_journal = Journal(name)
        self.assertEqual('### ' + name + ' #', t_journal.fprint_name())
    
    def test_fprint_desc(self):
        name = 'Lord of the Fries'
        t_journal = Journal(name)

        # 1) Empty description
        desc = ''
        t_journal.setDescription(desc)
        self.assertEqual('Description:\n', t_journal.fprint_desc())
        
        # 2) Normal description
        desc = 'Book by George Dorwell'
        t_journal.setDescription(desc)
        self.assertEqual('Description:\n' + desc, t_journal.fprint_desc())

        # 3) One newline added because of length
        desc = createXLengthStr_a(MAX_WIDTH) + createXLengthStr_a(MAX_WIDTH)
        t_journal.setDescription(desc)
        self.assertEqual(
            'Description:\n' \
                + createXLengthStr_a(MAX_WIDTH) + '\n' \
                + createXLengthStr_a(MAX_WIDTH),
            t_journal.fprint_desc())
        
        # 4) Three newlines added because of length
        desc = createXLengthStr_a(MAX_WIDTH) \
            + createXLengthStr_a(MAX_WIDTH) \
            + createXLengthStr_a(MAX_WIDTH)
        
        t_journal.setDescription(desc)
        self.assertEqual(
            'Description:\n' \
                + createXLengthStr_a(MAX_WIDTH) + '\n' \
                + createXLengthStr_a(MAX_WIDTH) + '\n' \
                + createXLengthStr_a(MAX_WIDTH),
            t_journal.fprint_desc())

    def test_fprint_note(self):
        name = 'Lord of the Fries'
        t_journal = Journal(name)

        # 1) Empty note
        note = ''
        t_journal.appendToNotes(note)
        self.assertEqual('Additional Notes:\n', t_journal.fprint_note())

        # 2) Max length for note
        note = createXLengthStr_a(MAX_NOTE_WIDTH)
        t_journal.appendToNotes(note)
        # Remove datetime printed since it is non-deterministic
        #   Additional Notes:\n[datetime]\naaaaaaa...aaaa
        jnotes = re.split('\[|\]', t_journal.fprint_note())
        # Join the first and last element. Cut out the datetime.
        # Then trim the newline from the note itself
        #   [Additional Notes:\n], [datetime], [\naaaaaaa...aaaa]
        jnotes_without_dt = jnotes[0] + jnotes[2][1:]
        # Now deterministic format for test comparison
        #   Additional Notes:\naaaaaaa...aaaa

        self.assertEqual('Additional Notes:\n' + note, jnotes_without_dt)


if __name__ == "__main__":
    unittest.main()
        