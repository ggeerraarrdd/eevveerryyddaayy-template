"""
TD
"""

# Python Standard Library
from datetime import datetime

# Third-Party Libraries
import ipywidgets as widgets

# Local
from .main import get_runs_validated
from .main import get_runs_initialized
from .config import SEQ_START
from .config import NB
from .config import NB_NAME
from .config import SEQ_NOTATION
from .config import SEQ_SPARSE
from .config import SOLUTIONS_DIR
from .config import CONFIG_DIR
from .config import TEMPLATES_DIR
from .config import COLS_WIDTH








class PackageHandler:
    """
    TD
    """
    def __init__(self):
        self._data = {
            "package": {
                "day": "",
                "url": "",
                "title": "",
                "site": "",
                "difficulty": "",
                "problem": "",
                "submitted_solution": "",
                "site_solution": "",
                "notes": "",
                "nb": "",
                "filename": "",
                "lastline": "\n",
            },

            "entry_data": {
                "day": "",
                "title": "",
                "solution": "",
                "site": "",
                "difficulty": "",
                "nb": "",
            },

            "entry_data_widths": {
                "day": 0,
                "title": 0,
                "solution": 0,
                "site": 0,
                "difficulty": 0,
                "nb": 0,
            },

            # "target_line_data": {
            #     "day": "",
            #     "title": "",
            #     "solution": "",
            #     "site": "",
            #     "difficulty": "",
            #     "nb": "",
            # },

            "config_base": {
                "seq_start_loc": SEQ_START,
                "nb_loc": NB,
                "nb_name_loc": NB_NAME,
                "seq_notation_loc": SEQ_NOTATION,
                "seq_sparse_loc": SEQ_SPARSE,
                "solutions_dir_loc": SOLUTIONS_DIR,
                "config_dir_loc": CONFIG_DIR,
                "templates_dir_loc": TEMPLATES_DIR,
            },

            "config_cols_widths": {
                "day": COLS_WIDTH["day"],
                "title": COLS_WIDTH["title"],
                "solution": COLS_WIDTH["solution"],
                "site": COLS_WIDTH["site"],
                "difficulty": COLS_WIDTH["difficulty"],
                "nb": COLS_WIDTH["nb"],
            }
        }

        # Store initial state for reset functionality
        self._initial_state = {
            "package": {
                "day": "",
                "url": "",
                "title": "",
                "site": "",
                "difficulty": "",
                "problem": "",
                "submitted_solution": "",
                "site_solution": "",
                "notes": "",
                "nb": "",
                "filename": "",
                "lastline": "\n",
            },

            "entry_data": {
                "day": "",
                "title": "",
                "solution": "",
                "site": "",
                "difficulty": "",
                "nb": "",
            },

            "entry_data_widths": {
                "day": 0,
                "title": 0,
                "solution": 0,
                "site": 0,
                "difficulty": 0,
                "nb": 0,
            },

            # "target_line_data": {
            #     "day": "",
            #     "title": "",
            #     "solution": "",
            #     "site": "",
            #     "difficulty": "",
            #     "nb": "",
            # },

            "config_base": {
                "seq_start_loc": SEQ_NOTATION,
                "nb_loc": NB,
                "nb_name_loc": NB_NAME,
                "seq_notation_loc": SEQ_NOTATION,
                "seq_sparse_loc": SEQ_SPARSE,
                "solutions_dir_loc": SOLUTIONS_DIR,
                "config_dir_loc": CONFIG_DIR,
                "templates_dir_loc": TEMPLATES_DIR,
            },

            "config_cols_widths": {
                "day": COLS_WIDTH["day"],
                "title": COLS_WIDTH["title"],
                "solution": COLS_WIDTH["solution"],
                "site": COLS_WIDTH["site"],
                "difficulty": COLS_WIDTH["difficulty"],
                "nb": COLS_WIDTH["nb"],
            }
        }


    def get_value(self, dict_name, key):
        """Get value from specified dictionary"""
        if dict_name in self._data and key in self._data[dict_name]:
            return self._data[dict_name][key]
        raise KeyError(f"Invalid dictionary name '{dict_name}' or key '{key}'")


    def update_value(self, dict_name, key, value):
        """Update value in specified dictionary"""
        if dict_name in self._data and key in self._data[dict_name]:
            self._data[dict_name][key] = value
        else:
            raise KeyError(f"Invalid dictionary name '{dict_name}' or key '{key}'")


    def get_dictionary(self, dict_name):
        """Get entire dictionary by name"""
        if dict_name in self._data:
            return self._data[dict_name]
        raise KeyError(f"Invalid dictionary name '{dict_name}'")

    def reset_dictionaries(self, dict_names=None):
        """Reset specified dictionaries or all dictionaries to their initial state"""
        if dict_names is None:
            self._data = self._initial_state.copy()
        else:
            for dict_name in dict_names:
                if dict_name in self._initial_state:
                    self._data[dict_name] = self._initial_state[dict_name].copy()
                else:
                    raise KeyError(f"Invalid dictionary name '{dict_name}'")





