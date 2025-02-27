"""
Project Start Handlers

This module provides handlers for initializing project settings selected by
users. It handles setting up configuration files, README.md, and solution 
templates based on those settings.

Functions:
    Public:
        handle_start: Main entry point for project initialization
    
    Private (internal use only):
        _handle_start_date: Updates project start date in config
        _handle_start_configs: Updates configuration files with environment variables
        _handle_start_readme: Sets up notebook column in README and templates
        _handle_start_solutions: Handles solution file initialization 
        _handle_start_template: Updates project title in files
"""

# Python Standard Library
from datetime import datetime
import json  # pylint: disable=unused-import
import os

# Third-Party Libraries

# Local
from src.config import ConfigManager
from src.utils import HYPHEN
from src.utils import INDEX_START
from src.utils import INDEX_END










def _handle_start_date(
        config: ConfigManager
    ) -> int:
    """
    Update the project start date in configuration file.

    Parameters
    ----------
    config : ConfigManager
        Custom container for validating, storing and retrieving application settings

    Returns
    -------
    int
        1 if update successful
    """
    today = datetime.now().strftime(f'%Y{HYPHEN}%m{HYPHEN}%d')

    with open(f"{config.get('CONFIG_DIR')}/config_proj.py", 'r+', encoding='utf-8') as file:
        lines = file.readlines()

        for i, line in enumerate(lines):

            if line.startswith('PROJ_START='):
                lines[i] = f'PROJ_START=\'{today}\'\n'

        file.seek(0)
        file.writelines(lines)
        file.truncate()

    return 1


def _handle_start_solutions(
        config: ConfigManager
    ) -> int:
    """
    Create solutions directory.

    Ensures there is a directory for storing solution files.

    Parameters
    ----------
    config : ConfigManager
        Custom container for validating, storing and retrieving application settings

    Returns
    -------
    int
        1 if directory creation successful or
        0 if directory creation failed
    """
    solutions_dir = config.get("SOLUTIONS_DIR")

    try:
        if not os.path.exists(solutions_dir):
            os.makedirs(solutions_dir)

        return 1
    except OSError:
        return 0


def _handle_start_configs(
        config: ConfigManager
    ) -> int:
    """
    Update configuration files with user settings.

    Parameters
    ----------
    config : ConfigManager
        Custom container for validating, storing and retrieving application settings

    Returns
    -------
    int
        1 if configuration update successful

    Notes
    -----
    Updates the following config files:
    - config_form.py: Options for Site field in Jupyter IPywidgets form
    - config_index.py: Index table settings in README.md
    - config_proj.py: Project start date and title
    """
    with open(f"{config.get('CONFIG_DIR')}/config_form.py", 'r+', encoding='utf-8') as file:
        lines = file.readlines()

        for i, line in enumerate(lines):

            if line.startswith('SITE_OPTIONS='):
                lines[i] = f"SITE_OPTIONS=\'{config.get('SITE_OPTIONS')}\'\n"

        file.seek(0)
        file.writelines(lines)
        file.truncate()

    with open(f"{config.get('CONFIG_DIR')}/config_index.py", 'r+', encoding='utf-8') as file:
        lines = file.readlines()

        for i, line in enumerate(lines):

            if line.startswith('NB='):
                lines[i] = f"NB={config.get('NB')}\n"

            if line.startswith('NB_NAME='):
                lines[i] = f"NB_NAME=\'{config.get('NB_NAME')}\'\n"

            if line.startswith('SEQ_NOTATION='):
                lines[i] = f"SEQ_NOTATION={config.get('SEQ_NOTATION')}\n"

            if line.startswith('SEQ_SPARSE='):
                lines[i] = f"SEQ_SPARSE={config.get('SEQ_SPARSE')}\n"

        file.seek(0)
        file.writelines(lines)
        file.truncate()

    with open(f"{config.get('CONFIG_DIR')}/config_proj.py", 'r+', encoding='utf-8') as file:
        lines = file.readlines()

        for i, line in enumerate(lines):

            if line.startswith('PROJ_TITLE='):
                lines[i] = f"PROJ_TITLE=\'{config.get('PROJ_TITLE')}\'\n"

        file.seek(0)
        file.writelines(lines)
        file.truncate()


    return 1


