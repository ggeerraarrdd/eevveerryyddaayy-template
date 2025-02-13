"""
EEVVEERRYYDDAAYY Project

Main program file that coordinates core functionality for configuring settings, 
managing form field values, and handling program flow. This file serves as 
the central coordinator for:

- Initializing and configuring project settings from environment variables
- Setting up Index table structure and template files
- Processing and validating new form entries
- Managing project files and reference indices
- Configuring first-time setup and user settings
- Coordinating data flow between notebook interface and storage
"""


# Python Standard Library
from datetime import datetime
import json
import os
import re

# Local
from .config import PROJ_TITLE
from .config import NB
from .config import NB_NAME
from .config import SEQ_NOTATION
from .config import SOLUTIONS_DIR
from .config import CONFIG_DIR
from .config import TEMPLATES_DIR
from .helpers import clean_strings
from .helpers import get_files_created
from .helpers import get_target_line_dict
from .helpers import get_target_line_updated
from .helpers import PackageHandler


# Non-breaking hyphen
HYPHEN = "\u2011"

INDEX_START = '<!-- Index Start - WARNING: Do not delete or modify this markdown comment. -->'
INDEX_END = '<!-- Index End - WARNING: Do not delete or modify this markdown comment. -->'










def validate_runs(handler: PackageHandler) -> bool:
    """
    Validates if this is the first run or a regular run of the project.

    Args:
        handler (PackageHandler): Package handler instance containing configuration

    Returns:
        bool: True if this is first run (no files and no SEQ_START value),
              False if regular run (files exist and SEQ_START set),

    Raises:
        ValueError: If project is in an invalid state regarding files and SEQ_START

    Side Effects:
        - Creates Solution directory if missing
    
    Prerequisites:
        - Config directory must exist
        - Solutions directory must be accessible, if exists
    """
    seq_start_loc = handler.get_value('config_base', 'seq_start_loc')

    # Create solutions directory if it doesn't exist
    if not os.path.exists(SOLUTIONS_DIR):
        os.makedirs(SOLUTIONS_DIR)

    with os.scandir(SOLUTIONS_DIR) as entries:
        files = sorted(entry.name for entry in entries)

        # First run case
        if files and seq_start_loc != '':
            run_validation = False

        # Regular run
        elif not files and seq_start_loc == '':
            run_validation = True

        # Invalid project state
        else:
            raise ValueError('Invalid project state: Either (1) Solutions dir contains file(s) and SEQ_START value set or (2) Solutions dir is empty and SEQ_START value set to empty string.')

    results = run_validation


    return results


def initialize_project_config(env_vars: dict[str, str | int]) -> int:
    """
    Updates config.py with environment variables.

    Args:
        env_vars: Dictionary containing project configuration values
            Keys: 'proj_title', 'seq_start', 'nb', 'nb_name', 'seq_notation'

    Returns:
        int: 1 if configuration update successful
    """
    with open(f'{CONFIG_DIR}/config.py', 'r+', encoding='utf-8') as file:
        lines = file.readlines()

        for i, line in enumerate(lines):

            if line.startswith('PROJ_TITLE='):
                lines[i] = f'PROJ_TITLE=\'{env_vars["proj_title"]}\'\n'

            if line.startswith('SEQ_START='):
                lines[i] = f'SEQ_START=\'{env_vars["seq_start"]}\'\n'

            if line.startswith('NB='):
                lines[i] = f'NB={env_vars["nb"]}\n'

            if line.startswith('NB_NAME='):
                lines[i] = f'NB_NAME=\'{env_vars["nb_name"]}\'\n'

            if line.startswith('SEQ_NOTATION='):
                lines[i] = f'SEQ_NOTATION={env_vars["seq_notation"]}\n'

        file.seek(0)
        file.writelines(lines)
        file.truncate()


    return 1


