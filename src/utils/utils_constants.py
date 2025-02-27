"""
Global Constants

This module defines constant values used throughout the application.
These values are intended to be immutable and context-independent.

Constants
---------
HYPHEN : str
    Unicode non-breaking hyphen character for dates
INDEX_START : str
    Markdown comment marking the start of Index table section in README.md
INDEX_END : str
    Markdown comment marking the end of Index table section in README.md
FIRST_ROW : str
    Header row of Index table section in README.md
SECOND_ROW : str
    Separator row of Index table section in README.md
"""










HYPHEN = "\u2011" # Non-breaking hyphen
INDEX_START = '<!-- Index Start - WARNING: Do not delete or modify this markdown comment. -->'
INDEX_END = '<!-- Index End - WARNING: Do not delete or modify this markdown comment. -->'
FIRST_ROW = '| Day   | Title   | Solution   | Site   | Difficulty   |'
SECOND_ROW = '| ----- | ------- | ---------- | ------ | ------------ |'
