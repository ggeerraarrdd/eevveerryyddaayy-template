"""
Utility Functions for Validating Project State
"""

# Python Standard Library
import os

# Local
from src.config import ConfigManager










def validate_project() -> bool:
    """
    Validate project is initalized or not.

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

    is_initilized = None

    is_solutions = bool(config.get('SOLUTIONS_DIR'))
    is_solutions_files = len(os.listdir(config.get('SOLUTIONS_DIR'))) == 0
    is_seq_date = bool(config.get('PROJ_START'))

    if not is_seq_date and not is_solutions and not is_solutions_files:
        is_initilized = False

    elif not is_seq_date and not is_solutions:
        is_initilized = False

    elif not is_seq_date:
        is_initilized = False

    elif is_seq_date and is_solutions and is_solutions_files:
        is_initilized = True

    elif is_seq_date and is_solutions:
        is_initilized = True

    elif is_seq_date:
        is_initilized = True

    else:
        raise ValueError('Invalid project state: TBD')


    return is_initilized