def initialize_project_title(env_vars: dict[str, str | int]) -> int:
    """
    Updates project title in README and solution template files.

    Args:
        env_vars: Dictionary containing project configuration values
            Required key: 'proj_title'

    Returns:
        int: 1 if title update successful
    """
    # HANDLE README
    with open('README.md', 'r+', encoding='utf-8') as file:
        lines_readme_title = file.readlines()

        lines_readme_title[0] = f'# {env_vars['proj_title']}\n'

        file.seek(0)
        file.writelines(lines_readme_title)
        file.truncate()

    # HANDLE TEMPLATE
    with open('src/main/templates/solution.txt', 'r+', encoding='utf-8') as file:
        lines_template_title = file.readlines()

        lines_template_title[0] = f'# {env_vars["proj_title"]} \\#{{{{ seq_full }}}}\n'

        file.seek(0)
        file.writelines(lines_template_title)
        file.truncate()


    return 1


def initialize_project_nb(env_vars: dict[str, str | int]) -> int:
    """
    Sets up NB in README and solution template files.

    Args:
        env_vars: Dictionary containing project configuration values
            Required key: 'nb_name' for extra column header

    Returns:
        i
    """
    index_header = {
        'labels': f'| Day   | Title   | Solution   | Site   | Difficulty   | {env_vars["nb_name"]}   |',
        'sep': f'| ----- | ------- | ---------- | ------ | ------------ | { "-" * (len(env_vars["nb_name"]) + 2) } |'
    }

    start_line_readme = None
    end_line_readme = None
    lines_readme = []
    lines_template = []

    with open('README.md', 'r+', encoding='utf-8') as file:
        lines_readme = file.readlines()

        for i in range(len(lines_readme)-1, -1, -1):

            if INDEX_START in lines_readme[i]:
                start_line_readme = i

            if INDEX_END in lines_readme[i]:
                end_line_readme = i

        lines_readme[start_line_readme + 1] = f'{index_header["labels"]}\n'
        lines_readme[start_line_readme + 2] = f'{index_header["sep"]}\n'

        for j in range(start_line_readme + 3, end_line_readme):

            lines_readme[j] = ''

        file.seek(0)
        file.writelines(lines_readme)
        file.truncate()

    # HANDLE SETUP - EXTRA COLUMN (aka NB) - TEMPLATE
    with open(f'{TEMPLATES_DIR}/solution.txt', 'r+', encoding='utf-8') as file:
        lines_template = file.readlines()

        lines_template[29] = f'## {env_vars["nb_name"]}\n'
        lines_template[32] = '\n'

        file.seek(0)
        file.writelines(lines_template)
        file.truncate()

    print(f'Extra column selected: {env_vars["nb_name"]}')


    return 1


def initialize_project(handler: PackageHandler, today: datetime) -> int:
    """
    Initializes the project for first run, setting up necessary user configurations.

    Args:
        handler (PackageHandler): Package handler instance for managing configurations
        today (datetime): Current date used for initialization

    Returns:
        int: 1 if initialization successful

    Side Effects:
        - Sets SEQ_START to prevent future initialization
        - Configures index table with 5 or 6 columns
        - Updates configuration dictionaries with new values
        - Creates or modifies multiple files (config.py, README.md, solution template)

    Prerequisites:
        - Solutions directory must be empty
        - SEQ_START must have empty string default value
        - Required environment variables or defaults must be available
    """
    # HANDLE ENVIRONMENT VARIABLES
    # Use global as default
    env_vars = {
        'proj_title': os.environ.get('PROJ_TITLE', PROJ_TITLE),
        'seq_start': today.strftime(f'%Y{HYPHEN}%m{HYPHEN}%d'),
        'nb': int(os.environ.get('NB', NB)),
        'nb_name': os.environ.get('NB_NAME', NB_NAME),
        'seq_notation': int(os.environ.get('SEQ_NOTATION', SEQ_NOTATION)),
    }

    # HANDLE CONFIG.PY
    initialize_project_config(env_vars)

    # HANDLE PROJECT TITLE
    if env_vars['proj_title'] != '[ ] Everyday':
        initialize_project_title(env_vars)

    # HANDLE EXTRA COLUMN (aka NB)
    if env_vars['nb'] == 1:
        initialize_project_nb(env_vars)

    # HANDLE DICTS
    handler.update_value('config_base', 'proj_title_loc', env_vars['proj_title'])
    handler.update_value('config_base', 'seq_start_loc', env_vars['seq_start'])
    handler.update_value('config_base', 'nb_loc', env_vars['nb'])
    handler.update_value('config_base', 'nb_name_loc', env_vars['nb_name'])
    handler.update_value('config_base', 'seq_notation_loc', env_vars['seq_notation'])
    handler.update_value('config_cols_widths', 'nb', len(env_vars['nb_name']) + 2)

    print('First run initialized')


    return 1


