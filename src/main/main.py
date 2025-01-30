"""
EEVVEERRYYDDAAYY Project Module

This module handles the core functionality for managing field values
submitted through the form generated in notebook.py. 

It provides classes and functions to:
- Initialize and configure project settings
- Process new entries
- Manage project files and reference index

Author: Gerard Bul-lalayao
"""

# Python Standard Library
import os
import re
from datetime import datetime, timedelta



# Local
from .config import SOLUTIONS_DIR
from .config import CONFIG_DIR
from .config import TEMPLATES_DIR
from .helpers import clean_strings
from .helpers import get_files_created
from .helpers import get_target_line_dict
from .helpers import get_target_line_updated
from .helpers import get_config_columns_updated
from .helpers import PackageHandler










def get_runs_validated(handler : PackageHandler) -> bool:
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

    seq_start_loc = handler.get_value("config_base", "seq_start_loc")

    # Create solutions directory if it doesn't exist
    if not os.path.exists(SOLUTIONS_DIR):
        os.makedirs(SOLUTIONS_DIR)

    with os.scandir(SOLUTIONS_DIR) as entries:
        files = sorted(entry.name for entry in entries)

        # First run case
        if files and seq_start_loc != "":
            run_validation = False

        # Regular run
        elif not files and seq_start_loc == "":
            run_validation = True

        # Invalid project state
        else:
            raise ValueError("Invalid project state: Either (1) Solutions dir contains file(s) and SEQ_START value set or (2) Solutions dir is empty and SEQ_START value set to empty string.")

    results = run_validation


    return results


def get_runs_initialized(handler, today):
    """
    Initializes the project for first run, setting up necessary user configurations.

    Prerequisites:
        - Solutions directory must be empty
        - SEQ_START must have empty string default value

    Side Effects:
        - Preventing future initialization
        - Locks Index to 5 or 6 columns
    """

    # HANDLE ENVIRONMENT VARIABLES
    env_vars = {
        "seq_start": repr(today).replace("'", '"'),
        "nb": int(os.environ.get("NB", 0)),
        "nb_name": os.environ.get("NB_NAME", "NB"),
        "seq_notation": int(os.environ.get("SEQ_NOTATION", 0)),
    }

    # HANDLE CONFIG.PY
    with open(f"{CONFIG_DIR}/config.py", "r", encoding="utf-8") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):

        if line.startswith("SEQ_START="):
            lines[i] = f"SEQ_START={env_vars["seq_start"]}\n"

        if line.startswith("NB="):
            lines[i] = f"NB={env_vars["nb"]}\n"

        if line.startswith("NB_NAME="):
            lines[i] = f'NB_NAME="{env_vars["nb_name"]}"\n'

        if line.startswith("SEQ_NOTATION="):
            lines[i] = f"SEQ_NOTATION={env_vars["seq_notation"]}\n"

    with open(f"{CONFIG_DIR}/config.py", "w", encoding="utf-8") as file:
        file.writelines(lines)

    # HANDLE EXTRA COLUMN (aka NB)
    if env_vars["nb"] == 1:

        # HANDLE SETUP - EXTRA COLUMN (aka NB) - README
        index_block = {
            "start": "<!-- Index Start - WARNING: Do not delete or modify this markdown comment. -->",
            "end": "<!-- Index End - WARNING: Do not delete or modify this markdown comment. -->"
        }

        start_line_readme = None
        end_line_readme = None

        index_header = {
            "labels": f"| Day   | Title   | Solution   | Site   | Difficulty   | {env_vars["nb_name"]}   |",
            "sep": f"| ----- | ------- | ---------- | ------ | ------------ | { '-' * (len(env_vars["nb_name"]) + 2) } |"
        }

        with open("README.md", "r", encoding="utf-8") as file:
            lines = file.readlines()

        for i in range(len(lines)-1, -1, -1):

            if index_block["start"] in lines[i]:
                start_line_readme = i

            if index_block["end"] in lines[i]:
                end_line_readme = i

        for j in range(start_line_readme + 1, end_line_readme):

            if j == start_line_readme + 1:

                lines[j] = f"{index_header["labels"]}\n"

            if j == start_line_readme + 2:

                lines[j] = f"{index_header["sep"]}\n"

            if j > start_line_readme + 2:

                lines[j] = ""

        with open("README.md", "w", encoding="utf-8") as file:
            file.writelines(lines)


        # HANDLE SETUP - EXTRA COLUMN (aka NB) - TEMPLATE
        with open(f"{TEMPLATES_DIR}/solution.txt", "r", encoding="utf-8") as file:
            lines_template = file.readlines()

        lines_template[29] = f"## {env_vars["nb_name"]}\n"
        lines_template[32] = "\n"

        with open(f"{TEMPLATES_DIR}/solution.txt", "w", encoding="utf-8") as file:
            file.writelines(lines_template)

        print(f"Extra column selected: {env_vars["nb_name"]}")


    # ######################################
    #
    # UPDATE DICTS
    #
    # ######################################
    handler.update_value("config_base", "seq_start_loc", env_vars["seq_start"])
    handler.update_value("config_base", "nb_loc", env_vars["nb"])
    handler.update_value("config_base", "nb_name_loc", env_vars["nb_name"])
    handler.update_value("config_base", "seq_notation_loc", env_vars["seq_notation"])

    handler.update_value("config_cols_widths", "nb", len(env_vars["nb_name"]) + 2)

    print("First run initialized")

    results = 1


    return results


