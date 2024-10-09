"""
journal.py
"""
from datetime import datetime

# Constants
MAX_WIDTH = 79
MAX_NAME_WIDTH = MAX_WIDTH - 4
MAX_DESC_LEN = MAX_WIDTH * 10
MAX_NOTE_WIDTH = MAX_WIDTH - 4

# Exceptions
E_NAME_NOT_VALID = 'Name "{}" is not a valid name'
E_NAME_EXCEEDS_MAX = 'Name of length {} exceeds max length {}'

class Journal:
    """
    Base object for journal entries
    """
    def __init__(self, name: str):
        self.check_name(name)

        self.journal_name = name
        self.description = ''
        self.additional_notes = ''

    def check_name(self, name: str):
        """
        Validate the name against constraints:
        1) Must be non empty
        2) Must be less than the MAX_NAME_WIDTH
        """
        name_len = len(name)

        if name_len == 0:
            raise ValueError(E_NAME_NOT_VALID.format(name))

        if name_len > MAX_NAME_WIDTH:
            raise ValueError(E_NAME_EXCEEDS_MAX.format(name_len, MAX_NAME_WIDTH))

        # Check file or directory name exists

    def __insert_width_newline(self, s: str):
        """
        Helper function to enforce MAX_WIDTH in output and
        returns formatted string

        s -- string to format to MAX_WIDTH by inserting newlines
        """
        formatted_str = ''
        for i, letter in enumerate(s):
            if i % MAX_WIDTH == 0:
                formatted_str += '\n  '
            formatted_str += letter

        if len(formatted_str) == 0:
            return formatted_str

        # first character would have inserted a newline, skip it
        return formatted_str[1:]

    def set_description(self, desc: str):
        """
        Sets/Overrides description of this object and enforces MAX_WIDTH.
        
        desc -- description (must be less than MAX_DESC_LEN)
        """
        self.description = self.__insert_width_newline(desc)

    def append_notes(self, note: str):
        """
        Appends incoming note to the existing notes with a datetime timestamp.
        
        note -- string to append (must be less than MAX_WIDTH)

        Ex:
                'Hello World' 
            
            ...becomes...
                
                '  [datetime]
                     Hello World'
        """
        new_note = '' if len(self.additional_notes) == 0 else '\n'

        if len(note) > 0:
            new_note += \
                '  [' + str(datetime.now()) + ']\n    ' + self.__insert_width_newline(note)
        
        self.additional_notes += new_note

    def fprint_name(self) -> str:
        """
        Format string with name as a title of length MAX_WIDTH.
        
        Ex:
            ### MyName ######...
        """
        left_title = '### ' + self.journal_name

        if len(left_title) < MAX_WIDTH:
            left_title += ' '

        return left_title.ljust(MAX_WIDTH, '#')

    def fprint_desc(self) -> str:
        """
        Format string with description as a paragraph.

        Ex:
            Description:
            My description goes here...
        """
        return 'Description:\n' + self.description

    def fprint_note(self) -> str:
        """
        Format string with notes as a list of entries where each line is 
        less than the MAX_WIDTH.
        
        Ex:
            Additional Notes:
            [datetime1]
            The earliest note
            [datetime2]
            The second earliest note
            ...
            [datetimeN]
            The most recent note
        """
        return 'Additional Notes:\n' + self.additional_notes

    def fprint(self) -> str:
        """
        Format the entire Journal object for printing.

        Ex:
            ### MyJournal #################
            Description:
            This is the description of obj
            Additional Notes:
            [datetime1]
            First note added
            [datetime2]
            Second note added
        """
        formatted_s = ''

        formatted_s += self.fprint_name() + '\n'
        formatted_s += self.fprint_desc() + '\n'
        formatted_s += self.fprint_note()

        return formatted_s
    