def open_runs_seq(handler: PackageHandler, today: datetime) -> tuple[str, str]:
    """
    Generates a sequence identifier for each entry in the Index table and solution 
    filename prefix.
    
    Args:
        handler (PackageHandler): Handler containing data
        today (datetime): Current timestamp for sequence generation
    
    Returns:
        tuple[str, str]: Tuple containing (sequence_id, full_sequence_id) where:
            - sequence_id: Either a 3-digit number or date string (YYYY‑MM‑DD)
            - full_sequence_id: sequence_id with suffix (e.g. "001_01" or "2025‑01‑31_01")
        
    Raises:
        ValueError: If seq_notation_loc is not 0 or 1
        
    Note:
        Uses seq_notation_loc to determine sequence format:
        - 0: Three digit sequence (e.g. "001")
        - 1: Date format using Unicode non-breaking hyphens U+2011 (e.g. "2025‑01‑31")
    """
    seq_start_loc = handler.get_value('config_base', 'seq_start_loc')
    seq_notation_loc = handler.get_value('config_base', 'seq_notation_loc')

    with os.scandir(SOLUTIONS_DIR) as entries:
        files = sorted(entry.name for entry in entries)

    if files:

        file_last = files[-1]

        # Handle sequence partials
        if seq_notation_loc == 0:

            seq_last = int(file_last[:3])
            
            seq_last_suffix = int(file_last[4:6])

            seq_actual = datetime.strptime(seq_start_loc, f'%Y{HYPHEN}%m{HYPHEN}%d')
            seq_actual = seq_actual.date()
            seq_actual = (today.date() - seq_actual).days + 1

            seq = f'{seq_actual:03d}'

        elif seq_notation_loc == 1:

            seq_last = datetime.strptime(file_last[:10], f'%Y{HYPHEN}%m{HYPHEN}%d')
            seq_last = seq_last.date()

            seq_last_suffix = int(file_last[11:13])

            seq_actual = datetime.now().date()

            seq = seq_actual.strftime(f'%Y{HYPHEN}%m{HYPHEN}%d')

        else:

            raise ValueError('Invalid configuration: TODO')

        # Handle full sequence
        if seq_last == seq_actual:
            seq_suffix = seq_last_suffix + 1
            seq_suffix = f'{seq_suffix:02d}'
            seq_full = f'{seq}_{seq_suffix}'
            print('Note: You have submitted more than 1 entry today.')

        elif seq_last < seq_actual:
            seq_full = f'{seq}_01'

        else:
            print('Note: Invalid sequence. Processing not terminated.')

    else:

        if seq_notation_loc == 0:

            seq = '001'
            seq_full = '001_01'

        elif seq_notation_loc == 1:

            seq = today.strftime(f'%Y{HYPHEN}%m{HYPHEN}%d')
            seq_full = today.strftime(f'%Y{HYPHEN}%m{HYPHEN}%d_01')

        else:

            raise ValueError('Invalid configuration: TODO')

    return seq, seq_full


def open_runs_file(title: str, seq_full: str) -> str:
    """
    Creates a standardized filename from title and sequence identifier.
    
    Args:
        title (str): Problem title to be converted into filename
        seq (str): Sequence identifier (either numeric or date format)
    
    Returns:
        str: Formatted filename in the pattern "{seq}_{sanitized_title}.md"
    """
    filename = title.lower()
    filename = re.sub(r'[^a-z0-9\s-]', '', filename)
    filename = filename.replace(' ', '_')
    filename = filename.replace('-', '_')
    filename = f'{seq_full}_{filename.strip()}.md'


    return filename


