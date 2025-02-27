"""
Form Interface Generator for Project Runs

Creates and manages an interactive form using ipywidgets to collect, validate
and process input data. The form interface is specifically designed for use within a 
Jupyter notebook environment.
"""

# Python Standard Library
from ast import literal_eval
import json  # pylint: disable=unused-import
from typing import Dict

# Third-Party Libraries
import ipywidgets as widgets

# Local
from src.config import ConfigManager











def _create_entry_form_widgets(config: ConfigManager) -> Dict[str, widgets.Widget]:
    """
    Creates and returns the layout settings and widget definitions for the form.
    
    Parameters
    ----------
    config : ConfigManager
        Custom container for validating, storing and retrieving application settings
    
    Returns
    -------
    Dict[str, widgets.Widget]
        Dictionary containing all widget instances needed for the form
    """
    # Common layout settings
    base_layout = {
        'width': '50%',
        'margin': '0 0 25px 0'
    }

    text_layout = {**base_layout}
    textarea_layout = {**base_layout, 'height': '100px'}
    solution_layout = {**base_layout, 'height': '200px'}

    # Widget Definitions
    url_widget = widgets.Textarea(
        value='',
        placeholder='Enter url',
        layout=text_layout
    )

    title_widget = widgets.Textarea(
        value='',
        placeholder='Enter problem title',
        layout=text_layout
    )

    site_options = config.get('SITE_OPTIONS')

    if site_options:
        # Convert list to string representation for literal_eval
        if isinstance(site_options, list):
            site_options_str = str(site_options) # pylint: disable=invalid-name
        else:
            site_options_str = site_options

        options_list = literal_eval(site_options_str)

        # If only one option, make it both the options and default value
        if len(options_list) == 1:
            site_widget = widgets.Dropdown(
                options=[options_list[0]],
                value=options_list[0],
                layout=text_layout
            )
        else:
            site_widget = widgets.Dropdown(
                options=[''] + options_list,
                value='',
                layout=text_layout
            )
    else:
        # Default options if environment variable is not set
        site_widget = widgets.Dropdown(
            options=['', 'Codewars', 'DataLemur', 'LeetCode'],
            value='',
            layout=text_layout
        )

    difficulty_widget = widgets.Dropdown(
        options=['', 'Easy', 'Medium', 'Hard'],
        value='',
        layout=text_layout
    )

    problem_widget = widgets.Textarea(
        value='',
        placeholder='Enter problem description',
        layout=textarea_layout
    )

    submitted_solution_widget = widgets.Textarea(
        value='',
        placeholder='Enter your solution here',
        layout=solution_layout
    )

    site_solution_widget = widgets.Textarea(
        value='',
        placeholder='Enter site solution here',
        layout=solution_layout
    )

    notes_widget = widgets.Textarea(
        value='TBD',
        layout=textarea_layout
    )

    nb_widget = widgets.Textarea(
        value='TBD',
        layout=textarea_layout
    )

    page_title_widget = widgets.Text(
        value='',
        placeholder='Enter page title',
        layout=textarea_layout
    )

    widgets_package = {
        'url': url_widget,
        'title': title_widget,
        'site': site_widget,
        'difficulty': difficulty_widget,
        'problem': problem_widget,
        'submitted_solution': submitted_solution_widget,
        'site_solution': site_solution_widget,
        'notes': notes_widget,
        'nb': nb_widget,
        'page_title': page_title_widget
    }


    return widgets_package


def _create_entry_form_head() -> widgets.VBox:
    """
    Creates the header section of the form.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    widgets.VBox
        A vertical box container with the form header elements.
        
    Notes
    -----
    Builds a header component with title and optional description
    for the form interface.
    """
    label_layout = widgets.Layout(
        width='50%',
        margin='30px 0',
    )

    container_layout = widgets.Layout(
        display='flex',
        flex_flow='column',
        align_items='center',
        width='100%'
    )

    description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'

    heading = widgets.HTML(value='<span style="font-size:20px;"><b>EEVVEERRYYDDAAYY</b></span>', layout=label_layout)
    description = widgets.HTML(value=description, layout=label_layout)

    section_head = widgets.VBox([heading], layout=container_layout)

    return section_head


