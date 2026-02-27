import os

# Centralized project constants
BASE_DIR = os.getcwd()
CFG_VERSION = "cfg-202602"  # Change this in one place when rolling over to a new config set
CFG_FOLDER = os.path.join(BASE_DIR, CFG_VERSION)
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")
STATIC_FOLDER = os.path.join(BASE_DIR, "static")

__all__ = [
    "BASE_DIR",
    "CFG_VERSION",
    "CFG_FOLDER",
    "OUTPUT_FOLDER",
    "STATIC_FOLDER",
]