def get_runs_started(handler, package_list, today):
    """
    Sets up first and regular runs by processing project information and updating
    all dictionaries except config_cols_widths.
        
    Prerequisites:
        - Valid package_list with all required elements from Jupyter Notebook form
        - Properly initialized PackageHandler
    """

    url = package_list[0]
    title = package_list[1]
    site = package_list[2]
    difficulty = package_list[3]
    problem = package_list[4]
    submitted_solution = package_list[5]
    site_solution = package_list[6]
    notes = package_list[7]
    nb = package_list[8]


    # Get sequence
    seq_notation_loc = handler.get_value("config_base", "seq_notation_loc")

    with os.scandir(SOLUTIONS_DIR) as entries:
        files = sorted(entry.name for entry in entries)

    if files:

        file_last = files[-1]

        if seq_notation_loc == 0:

            file_counter = int(file_last[:3]) + 1
            day = f"{file_counter:03d}"

        elif seq_notation_loc == 1:

            file_counter = datetime.strptime(file_last[:10], '%Y-%m-%d')
            file_counter = file_counter + timedelta(days=1)
            day = file_counter.strftime('%Y-%m-%d')

        else:

            raise ValueError("Invalid configuration: TODO")

    else:

        if seq_notation_loc == 0:

            day = "001"

        elif seq_notation_loc == 1:

            day = today.strftime('%Y-%m-%d')

        else:

            raise ValueError("Invalid configuration: TODO")


    # Get filename
    filename = title.lower()
    filename = re.sub(r"[^a-z0-9\s-]", "", filename)
    filename = filename.replace(" ", "_")
    filename = filename.replace("-", "_")
    filename = f"{day}_{filename.strip()}.md"


    # ######################################
    #
    # GET DICTIONARIES UPDATED
    #
    # ######################################
    # Update package
    handler.update_value("package", "day", day)
    handler.update_value("package", "url", url)
    handler.update_value("package", "title", title)
    handler.update_value("package", "site", site)
    handler.update_value("package", "difficulty", difficulty)
    handler.update_value("package", "problem", problem)
    handler.update_value("package", "submitted_solution", submitted_solution)
    handler.update_value("package", "site_solution", site_solution)
    handler.update_value("package", "notes", notes)
    handler.update_value("package", "nb", nb)
    handler.update_value("package", "filename", filename)

    # Update entry_data
    handler.update_value("entry_data", "day", day)
    handler.update_value("entry_data", "title", f"[{title}]({url})")
    handler.update_value("entry_data", "solution", f"[Solution](solutions/{filename})")
    handler.update_value("entry_data", "site", site)
    handler.update_value("entry_data", "difficulty", difficulty)
    handler.update_value("entry_data", "nb", nb)

    # Update entry_data_widths
    handler.update_value("entry_data_widths", "day", len(day) + 2)
    handler.update_value("entry_data_widths", "title", len(f"[{title}]({url}") + 2)
    handler.update_value("entry_data_widths", "solution", len(f"[Solution](solutions/{filename})") + 2)
    handler.update_value("entry_data_widths", "site", len(site) + 2)
    handler.update_value("entry_data_widths", "difficulty", len(difficulty) + 2)
    handler.update_value("entry_data_widths", "nb", len(nb) + 2)

    return 1