def _create_entry_form_main(config: ConfigManager, pidgets: Dict[str, widgets.Widget]) -> widgets.VBox:
    """
    Creates the main section of the form with input fields.
    
    Parameters
    ----------
    config : ConfigManager
        ConfigManager instance for configuration management
    pidgets : Dict[str, widgets.Widget]
        Dictionary of widget instances to use in the form

    Returns
    -------
    widgets.VBox
        A vertical box container with all form input fields.
        
    Notes
    -----
    Constructs the main form body with all input fields organized in
    a vertical layout with appropriate labels.
    """
    label_layout = widgets.Layout(
        width='50%',
        margin='0'
    )

    container_layout = widgets.Layout(
        display='flex',
        flex_flow='column',
        align_items='center',
        width='100%'
    )

    sections = [
        ('URL', pidgets['url']),
        ('Title', pidgets['title']),
        ('Site', pidgets['site']),
        ('Difficulty', pidgets['difficulty']),
        ('Problem', pidgets['problem']),
        ('Your Solution', pidgets['submitted_solution']),
        ('Site Solution', pidgets['site_solution']),
        ('Notes', pidgets['notes'])
    ]

    if config.get('NB') == 1:
        sections.append((config.get('NB_NAME'), pidgets['nb']))

    section_list = []
    for heading, widget in sections:
        label = widgets.HTML(value=f'<b>{heading}</b>', layout=label_layout)
        section_list.append(widgets.VBox([label, widget], layout=container_layout))

    section_main = widgets.VBox(section_list, layout=container_layout)

    return section_main


def _create_entry_form_button(config: ConfigManager, pidgets: Dict[str, widgets.Widget]) -> widgets.VBox:
    """
    Creates the form submission button section with validation logic.
    
    Parameters
    ----------
    config : ConfigManager
        Custom container for validating, storing and retrieving application settings
    pidgets : Dict[str, widgets.Widget]
        Dictionary of widget instances used in the form

    Returns
    -------
    widgets.VBox
        A vertical box container with the submission button.
        
    Notes
    -----
    This function creates the button UI element with attached event handlers for
    form validation and submission. Includes nested functions for data processing:
    - validate_form_data(): Validates all form inputs
    - execute_runs(): Processes validated form data and triggers actions
    """
    container_layout = widgets.Layout(
        display='flex',
        flex_flow='column',
        align_items='center',
        width='100%'
    )

    def validate_form_data():

        form_inputs = {
            'url': pidgets['url'].value,
            'title': pidgets['title'].value, 
            'site': pidgets['site'].value,
            'difficulty': pidgets['difficulty'].value,
            'problem': pidgets['problem'].value,
            'submitted_solution': pidgets['submitted_solution'].value,
            'site_solution': pidgets['site_solution'].value,
            'notes': pidgets['notes'].value,
            'nb': pidgets['nb'].value,
        }

        for key, value in form_inputs.items():

            if key == 'nb':
                key = config.get('NB_NAME')
                key_label = key.replace('_', ' ').title()
            else:
                key_label = key.replace('_', ' ').title()

            if not isinstance(value, str):
                return False, f'Field {key_label} must be a string'
            if not value.strip():
                return False, f'Field {key_label} cannot be empty'


        return True, form_inputs

    def execute_runs(b):

        is_valid, form_inputs_validated = validate_form_data()

        if not is_valid:
            print(f'Validation error: {form_inputs_validated}')
            return

        print(b.tooltip)

        # Clear all form fields
        pidgets['url'].value = ''
        pidgets['title'].value = ''
        try:
            pidgets['site'].value = ''
        except ValueError:
            pass
        pidgets['difficulty'].value = ''
        pidgets['problem'].value = ''
        pidgets['submitted_solution'].value = ''
        pidgets['site_solution'].value = ''
        pidgets['notes'].value = 'TBD'
        pidgets['nb'].value = 'TBD'

        # print(form_inputs_validated)

        from src import eevveerryyddaayy # pylint: disable=import-outside-toplevel

        eevveerryyddaayy(form_inputs_validated, source=3)

    create_button = widgets.Button(description='Process Entry', tooltip='Processing...')
    create_button.on_click(execute_runs)
    section_button = widgets.VBox([create_button], layout=container_layout)


    return section_button


def create_entry_form(config: ConfigManager) -> widgets.VBox:
    """
    Creates and returns the complete form interface.
    
    Parameters
    ----------
    config : ConfigManager
        Custom container for validating, storing and retrieving application settings

    Returns
    -------
    widgets.VBox
        The complete form interface containing header, main input fields,
        and submission button.
        
    Notes
    -----
    Assembles the entire form by combining the header, main input fields,
    and submission button into a single form interface. This is the main
    entry point for creating the form.
    """
    container_layout = widgets.Layout(
        display='flex',
        flex_flow='column',
        align_items='center',
        width='100%'
    )

    widgets_package = _create_entry_form_widgets(config)

    head = _create_entry_form_head()
    main = _create_entry_form_main(config, widgets_package)
    button = _create_entry_form_button(config, widgets_package)

    full_section = widgets.VBox([head, main, button], layout=container_layout)


    return full_section