# %% Layout Settings
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

site_widget = widgets.Dropdown(
    options=['', 'LeetCode', 'HackerRank', 'DataLemur', 'Other'],
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
# %%





def get_form_section_head():
    """
    TD
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


def get_form_section_main():
    """
    TD
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
        ('URL', url_widget),
        ('Title', title_widget),
        ('Site', site_widget),
        ('Difficulty', difficulty_widget),
        ('Problem', problem_widget),
        ('Your Solution', submitted_solution_widget),
        ('Site Solution', site_solution_widget),
        ('Notes', notes_widget)
    ]

    if NB == 1:
        sections.append(('NB', nb_widget))

    section_list = []
    for heading, widget in sections:
        label = widgets.HTML(value=f'<b>{heading}</b>', layout=label_layout)
        section_list.append(widgets.VBox([label, widget], layout=container_layout))

    section_main = widgets.VBox(section_list, layout=container_layout)

    return section_main


def get_form_section_button(handler, today, file_last):
    """
    TD
    """

    container_layout = widgets.Layout(
        display='flex',
        flex_flow='column',
        align_items='center',
        width='100%'
    )

    def create_solution_file(b):

        print(b.tooltip)

        from src import get_runs_default

        # try:
        #     nb = nb
        # except:
        #     nb = "TBD"

        get_runs_default(
            handler,
            title = title_widget.value,
            url = url_widget.value,
            site = site_widget.value,
            difficulty = difficulty_widget.value,
            problem = problem_widget.value,
            submitted_solution = submitted_solution_widget.value,
            site_solution = site_solution_widget.value,
            notes = notes_widget.value,
            nb = nb_widget.value,
            today = today,
            file_last = file_last
        )


    create_button = widgets.Button(description="Process Entry", tooltip="Processing...")
    create_button.on_click(create_solution_file)
    section_button = widgets.VBox([create_button], layout=container_layout)


    return section_button


def get_form():
    """
    TD
    """

    # ######################################
    # GET HANDLER
    # ######################################
    handler = PackageHandler()


    # ######################################
    # GET RUNS VALIDATED (FIRST OR REGULAR)
    # ######################################
    is_run_first, file_last = get_runs_validated(handler)



    # ######################################
    # GET RUNS INITIALIZED (FIRST)
    # ######################################
    today = datetime.now().strftime("%Y-%m-%d")

    if is_run_first:

        get_runs_initialized(handler, today)

    elif not is_run_first:

        pass

    else:

        raise ValueError("Invalid configuration: TODO")


    # ######################################
    # GET FORM
    # ######################################
    container_layout = widgets.Layout(
        display='flex',
        flex_flow='column',
        align_items='center',
        width='100%'
    )

    head = get_form_section_head()
    main = get_form_section_main()
    button = get_form_section_button(handler, today, file_last)

    full_section = widgets.VBox([head, main, button], layout=container_layout)


    return full_section
