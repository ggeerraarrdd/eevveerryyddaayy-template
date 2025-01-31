"""
TD
"""

# Third-Party Libraries
from jinja2 import Template

# Local
from src.main.config import NB
from src.main.config import TEMPLATES_DIR










def clean_strings(*args):

    results = []
    for arg in args:
        results.append(arg.strip("\n"))

    return results


def get_files_created(data):

    with open(f"{TEMPLATES_DIR}/solution.txt", "r", encoding='utf-8') as file:
        template_content = file.read()

    # Create a Jinja2 template object
    template = Template(template_content)

    # Render the template with the data
    filled_document = template.render(data)

    with open(f"solutions/{data['filename']}", "w", encoding='utf-8') as file:
        file.write(filled_document)

    return 1


def get_target_line_dict(line):

    data = {
        'day': '',
        'title': '',
        'solution': '',
        'site': '',
        'difficulty': '',
        'nb': '',
    }

    if NB == 0:

        keys = list(data.keys())[:-1]  # Exclude 'nb'

    elif NB == 1:

        keys = list(data.keys())

    else:

        raise ValueError("Invalid configuration: TODO")


    segments = []
    for segment in line.split('|'):
        segment = segment.strip()
        if segment:
            segments.append(segment)

    for i, key in enumerate(keys):
        if i < len(segments):
            data[key] = f"{segments[i]}"

    results = data

    return results


def get_target_line_updated(data, widths):

    target_line = "|"

    if NB == 0:

        for key, value in data.items():

            if key != 'nb':  # Skip the 'nb' key
                value_str = str(value)
                is_second_line = all(char == "-" for char in value_str.strip())
                diff = widths[key] - len(value_str)

                if is_second_line:
                    padding = '-' * diff
                else:
                    padding = ' ' * diff

                target_line += f" {value_str}{padding} |"

    elif NB == 1:

        for key, value in data.items():

            value_str = str(value)

            is_second_line = value_str and all(char == "-" for char in value_str.strip())
            diff = widths[key] - len(value_str)

            if is_second_line:
                padding = '-' * diff
            else:
                padding = ' ' * diff

            target_line += f" {value_str}{padding} |"

    else:

        raise ValueError("Invalid configuration: TODO")

    results = target_line

    return results
