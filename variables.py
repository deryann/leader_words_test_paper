import os

# Centralized project constants
# _HERE: directory of this file (works in dev, Nuitka standalone, and Nuitka onefile)
_HERE = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = _HERE
CFG_VERSION = "cfg-202602"  # Change this in one place when rolling over to a new config set
CFG_FOLDER = os.path.join(_HERE, CFG_VERSION)
OUTPUT_FOLDER = os.path.join(os.getcwd(), "output")  # Write output to user's working directory
STATIC_FOLDER = os.path.join(_HERE, "static")

__all__ = [
    "BASE_DIR",
    "CFG_VERSION",
    "CFG_FOLDER",
    "OUTPUT_FOLDER",
    "STATIC_FOLDER",
]
