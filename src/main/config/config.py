# #########################################################################
#
# WARNING: DO NOT MODIFY THIS CONFIG FILE.
#
# Manual modifications may cause unintended behavior.
# The system will manage this file automatically.
#
# #########################################################################





"""
Project: Title
===========================================================================

Sets the project title that will be used in generated files.

Parameters
----------
PROJ_TITLE : str
    The name of the project to be used in file headers and templates.
    Default: '[ ] Everyday'

Example:
    'SQL Everyday'

Notes:
    The title will be consistently used across all generated files
"""
PROJ_TITLE='[ ] Everyday'





"""
Project: Start Date
===========================================================================

Controls initialization behavior through start date setting.

Parameters
----------
SEQ_START : str
    Values:
        '' : Empty string - enables initialization on first run
        'YYYY‑MM‑DD' : Specific date - prevents initialization
                       (uses U+2011 non-breaking hyphen)
    Default: '' (empty string)

Example:
    '2025‑01‑01' # Note: Uses non-breaking hyphens

Notes:
    When set to empty string, initialization will occur on first run
    and SEQ_START will be set to that date. Once set, initialization
    will not occur again.
"""
SEQ_START=''





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
Locations of Critical Directories
===========================================================================

Controls the paths to critical directories.

Parameters
----------
SOLUTIONS_DIR : str
    Relative path to the directory containing solution files
    Default: 'solutions'
CONFIG_DIR : str
    Relative path to the configuration files directory
    Default: 'src/main/config'
TEMPLATES_DIR : str
    Relative path to the templates directory
    Default: 'src/main/templates' 
"""
SOLUTIONS_DIR='solutions'
CONFIG_DIR='src/main/config'
TEMPLATES_DIR='src/main/templates'
