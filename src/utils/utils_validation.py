"""
Utility Functions for Validating Project State
"""

# Python Standard Library
import os

# Local
from src.config import ConfigManager










def validate_project() -> bool:
    """
    Validate project is initialized or not.

    Parameters
    ----------
        None

    Returns
    -------
        bool
            True if this is first run (no files and no SEQ_START value), 
            False if regular run (files exist and SEQ_START set),

    Raises
    ------
        ValueError
            If project is in an invalid state regarding files and SEQ_START
    
    Prerequisites
    -------------
    - Config directory must exist
    - Solutions directory must be accessible, if exists
    """
    config = ConfigManager()

    is_initialized = None

    is_solutions = bool(config.get('SOLUTIONS_DIR'))
    is_solutions_files = len(os.listdir(config.get('SOLUTIONS_DIR'))) == 0
    is_seq_date = bool(config.get('PROJ_START'))

    if not is_seq_date and not is_solutions and not is_solutions_files:
        is_initialized = False

    elif not is_seq_date and not is_solutions:
        is_initialized = False

    elif not is_seq_date:
        is_initialized = False

    elif is_seq_date and is_solutions and is_solutions_files:
        is_initialized = True

    elif is_seq_date and is_solutions:
        is_initialized = True

    elif is_seq_date:
        is_initialized = True

    else:
        raise ValueError('Invalid project state: TBD')


    return is_initialized
