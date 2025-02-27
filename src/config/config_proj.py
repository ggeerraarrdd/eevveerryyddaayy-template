# #########################################################################
#
# WARNING: DO NOT MODIFY THIS CONFIG FILE.
#
# Manual modifications can cause unintended behavior.
# The system will manage this file automatically.
#
# #########################################################################





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
PROJ_START='2025‑02‑26'





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
