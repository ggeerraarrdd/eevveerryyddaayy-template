"""
Utility Functions Module

This module provides a collection of utility functions and components to support 
core application operations. It exports constants, data management tools, and helper 
functions that handle various aspects of application workflow.

Components
----------
Constants:
    HYPHEN, INDEX_START, INDEX_END, FIRST_ROW, SECOND_ROW: 
        String constants used throughout the application for formatting and parsing

Classes:
    PackageManager:
        Handles dictionary-based data storage and manipulation for form inputs and derived values

Functions:
    clean_strings:
        Normalizes and sanitizes string inputs
    get_files_created:
        Generates solution files from template
    get_target_line_dict:
        Converts string to dictionary for downstream processing
    get_target_line_updated:
        Functions for locating and updating specific lines in Index table in README.md
    validate_project:
        Checks whether the project has been properly initialized

These utilities form the foundation for higher-level operations handled by the application's
main modules and handlers.
"""

from .utils_constants import HYPHEN
from .utils_constants import INDEX_START
from .utils_constants import INDEX_END
from .utils_constants import FIRST_ROW
from .utils_constants import SECOND_ROW
from .utils_package import PackageManager
from .utils_runs import clean_strings
from .utils_runs import get_files_created
from .utils_runs import get_target_line_dict
from .utils_runs import get_target_line_updated
from .utils_validation import validate_project


__all__ = [
    'HYPHEN',
    'INDEX_START',
    'INDEX_END',
    'FIRST_ROW',
    'SECOND_ROW',
    'PackageManager',
    'clean_strings',
    'get_files_created',
    'get_target_line_dict',
    'get_target_line_updated',
    'validate_project'
]
