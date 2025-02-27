# #########################################################################
#
# WARNING: DO NOT MODIFY THIS CONFIG FILE.
#
# Manual modifications can cause unintended behavior.
# The system will manage this file automatically.
#
# #########################################################################





"""
Index Table: Optional Extra Column
===========================================================================

Adds an optional sixth column to the Index table for additional 
notes and annotations.

Parameters
----------
NB : int
    Controls visibility of the sixth column in Index table.
    Values:
        0: Disable sixth column display (default)
        1: Enable sixth column display

NB_NAME : str
    The header title for the sixth column when enabled.
    Only relevant when NB=1.
    Default: 'NB'

Example:
    NB=0 keeps number of columns to five.
    NB=1, NB_NAME='Notes' creates a sixth column titled 'Notes'
"""
NB=0
NB_NAME='NB'





"""
Index Table: Sequential Numbering Format for First Column ('Day')
===========================================================================

This setting determines how the values in the first column ('Day') of the
Index table are formatted.

Parameters
----------
SEQ_NOTATION : int
    Values:
        0: Three-digit zero-padded number (e.g., '001', '002')
        1: Full ISO date format with non-breaking hyphens U+2011 (e.g., '2001‑01‑01')
    Default: 0

Notes:
    1. The chosen format affects all 'Day' values throughout the sequence. 
    2. Three-digit format (0) is more compact but date format (1) provides 
       more temporal context. 
    3. When using format 1, dates use Unicode non-breaking hyphens (U+2011).
"""
SEQ_NOTATION=0





"""
Index Table: Sequential Numbering Gaps for First Column ('Day')
===========================================================================

This setting determines how the system handles 'Day' values that are 
missing from the sequence numbering.

Parameters
----------
SEQ_SPARSE : int
    Values:
        0: Continuous rows but non-continuous sequence - skips missing days
        1: All days in sequence shown - blank entries for missed days
    Default: 0
        
Example:
    For three-digit format (SEQ_NOTATION=0):
    If SEQ_SPARSE=0: Missing a day shows as gap in sequence
        Row 1: 001
        Row 2: 003 (sequence skips 002)
    If SEQ_SPARSE=1: Missing day included with blank data
        Row 1: 001 
        Row 2: 002 [not skipped but other columns blank]
        Row 3: 003 
    
    For date format (SEQ_NOTATION=1):
    If SEQ_SPARSE=0: Missing a day shows as gap in sequence
        Row 1: 2025‑01‑01
        Row 2: 2025‑01‑03 (skips 2025‑01‑02)
    If SEQ_SPARSE=1: Missing day included with blank data
        Row 1: 2025‑01‑01 
        Row 2: 2025‑01‑02 [not skipped but other columns blank]
        Row 3: 2025‑01‑03 

Notes:
    Setting SEQ_SPARSE=1 helps with accountability by making missed days 
    visible in the sequence, rather than hiding gaps.
"""
SEQ_SPARSE=0





"""
Index Table: Column Widths
===========================================================================

WARNING: DO NOT MODIFY THIS FILE. Manual modifications may cause 
unintended behavior. The system will manage this file
automatically.

This configuration file defines the markdown widths of the columns in the
Index table of README.

Column Descriptions:
    day (int): Width of "Day" column
    title (int): Width of "Title" column
    solution (int): Width of "Solution" column
    site (int): Width of "Site" column
    difficulty (int): Width of "Difficulty" column
    nb (int): Width of optional sixth column

COLS_WIDTH_DEFAULT = {
    'day': 5,
    'title': 7,
    'solution': 10,
    'site': 6,
    'difficulty': 12,
    'nb': 1
}

Notes:
    These settings only affect the underlying markdown formatting of the
    Index table, not its visual appearance in the rendered README file.
"""
COLS_WIDTH = {
    'day': 5,
    'title': 7,
    'solution': 10,
    'site': 6,
    'difficulty': 12,
    'nb': 1
}
