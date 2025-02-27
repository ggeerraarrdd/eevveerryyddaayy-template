"""
A configuration manager class for application settings
"""

# Python Standard Library
from typing import Dict, Any, Optional, Tuple
import importlib.util
from ast import literal_eval

# Local
from .config_paths import CONFIG_DIR










class ConfigManager:
    """
    Configuration Manager
    
    A configuration manager class for application settings loaded from 
    config files and Jupyter Ipywidgets forms. Handles validating 
    configuration values and managing updates to application settings.
    
    Attributes
    ----------
        config : Dict[str, Any]
            Dictionary storing configuration values with keys:
            - PROJ_START (str): Project start date
            - PROJ_TITLE (str): Title used in generated files
            - NB (int): Controls visibility of sixth column
            - NB_NAME (str): Header title for optional sixth column
            - SEQ_NOTATION (int): Format for Day column (0=numbered, 1=date)
            - SEQ_SPARSE (int): Handling of missing days (0=skip, 1=show blank)
            - COLS_WIDTH (dict): Column width settings for markdown table
            - SITE_OPTIONS (list): Available options for problem sites
            - SOLUTIONS_DIR (str): Path to solutions directory
            - CONFIG_DIR (str): Path to config files directory  
            - TEMPLATES_DIR (str): Path to templates directory
        
    
    Public Methods
    --------------
        get(key: str) -> Optional[Any]
            Retrieve a configuration value by key

        get_all(key) -> Dict[str, Any]
            Retrieve copy of entire configuration dictionary

        update(key: str, value: Any) -> bool
            Update configuration value with validation

        load_settings_from_form(config_vars: Optional[Dict[str, Tuple[type, Any]]] = None) -> None
            Process configuration variables with provided parameters or defaults
    """
    def __init__(self):
        # Initialize empty configuration dictionary
        self.config: Dict[str, Any] = {}

        # Load and validate constants from config.py
        self._load_settings_from_system()


    def _load_settings_from_system(self) -> None:
        """
        Load and validate constants from config.py and config_proj.py files
        """
        config_files = [
            f"{CONFIG_DIR}/config_proj.py",
            f"{CONFIG_DIR}/config_index.py",
            f"{CONFIG_DIR}/config_form.py",
            f"{CONFIG_DIR}/config_paths.py",
        ]

        for config_file in config_files:

            try:

                spec = importlib.util.spec_from_file_location("config", config_file)

                if spec and spec.loader:

                    config_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(config_module)

                    # Get all uppercase variables as constants
                    constants = {name: value for name, value in vars(config_module).items() if name.isupper()}

                    # Validate each constant before adding to config
                    for key, value in constants.items():

                        if self._validate_value(key, value, type(value)):
                            self.config[key] = value

            except (ImportError, AttributeError, ValueError) as e:
                print(f"Error loading constants from {config_file}: {e}")


    def load_settings_from_form(self, config_vars: Optional[Dict[str, Tuple[type, Any]]] = None) -> None:
        """
        Process configuration variables with provided parameters or defaults
        """
        # Use defaults if no config vars provided
        if config_vars is None:

            config_vars = {
                'PROJ_TITLE': (str, '[ ] Everyday'),
                'NB': (int, 0),
                'NB_NAME': (str, 'NB'),
                'SEQ_NOTATION': (int, 0),
                'SEQ_SPARSE': (int, 0),
                'SITE_OPTIONS': (list, ['Codewars', 'DataLemur', 'LeetCode'])
            }

        changes = {}

        for key, (expected_type, default) in config_vars.items():

            validated_value = self._convert_and_validate(default, expected_type, default)

            if key in self.config and self.config[key] != validated_value:
                old_value = self.config[key]
                self.config[key] = validated_value
                changes[key] = {
                    'old_value': old_value,
                    'new_value': validated_value
                }
                #self._notify_change(key, old_value, validated_value)
            else:
                self.config[key] = validated_value

        return changes


    def _convert_and_validate(self, value: Any, expected_type: type, default: Any) -> Any:
        """
        Convert and validate a value to its expected type
        """
        try:

            if expected_type == list and isinstance(value, str):

                try:

                    value = literal_eval(value)
                    if not isinstance(value, list):
                        return default

                except (SyntaxError, ValueError, NameError):
                    return default

            elif expected_type in (int, float):

                value = expected_type(value)

            return value if isinstance(value, expected_type) else default

        except (ValueError, TypeError):
            return default


    def _validate_value(self, key: str, value: Any, expected_type: type) -> bool: # pylint: disable=unused-argument
        """
        Validate a value against its expected type
        """
        return isinstance(value, expected_type)


    def _notify_change(self, key: str, old_value: Any, new_value: Any) -> None:
        """
        Log configuration changes
        """
        print(f"Config change: {key} changed from {old_value} to {new_value}")


    def get(self, key: str) -> Optional[Any]:
        """
        Safely get configuration value
        """
        return self.config.get(key)


    def get_all(self) -> Dict[str, Any]:
        """Get the entire configuration dictionary"""
        return self.config.copy()


    def update(self, key: str, value: Any) -> bool:
        """
        Update a configuration value with validation
        """
        if key not in self.config:
            print(f"Error: Key '{key}' not found in configuration")
            return False

        expected_type = type(self.config[key])
        validated_value = self._convert_and_validate(value, expected_type, self.config[key])

        if validated_value != self.config[key]:
            old_value = self.config[key]
            self.config[key] = validated_value
            self._notify_change(key, old_value, validated_value)
            return True

        return False