def get_runs_implemented(handler):
    """
    Processes new entries by creating file and updating Index.

    Prerequisites:
        - Propery updated dictionaries
        - Properly initialized PackageHandler
    """

    # ######################################
    # CREATE NEW FILE
    # ######################################
    get_files_created(handler.get_dictionary("package"))


    # ######################################
    # UPDATE config_cols_widths
    # ######################################
    change_old_lines = 0
    for key, value in handler.get_dictionary("config_cols_widths").items():
        config_value = value
        new_value = handler.get_dictionary("entry_data_widths")[key]
        if config_value < new_value:
            handler.update_value("config_cols_widths", key, new_value)
            change_old_lines = 1


    # ######################################
    # CREATE NEW LINE
    # ######################################
    if handler.get_value("entry_data", "nb"):

        handler.update_value("entry_data", "nb", "")

    new_entry = get_target_line_updated(handler.get_dictionary("entry_data"), 
                                        handler.get_dictionary("config_cols_widths"))


    # ######################################
    # GET TARGET LINES FROM README
    # ######################################
    start_comment = "<!-- Index Start - WARNING: Do not delete or modify this markdown comment. -->"
    end_comment = "<!-- Index End - WARNING: Do not delete or modify this markdown comment. -->"
    with open("README.md", "r", encoding='utf-8') as file:
        lines = file.readlines()

        start_line = None
        end_line = None

        for i, line in enumerate(lines):
            if start_comment in line:
                start_line = i  # Line numbers start from 1
            if end_comment in line:
                end_line = i


    # ######################################
    # UPDATE TARGET LINES (if needed)
    # ######################################
    if change_old_lines == 1:

        for i in range(start_line + 1, end_line):

            line = lines[i]

            # Convert line (str) to data (dict)
            target_line_data = get_target_line_dict(line)

            # Process each line between start_line and end_line
            line_updated = get_target_line_updated(target_line_data, 
                                                   handler.get_dictionary("config_cols_widths"))

            # Replace the original line with the updated one
            lines[i] = f"{line_updated}\n"


    # ######################################
    # INSERT NEW LINE TO LINES
    # ######################################
    lines.insert(end_line, f"{new_entry}\n")


    # ######################################
    # WRITE LINES BACK TO README
    # ######################################
    # Write the updated content back to the file
    with open("README.md", "w", encoding='utf-8') as file:
        file.writelines(lines)


    return 1


def get_runs_default(handler, url, title, site, difficulty, problem, submitted_solution, site_solution, notes, nb, today):
    """
    TD
    """

    if nb is None:
        nb = "TBD"

    # Clean input strings
    package_list = clean_strings(url, title, site, difficulty, problem, submitted_solution, site_solution, notes, nb)


    # ######################################
    # GET RUNS STARTED (FIRST OR REGULAR)
    # ######################################
    get_runs_started(handler, package_list, today)


    # ######################################
    # GET RUNS IMPLEMENTED
    # ######################################
    get_runs_implemented(handler)


    # ######################################
    # GET RUNS CLOSED
    # ######################################
    get_config_columns_updated(handler.get_dictionary("config_cols_widths"))




    return print("Done")
