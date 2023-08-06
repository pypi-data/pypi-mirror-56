
import os
import sys

HERE_PATH =  os.path.abspath(os.path.dirname(__file__))

if not HERE_PATH in sys.path:
    sys.path.insert(0, HERE_PATH)
