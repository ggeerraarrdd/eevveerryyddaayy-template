"""
EEVVEERRYYDDAAYY Project

Main program file that coordinates core functionality for configuring settings, 
managing field values from Jupyter IPyWidgets forms, and handling program flow. 
This file serves as the central coordinator for:

- Initializing and configuring project settings selected by the user
- Setting up Index table structure and template files
- Processing and validating new form entries
- Managing project files and reference index
- Coordinating data flow between notebook interface and storage

This module acts as the interface between user-facing forms and the underlying
application logic, routing inputs to appropriate handlers.
"""

# Python Standard Library
from datetime import datetime
from typing import Any, Dict, List, Tuple, Union
import json

# Third-Party Libraries
import ipywidgets as widgets

# Local
from .config import ConfigManager
from .forms import create_entry_form
from .handlers import handle_start
from .handlers import handle_runs
from .utils import PackageManager
from .utils import validate_project










def start_project(package: Dict[str, Tuple[type, Any]]) -> int:
    """
    Initialize the project.
    
    Sets up necessary user configurations including directories, templates,
    and initial settings based on form inputs.
    
    Parameters
    ----------
    package : Dict[str, Tuple[type, Any]]
        Dictionary containing configuration settings from the start form
        with type information and values
        
    Returns
    -------
    int
        Status code: 1 for success, 0 for failure
    """
    config = ConfigManager()

    package_changes = config.load_settings_from_form(package)

    handle_start(config, package_changes)

    print('Project initialized')


    return 1


def update_project(package):
    """
    TD
    """
    config = ConfigManager()

    config_all = config.get_all()

    print(json.dumps(config_all, indent=4))
    print(package)

    return 1


def add_project() -> widgets.VBox:
    """
    Create entry form for adding new items to the project.
    
    Generates and returns a form interface with fields based on 
    current project configuration.
    
    Returns
    -------
    widgets.VBox
        IPyWidgets form widget for data entry
    """
    config = ConfigManager()

    form_entry = create_entry_form(config)

    return form_entry


def run_project(package: PackageManager, data: List[Any]) -> int:
    """
    Process new entry data and update project resources.
    
    Takes data from completed form, passes it to handlers for
    processing, and updates relevant project files.
    
    Parameters
    ----------
    package : PackageManager
        Custom container for storing and retrieving form data and derived values
    data : List[Any]
        List of form input values
        
    Returns
    -------
    int
        Status code: 1 for success, 0 for failure
    """
    config = ConfigManager()

    today = datetime.now()

    handle_runs(config, package, data[0], today)

    return 1


def eevveerryyddaayy(*args: Any, **kwargs: Any) -> Union[int, Any]:
    """
    Main entry point that routes form inputs to appropriate handlers.
    
    This function serves as the primary interface between notebook forms
    and the application logic. It determines which action to take based
    on the source parameter and validates project state before proceeding.
    
    Parameters
    ----------
    *args : Any
        Variable positional arguments from form inputs
    **kwargs : Any
        Keyword arguments including 'source' which determines routing:
            0: Initialize project configurations
            1: Update project configurations
            2: Create Jupyter IpyWidgets forms
            3: Process entry submission
            
    Returns
    -------
    Union[int, Any]
        Status code (int) or form widget (for source=2)
        1 for success, 0 for failure or error condition
    """
    is_initialized = validate_project()

    # from IPython import get_ipython
    # ip = get_ipython()
    # path = None
    # if '__vsc_ipynb_file__' in ip.user_ns:
    #     path = ip.user_ns['__vsc_ipynb_file__']
    # print(path)

    if (kwargs['source'] == 0) or (kwargs['source'] == 1):

        package = {
            'PROJ_TITLE': (str, args[0]),
            'NB': (int, args[1]),
            'NB_NAME': (str, args[2]),
            'SEQ_NOTATION': (int, args[3]),
            'SEQ_SPARSE': (int, args[4]),
            'SITE_OPTIONS': (list, args[5])
        }

        if kwargs['source'] == 0:

            # START FORM - every_start.ipynb
            if is_initialized:
                print('Project is already initialized.')
                print('Use every_update.ipynb to update project settings.')
                print('Use every_entry.ipynb to create a project entry.')
                return 0

            print('Initializing project...')
            start_project(package)
            print('Done')
            return 1

        if kwargs['source'] == 1:
            # UPDATE FORM - every_update.ipynb
            # if is_initialized:
            #     print('Updating project settings...')
            #
            # print('Project is not initialized.')
            # print('Use every_start.ipynb to initialize project.')
            # return 0

            print('Not yet implemented')
            return 0

    elif kwargs['source'] == 2:
        # ENTRY FORM - every_entry.ipynb
        if is_initialized:
            return add_project()

        print('The project is not initialized.')
        print('Use every_start.ipynb to initialize project.')
        return 0

    elif kwargs['source'] == 3:
        # ENTRY FORM - every_entry.ipynb - button clicked
        package = PackageManager()
        run_project(package, args)
        package.reset()
        return 1

    else:
        print('Invalid source')
        return 0


    return 0
