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
from datetime import datetime, timedelta
import json
import os
import re

# Local
from .config import SOLUTIONS_DIR
from .config import CONFIG_DIR
from .config import TEMPLATES_DIR
from .helpers import clean_strings
from .helpers import get_files_created
from .helpers import get_target_line_dict
from .helpers import get_target_line_updated
from .helpers import PackageHandler










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


def initialize_runs(handler: PackageHandler, today: datetime) -> int:
    """
    Initializes the project for first run, setting up necessary user configurations.

    Args:
        handler (PackageHandler): Package handler instance for managing configurations
        today (datetime): Current date used for initialization

    Returns:
        int: 1 if initialization successful

    Side Effects:
        - Prevents future initialization by setting SEQ_START
        - Locks Index to 5 or 6 columns

    Prerequisites:
        - Solutions directory must be empty
        - SEQ_START must have empty string default value
    """

    # HANDLE ENVIRONMENT VARIABLES
    env_vars = {
        "seq_start": f'"{today.strftime('%Y-%m-%d')}"',
        "nb": int(os.environ.get("NB", 0)),
        "nb_name": os.environ.get("NB_NAME", "NB"),
        "seq_notation": int(os.environ.get("SEQ_NOTATION", 0)),
    }


    # HANDLE CONFIG.PY
    with open(f"{CONFIG_DIR}/config.py", "r+", encoding="utf-8") as file:
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

        file.seek(0)
        file.writelines(lines)
        file.truncate()


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

        with open("README.md", "r+", encoding="utf-8") as file:
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

            file.seek(0)
            file.writelines(lines)
            file.truncate()

        # HANDLE SETUP - EXTRA COLUMN (aka NB) - TEMPLATE
        with open(f"{TEMPLATES_DIR}/solution.txt", "r+", encoding="utf-8") as file:
            lines_template = file.readlines()

            lines_template[29] = f"## {env_vars["nb_name"]}\n"
            lines_template[32] = "\n"

            file.seek(0)
            file.writelines(lines_template)
            file.truncate()

        print(f"Extra column selected: {env_vars["nb_name"]}")


    # UPDATE DICTS
    handler.update_value("config_base", "seq_start_loc", env_vars["seq_start"])
    handler.update_value("config_base", "nb_loc", env_vars["nb"])
    handler.update_value("config_base", "nb_name_loc", env_vars["nb_name"])
    handler.update_value("config_base", "seq_notation_loc", env_vars["seq_notation"])

    handler.update_value("config_cols_widths", "nb", len(env_vars["nb_name"]) + 2)

    print("First run initialized")


    return 1


