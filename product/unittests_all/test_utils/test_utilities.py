"""
Utility functions for use during unit tests
"""
import re

DATETIME_PLACEHOLDER = 'yyyy-mm-dd hh:mm:ss.msssss'

def create_x_length_str_a(length: int) -> str:
    """
    Create a string of 'a' characters repeated based on parameter.

    length -- number of 'a' characters in returned string
    """
    name = ''
    for _ in range(length):
        name += 'a'

    return name

def clean_dt(output_with_dt: str) -> str:
    """
    Clean datetime patterns by replacing them with special string for testing
    DATETIME_PLACEHOLDER = [yyyy-mm-dd hh:mm:ss.msssss]
    """
    datetime_pattern = r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+\]'
    return re.sub(
        datetime_pattern,
        '[' + DATETIME_PLACEHOLDER + ']',
        output_with_dt)