"""
Form Interfaces for Jupyter Notebooks

This module provides reusable form components for data entry in Jupyter 
notebooks. It includes functions to generate interactive forms using 
ipywidgets.

Functions:
    create_start_form
        Builds interactive form for initializing project configurations
        selected by user
        [Not yet implemented]
        
    create_entry_form
        Builds interactive form to process new entries with validation 
        and submission handling
        
    create_update_form
        Builds a configuration management form for updating project
        settings and parameters after initialization
        [Not yet implemented]
"""

from .form_entry import create_entry_form


__all__ = ['create_entry_form']
