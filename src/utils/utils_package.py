"""
A data manager class for user data inputs from Jupyter IPywidgets forms.
"""

from typing import Any, Dict, List, Optional










class PackageManager:
    """
    Package Manager

    A data manager class for user data inputs from Jupyter IPywidgets forms. Handles 
    both direct form inputs and values derived from those inputs. The processed data 
    is stored in this PackageManager instance and used to populate project files, 
    including the Index table and file template.

    Attributes
    ----------
        package : Dict[str, str]
            Stores form inputs and derived values with expected keys:
            - day (str): Date or day identifier
            - url (str): Problem URL
            - title (str): Problem title
            - title_index (str): Formatted title for index
            - site (str): Source website name
            - difficulty (str): Problem difficulty level
            - problem (str): Problem description
            - submitted_solution (str): User's submitted code solution
            - site_solution (str): Solution code from site
            - solution (str): Final solution text
            - notes (str): Optional notes
            - nb (str): Quick notes for solution files
            - nb_index (str): Quick notes for optional sixth column of index
            - seq_full (str): Full sequence identifier
            - filename (str): Generated filename
            - lastline (str): Line ending character
        
        package_widths : Dict[str, str]
            Display width for index columns with expected keys:
            - day (int): Width for day column
            - title (int): Width for title column
            - solution (int): Width for solution column
            - site (int): Width for site column
            - difficulty (int): Width for difficulty column
            - nb (int): Width for optional sixth column

    Public Methods
    --------------
        get_value(dict_name: str, key: str) -> Any
            Retrieve value from specified dictionary

        update_value(dict_name: str, key: str, value: Any) -> None
            Update value in specified dictionary

        get_dictionary(dict_name: str) -> dict
            Retrieve entire dictionary by name

        reset(dict_names: Optional[List[str]] = None) -> None
            Reset dictionaries to initial state
    """
    def __init__(self):
        self._data : Dict[str, Dict[str, Any]] = {
            'package': {
                'day': '',
                'url': '',
                'title': '',
                'title_index': '',
                'site': '',
                'difficulty': '',
                'problem': '',
                'submitted_solution': '',
                'site_solution': '',
                'solution': '',
                'notes': '',
                'nb': '',
                'nb_index': '',
                'seq_full': '',
                'filename': '',
                'lastline': '\n',
            },

            'package_widths': {
                'day': 0,
                'title': 0,
                'solution': 0,
                'site': 0,
                'difficulty': 0,
                'nb': 0,
            },

        }

        # Store initial state for reset functionality
        self._initial_state : Dict[str, Dict[str, Any]]  = {
            'package': {
                'day': '',
                'url': '',
                'title': '',
                'title_index': '',
                'site': '',
                'site_index': '',
                'difficulty': '',
                'problem': '',
                'submitted_solution': '',
                'site_solution': '',
                'notes': '',
                'nb': '',
                'seq_full': '',
                'filename': '',
                'lastline': '\n',
            },

            'package_col_widths': {
                'day': 0,
                'title': 0,
                'solution': 0,
                'site': 0,
                'difficulty': 0,
                'nb': 0,
            },
        }


    def get_value(self, dict_name: str, key: str) -> Any:
        """
        Retrieve a value from a specified dictionary using the given key.

        Args:
            dict_name (str): Name of the dictionary to access
            key (str): Key to lookup in the dictionary

        Returns:
            Any: The value associated with the key in the specified dictionary

        Raises:
            KeyError: If dictionary name or key is invalid
        """
        if dict_name in self._data and key in self._data[dict_name]:
            return self._data[dict_name][key]
        raise KeyError(f'Invalid dictionary name \'{dict_name}\' or key \'{key}\'')


    def update_value(self, dict_name: str, key: str, value: Any) -> None:
        """
        Update a value in a specified dictionary for the given key.

        Args:
            dict_name (str): Name of the dictionary to update
            key (str): Key to update in the dictionary
            value (Any): New value to set

        Raises:
            KeyError: If dictionary name or key is invalid
        """
        if dict_name in self._data and key in self._data[dict_name]:
            self._data[dict_name][key] = value
        else:
            raise KeyError(f'Invalid dictionary name \'{dict_name}\' or key \'{key}\'')


    def get_dictionary(self, dict_name: str) -> Dict[str, Any]:
        """
        Retrieve an entire dictionary by its name.

        Args:
            dict_name (str): Name of the dictionary to retrieve

        Returns:
            Dict[str, Any]: The requested dictionary

        Raises:
            KeyError: If dictionary name is invalid
        """
        if dict_name in self._data:
            return self._data[dict_name]
        raise KeyError(f'Invalid dictionary name \'{dict_name}\'')


    def reset(self, dict_names: Optional[List[str]] = None) -> None:
        """
        Reset specified dictionaries or all dictionaries to their initial state.

        Args:
            dict_names (Optional[List[str]]): List of dictionary names to reset.
                If None, resets all dictionaries.

        Raises:
            KeyError: If any dictionary name in the list is invalid
        """
        if dict_names is None:
            self._data = self._initial_state.copy()
        else:
            for dict_name in dict_names:
                if dict_name in self._initial_state:
                    self._data[dict_name] = self._initial_state[dict_name].copy()
                else:
                    raise KeyError(f'Invalid dictionary name \'{dict_name}\'')
