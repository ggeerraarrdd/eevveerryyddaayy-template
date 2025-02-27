"""
Utility Functions for Project Runs
"""

# Python Standard Library
from typing import Any, Dict

# Third-Party Libraries
from jinja2 import Template

# Local
from src.config import ConfigManager
from src.utils import PackageManager










def clean_strings(data: Dict[str, str]) -> Dict[str, str]:
    """
    Remove newline characters from string values in a dictionary.

    Parameters
    ----------
    data : Dict[str, str]
        Dictionary containing string values to clean

    Returns
    -------
    Dict[str, str]
        Cleaned dictionary with newlines removed from string values
    """
    cleaned_dict = {}
    for key, value in data.items():
        if isinstance(value, str):
            cleaned_dict[key] = value.strip('\n')
        else:
            cleaned_dict[key] = value
    return cleaned_dict


def get_files_created(config: ConfigManager, data: Dict[str, Any]) -> int:
    """
    Create a solution file using a template and provided data.

    Parameters
    ----------
    config : ConfigManager
        Custom container for validating, storing and retrieving application settings
    data : Dict[str, Any]
        Dictionary containing template variables including "filename"

    Returns
    -------
    int
        1 on successful file creation
    """
    with open(f'{config.get('TEMPLATES_DIR')}/solution.txt', 'r', encoding='utf-8') as file:
        template_content = file.read()

    # Create a Jinja2 template object
    template = Template(template_content)

    # Render the template with the data
    filled_document = template.render(data)

    with open(f'solutions/{data["filename"]}', 'w', encoding='utf-8') as file:
        file.write(filled_document)

    return 1


def get_target_line_dict(nb_loc: int, line: str) -> Dict[str, str]:
    """
    Parse a table line into a dictionary based on notebook configuration.

    Parameters
    ----------
    nb_loc : int
        Notebook configuration value determining parsing behavior
    line : str
        String containing pipe-separated table data

    Returns
    -------
    Dict[str, str]
        Dictionary with parsed table data fields

    Raises
    ------
    ValueError
        If notebook configuration is invalid
    """
    data = {
        'day': '',
        'title': '',
        'solution': '',
        'site': '',
        'difficulty': '',
        'nb': '',
    }

    if nb_loc == 0:

        keys = list(data.keys())[:-1]  # Exclude 'nb'

    elif nb_loc == 1:

        keys = list(data.keys())

    else:

        raise ValueError('Invalid configuration: TODO')


    segments = []
    for segment in line.split('|'):
        segment = segment.strip()
        if segment:
            segments.append(segment)

    for i, key in enumerate(keys):
        if i < len(segments):
            data[key] = f'{segments[i]}'

    results = data

    return results


def get_target_line_updated(is_second_line: bool, config: ConfigManager, package: PackageManager, data: Dict[str, str]) -> str:
    """
    Format a table line with proper padding based on column widths.

    Parameters
    ----------
    is_second_line : bool
        Boolean indicating if this is the second line of Index table
    config : ConfigManager
        Custom container for validating, storing and retrieving application settings
    package : PackageManager
        Custom container for storing and retrieving form data and derived values
    data : Dict[str, str]
        Dictionary containing table cell values

    Returns
    -------
    str
        Formatted table line with proper padding

    Raises
    ------
    ValueError
        If notebook configuration is invalid
    """
    nb_local = config.get('NB')
    widths = package.get_dictionary('package_widths')

    if data is None:
        data_dict = package.get_dictionary('package')
        data = {
            'day': data_dict['day'],
            'title': data_dict['title'],
            'solution': data_dict['solution'],
            'site': data_dict['site'],       
            'difficulty': data_dict['difficulty'],
            'nb': data_dict['nb'],
        }

    target_line = '|'

    if nb_local == 0:

        for key, value in data.items():

            if key != 'nb':  # Skip the "nb" key

                value_str = str(value)
                diff = widths[key] - len(value_str)

                if is_second_line is True:
                    padding = '-' * diff
                else:
                    padding = ' ' * diff

                target_line += f' {value_str}{padding} |'

    elif nb_local == 1:

        for key, value in data.items():

            value_str = str(value)
            diff = widths[key] - len(value_str)

            if is_second_line is True:
                padding = '-' * diff
            else:
                padding = ' ' * diff

            target_line += f' {value_str}{padding} |'

    else:

        raise ValueError('Invalid configuration: TODO')

    results = target_line


    return results