def _handle_start_readme(
        config: ConfigManager,
        package_changes: dict
    ) -> int:
    """
    Set up Index table in README.md and solution template files.

    Parameters
    ----------
    config : ConfigManager
        Custom container for validating, storing and retrieving application settings

    Returns
    -------
    int
        1 if notebook initialization successful

    Notes
    -----
    Updates both README.md index table and solution template files
    with the configured notebook column name
    """
    nb_name = config.get('NB_NAME')

    index_header = {
        'labels': f'| Day   | Title   | Solution   | Site   | Difficulty   | {nb_name}   |',
        'sep': f'| ----- | ------- | ---------- | ------ | ------------ | { "-" * (len(nb_name) + 2) } |'
    }

    start_line_readme = None
    end_line_readme = None
    lines_readme = []

    with open('README.md', 'r+', encoding='utf-8') as file:
        lines_readme = file.readlines()

        # HANDLE README CHANGES - TITLE
        if config.get('PROJ_TITLE') in package_changes:
            lines_readme[0] = f'# {config.get("PROJ_TITLE")}\n'

        # HANDLE README CHANGES - NB
        if config.get('NB') in package_changes and config.get('NB_NAME') in package_changes:
            for i in range(len(lines_readme)-1, -1, -1):

                if INDEX_START in lines_readme[i]:
                    start_line_readme = i

                if INDEX_END in lines_readme[i]:
                    end_line_readme = i

            lines_readme[start_line_readme + 1] = f'{index_header["labels"]}\n'
            lines_readme[start_line_readme + 2] = f'{index_header["sep"]}\n'

            for j in range(start_line_readme + 3, end_line_readme):

                lines_readme[j] = ''

            print(f'Extra column selected: {nb_name}')

        file.seek(0)
        file.writelines(lines_readme)
        file.truncate()

    return 1


def _handle_start_template(
        config : ConfigManager,
        package_changes: dict
    ) -> int:
    """
    Update project title and optional sixth column settings in README.md
    and template files.

    Parameters
    ----------
    config : ConfigManager
        Custom container for validating, storing and retrieving application settings

    Returns
    -------
    int
        1 if title update successful
    """
    lines_template = []

    with open(f'{config.get('SOLUTIONS_DIR')}/solution.txt', 'r+', encoding='utf-8') as file:
        lines_template = file.readlines()

        # HANDLE TEMPLATE CHANGES - TITLE
        if config.get('PROJ_TITLE') in package_changes:
            lines_template[0] = f"# {config.get('PROJECT_TITLE')} \\#{{{{ seq_full }}}}\n"

        # HANDLE TEMPLATE CHANGES - NB
        if config.get('NB') in package_changes and config.get('NB_NAME') in package_changes:
            lines_template[29] = f'## {config.get('NB_NAME')}\n'
            lines_template[32] = '\n'

        file.seek(0)
        file.writelines(lines_template)
        file.truncate()


    return 1


def handle_start(
        config: ConfigManager,
        package_changes: dict
    ) -> int:
    """
    Initialize project settings and update configuration files.

    Parameters
    ----------
    config : ConfigManager
        Custom container for validating, storing and retrieving application settings
    package_changes : dict
        Dictionary of configuration changes to apply

    Returns
    -------
    int
        1 if initialization successful

    Notes
    -----
    Main entry point for project setup that coordinates:
    - Setting project start date
    - Updating configuration files
    - Setting up Index table in README.md
    - Configuring template files
    """
    # UPDATE PROJECT START DATE
    _handle_start_date(config)

    # CREATE SOLUTIONS DIRECTORY
    _handle_start_solutions(config)

    if len(package_changes) > 0:
        print(json.dumps(package_changes, indent=4))

        # UPDATE CONFIG FILES
        _handle_start_configs(config)

        if config.get('PROJ_TITLE') in package_changes or config.get('NB') in package_changes:
            # UPDATE README
            _handle_start_readme(config, package_changes)

            # UPDATE TEMPLATE FILE
            _handle_start_template(config, package_changes)

    return 1
