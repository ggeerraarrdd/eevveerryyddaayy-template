from .main import handle_runs_default

# Version information
__version__ = "0.1.0"

# Define what should be available when using "from src import *"
__all__ = ["handle_runs_default"]

# Package-level configuration
PACKAGE_NAME = "everyday-template"
DEBUG = False

# Exclude test files from package imports
def _is_test_file(name: str) -> bool:
    return name.startswith("test_") or name.endswith("_test.py")
