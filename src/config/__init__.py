"""
Configuration Module

This module centralizes configuration management for the application, providing
access to settings, paths, and project parameters. It serves as a single entry
point for all configuration needs across the application.

Components
----------
ConfigManager : class
    A class responsible for managing dictionary-based configuration settings
    and providing controlled access to configuration values.

Configuration Variables:
    Index Table Settings:
        NB : int
            Flag indicating whether notebook feature is enabled
        NB_NAME : str
            Display name for notebook column in the index
        SEQ_NOTATION : str
            Format notation for sequence identifiers
        SEQ_SPARSE : int
            Flag for sparse sequence numbering
        COLS_WIDTH : dict
            Width settings for Index table columns

    Path Settings:
        SOLUTIONS_DIR : str
            Directory path for solution files
        CONFIG_DIR : str
            Directory path for configuration files
        TEMPLATES_DIR : str
            Directory path for template files

    Project Settings:
        PROJ_START : str
            Project start date
        PROJ_TITLE : str
            Project title

This module consolidates imports from various configuration submodules to
provide a streamlined interface for accessing all configuration components.
"""

from .config_manager import ConfigManager
from .config_index import NB
from .config_index import NB_NAME
from .config_index import SEQ_NOTATION
from .config_index import SEQ_SPARSE
from .config_index import COLS_WIDTH
from .config_paths import SOLUTIONS_DIR
from .config_paths import CONFIG_DIR
from .config_paths import TEMPLATES_DIR
from .config_proj import PROJ_START
from .config_proj import PROJ_TITLE


__all__ = [
    'ConfigManager',
    'NB',
    'NB_NAME',
    'SEQ_NOTATION',
    'SEQ_SPARSE',
    'COLS_WIDTH',
    'SOLUTIONS_DIR',
    'CONFIG_DIR',
    'TEMPLATES_DIR',
    'PROJ_START',
    'PROJ_TITLE'
]