def open_runs_dicts(handler: PackageHandler, seq: str, seq_full: str, new_package: dict, filename: str) -> int:
    """
    Updates PackageHandler dictionaries.
    
    Args:
        handler (PackageHandler): Handler for managing package data
        seq (str): Sequence identifier
        new_package (dict[str, str]): Dictionary containing problem information
        filename (str): Generated filename for the solution
    
    Returns:
        int: 1 if update successful
        
    Updates:
        - package: Data submitted through form
        - entry_data: Formatted form data for display
        - entry_data_widths: Column width calculations for display formatting
    """
    # Update package
    handler.update_value('package', 'day', seq)
    handler.update_value('package', 'url', new_package["url"])
    handler.update_value('package', 'title', new_package["title"])
    handler.update_value('package', 'site', new_package["site"])
    handler.update_value('package', 'difficulty', new_package["difficulty"])
    handler.update_value('package', 'problem', new_package["problem"])
    handler.update_value('package', 'submitted_solution', new_package["submitted_solution"])
    handler.update_value('package', 'site_solution', new_package["site_solution"])
    handler.update_value('package', 'notes', new_package["notes"])
    handler.update_value('package', 'nb', new_package["nb"])
    handler.update_value('package', 'seq_full', seq_full)
    handler.update_value('package', 'filename', filename)

    # Update entry_data
    handler.update_value('entry_data', 'day', seq)
    handler.update_value('entry_data', 'title', f'[{new_package["title"]}]({new_package["url"]})')
    handler.update_value('entry_data', 'solution', f'[Solution](solutions/{filename})')
    handler.update_value('entry_data', 'site', new_package["site"])
    handler.update_value('entry_data', 'difficulty', new_package["difficulty"])
    handler.update_value('entry_data', 'nb', new_package["nb"])

    # Update entry_data_widths
    handler.update_value('entry_data_widths', 'day', len(seq) + 2)
    handler.update_value('entry_data_widths', 'title', len(f'[{new_package["title"]}]({new_package["url"]})') + 2)
    handler.update_value('entry_data_widths', 'solution', len(f'[Solution](solutions/{filename})') + 2)
    handler.update_value('entry_data_widths', 'site', len(new_package["site"]) + 2)
    handler.update_value('entry_data_widths', 'difficulty', len(new_package["difficulty"]) + 2)
    handler.update_value('entry_data_widths', 'nb', len(new_package["nb"]) + 2)


    return 1


def open_runs(handler: PackageHandler, package_list: list[str], today: datetime) -> int:
    """
    Sets up first and regular runs by processing project information and 
    updating dictionaries.

    Args:
        handler (PackageHandler): Handler object for managing package data
        package_list (list[str]): List containing project information from Jupyter Notebook form
        today (datetime): Current date for timestamp generation

    Returns:
        int: 1 if successful

    Raises:
        ValueError: TD
    
    Updates:
        - handler.package: Core project information and metadata
        - handler.entry_data: Formatted data for display
        - handler.entry_data_widths: Column width calculations

    Note:
        -- package_list validation done elsewhere
        -- Does not update handler.config_cols_widths dictionary

    Prerequisites:
        - Properly initialized config.py, if first run
        - Properly initialized PackageHandler
        - Valid package_list with all required elements from Jupyter Notebook form
    """
    new_package = {
        'url': package_list[0],
        'title': package_list[1],
        'site': package_list[2],
        'difficulty': package_list[3],
        'problem': package_list[4],
        'submitted_solution': package_list[5],
        'site_solution': package_list[6],
        'notes': package_list[7],
        'nb': package_list[8]
    }

    # Create sequence
    seq, seq_full = open_runs_seq(handler, today)

    # Create filename
    filename = open_runs_file(new_package['title'], seq_full)

    # Update PackageHandler dicts
    results = open_runs_dicts(handler, seq, seq_full, new_package, filename)


    return results


