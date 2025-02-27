"""
Handler Functions Module

This module provides core functions for project management including
initialization, operations, and configuration updates. These functions handle
the business logic and processes for:

1. Project initialization: Setting up initial configuration, templates, and file structure
2. Normal operations: Running daily project tasks and updates
3. Settings management: Updating project configurations and preferences

Components
----------
Functions:
    handle_runs:
        Manages execution of project operations during normal usage
    handle_start:
        Controls initial project setup and configuration

The handler functions act as entry points for key application processes,
coordinating between UI inputs, configuration management, and project resources.
"""

from .handle_runs import handle_runs
from .handle_start import handle_start


__all__ = [
    'handle_runs',
    'handle_start'
]