def start_runs(handler: PackageHandler, package_list: list[str], today: datetime) -> int:
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
        - Properly initialized PackageHandler
        - Valid package_list with all required elements from Jupyter Notebook form
    """

    new_package = {
        "url": package_list[0],
        "title": package_list[1],
        "site": package_list[2],
        "difficulty": package_list[3],
        "problem": package_list[4],
        "submitted_solution": package_list[5],
        "site_solution": package_list[6],
        "notes": package_list[7],
        "nb": package_list[8]
    }

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

            file_counter = datetime.strptime(file_last[:10], "%Y-%m-%d")

            if file_counter == today:
                print("Note: You have submitted more than 1 entry today.")
                day = file_counter.strftime("%Y-%m-%d")
            elif file_counter > today:
                file_counter = file_counter + timedelta(days=1)
                day = file_counter.strftime("%Y-%m-%d")
            else:
                print("Note: Invalid sequence. Processing not terminated.")
                day = file_counter.strftime("%Y-%m-%d")

        else:

            raise ValueError("Invalid configuration: TODO")

    else:

        if seq_notation_loc == 0:

            day = "001"

        elif seq_notation_loc == 1:

            day = today.strftime("%Y-%m-%d")

        else:

            raise ValueError("Invalid configuration: TODO")


    # Get filename
    filename = new_package["title"].lower()
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
    handler.update_value("package", "url", new_package["url"])
    handler.update_value("package", "title", new_package["title"])
    handler.update_value("package", "site", new_package["site"])
    handler.update_value("package", "difficulty", new_package["difficulty"])
    handler.update_value("package", "problem", new_package["problem"])
    handler.update_value("package", "submitted_solution", new_package["submitted_solution"])
    handler.update_value("package", "site_solution", new_package["site_solution"])
    handler.update_value("package", "notes", new_package["notes"])
    handler.update_value("package", "nb", new_package["nb"])
    handler.update_value("package", "filename", filename)

    # Update entry_data
    handler.update_value("entry_data", "day", day)
    handler.update_value("entry_data", "title", f"[{new_package["title"]}]({new_package["url"]})")
    handler.update_value("entry_data", "solution", f"[Solution](solutions/{filename})")
    handler.update_value("entry_data", "site", new_package["site"])
    handler.update_value("entry_data", "difficulty", new_package["difficulty"])
    handler.update_value("entry_data", "nb", new_package["nb"])

    # Update entry_data_widths
    handler.update_value("entry_data_widths", "day", len(day) + 2)
    handler.update_value("entry_data_widths", "title", len(f"[{new_package["title"]}]({new_package["url"]})") + 2)
    handler.update_value("entry_data_widths", "solution", len(f"[Solution](solutions/{filename})") + 2)
    handler.update_value("entry_data_widths", "site", len(new_package["site"]) + 2)
    handler.update_value("entry_data_widths", "difficulty", len(new_package["difficulty"]) + 2)
    handler.update_value("entry_data_widths", "nb", len(new_package["nb"]) + 2)

    return 1


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
    get_files_created(handler.get_dictionary("package"))


    # ######################################
    # UPDATE config_cols_widths
    # ######################################
    change_old_lines = 0
    for key, value in handler.get_dictionary("config_cols_widths").items():
        new_value = handler.get_dictionary("entry_data_widths")[key]
        if value < new_value:
            handler.update_value("config_cols_widths", key, new_value)
            change_old_lines = 1


    # ######################################
    # CREATE NEW LINE
    # ######################################
    if handler.get_value("entry_data", "nb"):
        handler.update_value("entry_data", "nb", "")

    new_entry = get_target_line_updated(handler.get_value("config_base", "nb_loc"),
                                        handler.get_dictionary("entry_data"),
                                        handler.get_dictionary("config_cols_widths"))


    # ######################################
    # GET TARGET LINES FROM README
    # ######################################
    index_block = {
        "start": "<!-- Index Start - WARNING: Do not delete or modify this markdown comment. -->",
        "end": "<!-- Index End - WARNING: Do not delete or modify this markdown comment. -->"
    }

    with open("README.md", "r+", encoding='utf-8') as file:
        lines = file.readlines()

        start_line = None
        end_line = None

        # GET START AND END LINES OF INDEX
        for i, line in enumerate(lines):
            if index_block["start"] in line:
                start_line = i  # Line numbers start from 1
            if index_block["end"] in line:
                end_line = i


        # UPDATE TARGET LINES (if needed)
        if change_old_lines == 1:

            # Process each line between start_line and end_line
            for i in range(start_line + 1, end_line):

                # Convert target line (str) to data (dict)
                target_line_data = get_target_line_dict(handler.get_value("config_base", "nb_loc"),
                                                        lines[i])

                # Update target line
                line_updated = get_target_line_updated(handler.get_value("config_base", "nb_loc"),
                                                       target_line_data,
                                                       handler.get_dictionary("config_cols_widths"))

                # Replace the original line with the updated one
                lines[i] = f"{line_updated}\n"

        # INSERT NEW LINE TO LINES
        lines.insert(end_line, f"{new_entry}\n")

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

    with open(f"{CONFIG_DIR}/columns.py", 'r+', encoding='utf-8') as file:
        lines = file.readlines()

        line_target = None
        for i, line in enumerate(lines):
            if "COLS_WIDTH = {" in line:
                line_target = i
                break

        del lines[line_target:]

        data = f"COLS_WIDTH = {json.dumps(column_widths, indent=4)}\n"

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

    if data["nb"] is None:
        nb = "TBD"
    else:
        nb = data["nb"]

    # Clean input strings
    new_package = clean_strings(data["url"],
                                data["title"],
                                data["site"],
                                data["difficulty"],
                                data["problem"],
                                data["submitted_solution"],
                                data["site_solution"],
                                data["notes"],
                                nb)


    # ######################################
    # RUNS - START (FIRST OR REGULAR)
    # ######################################
    start_runs(handler, new_package, today)


    # ######################################
    # RUNS - IMPLEMENT
    # ######################################
    implement_runs(handler)


    # ######################################
    # RUNS - CLOSE
    # ######################################
    close_runs(handler.get_dictionary("config_cols_widths"))




    return print("Done")