def implement_runs(handler: PackageHandler) -> int:
    """
    Processes new entries by creating file and updating Index.

    Args:
        handler (PackageHandler): Handler object for managing package data

    Returns:
        int: 1 if successful

    Updates:
        - Creates new solution file based on package data
        - Updates config_cols_widths if new widths are larger
        - Adds new entry line to README.md index
        - Updates existing index lines if column widths changed

    Prerequisites:
        - Properly initialized PackageHandler
        - Properly updated dictionaries (package, entry_data, entry_data_widths)
        - Valid README.md with index block markers
    """
    # ######################################
    # CREATE NEW FILE
    # ######################################
    get_files_created(handler.get_dictionary('package'))


    # ######################################
    # UPDATE config_cols_widths
    # ######################################
    change_old_lines = 0
    for key, value in handler.get_dictionary('config_cols_widths').items():
        new_value = handler.get_dictionary('entry_data_widths')[key]
        if value < new_value:
            handler.update_value('config_cols_widths', key, new_value)
            change_old_lines = 1


    # ######################################
    # CREATE NEW LINE
    # ######################################
    if handler.get_value('entry_data', 'nb') == 'TBD':
        handler.update_value('entry_data', 'nb', '')
    
    new_entry = get_target_line_updated(handler.get_value('config_base', 'nb_loc'),
                                        handler.get_dictionary('entry_data'),
                                        handler.get_dictionary('config_cols_widths'))


    # ######################################
    # UPDATE INDEX
    # ######################################
    index_block = {
        'start': '<!-- Index Start - WARNING: Do not delete or modify this markdown comment. -->',
        'end': '<!-- Index End - WARNING: Do not delete or modify this markdown comment. -->'
    }

    with open('README.md', 'r+', encoding='utf-8') as file:
        lines = file.readlines()

        start_line = None
        end_line = None

        # GET START AND END LINES OF INDEX
        for i, line in enumerate(lines):
            if index_block['start'] in line:
                start_line = i  # Line numbers start from 1
            if index_block['end'] in line:
                end_line = i


        # UPDATE TARGET LINES (if needed)
        if change_old_lines == 1:

            # Process each line between start_line and end_line
            for i in range(start_line + 1, end_line):

                # Convert target line (str) to data (dict)
                target_line_data = get_target_line_dict(handler.get_value('config_base', 'nb_loc'),
                                                        lines[i])

                # Update target line
                line_updated = get_target_line_updated(handler.get_value('config_base', 'nb_loc'),
                                                       target_line_data,
                                                       handler.get_dictionary('config_cols_widths'))

                # Replace the original line with the updated one
                lines[i] = f'{line_updated}\n'

        # INSERT NEW LINE TO LINES
        lines.insert(end_line, f'{new_entry}\n')

        file.seek(0)
        file.writelines(lines)
        file.truncate()


    return 1


def close_runs(column_widths: dict) -> int:
    """
    Updates the COLS_WIDTH config in columns.py with new data.
    
    Args:
        column_widths (dict): Dictionary containing column width configurations 
    
    Returns:
        int: Returns 1 on successful completion
    """
    with open(f'{CONFIG_DIR}/columns.py', 'r+', encoding='utf-8') as file:
        lines = file.readlines()

        line_target = None
        for i, line in enumerate(lines):
            if 'COLS_WIDTH = {' in line:
                line_target = i
                break

        del lines[line_target:]

        data = f'COLS_WIDTH = {json.dumps(column_widths, indent=4)}\n'

        lines[line_target:line_target] = data.splitlines(True)

        file.seek(0)
        file.writelines(lines)
        file.truncate()


    return 1


def handle_runs_default(handler: PackageHandler, today: datetime, data: dict) -> None:
    """
    Process form inputs and coordinate execution flow by passing values to specialized functions.
    Acts as a coordinator between form submission and data processing pipeline.

    Args:
        TD

    Returns:
        None: Prints "Done" on completion

    Flow:
        1. Validates and cleans input strings
        2. Initiates run configuration process
        3. Implements run settings
        4. Updates configuration columns
    """
    if data['nb'] is None:
        nb = 'TBD'
    else:
        nb = data['nb']

    # Clean input strings
    new_package = clean_strings(data['url'],
                                data['title'],
                                data['site'],
                                data['difficulty'],
                                data['problem'],
                                data['submitted_solution'],
                                data['site_solution'],
                                data['notes'],
                                nb)


    # ######################################
    # RUNS - START (FIRST OR REGULAR)
    # ######################################
    open_runs(handler, new_package, today)


    # ######################################
    # RUNS - IMPLEMENT
    # ######################################
    implement_runs(handler)


    # ######################################
    # RUNS - CLOSE
    # ######################################
    close_runs(handler.get_dictionary('config_cols_widths'))




    return print('Done')
