import os

_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.join(_FILE_DIR, os.path.pardir))
DATA_DIR = os.path.join(BASE_DIR, "data")
