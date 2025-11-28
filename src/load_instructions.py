
###############################################################################
#
#
#  CHANGE LOG
#
#     DATE        AUTHOR         COMMENTS  
#  ----------   ------------   -------------------
#  2025-10-01   JJ Lay         Initial version
#
#
###############################################################################


###############################################################################
#
#
#   MODULE: load_instructions.py
#
#   PURPOSE:
#   Imports the predefined instructions for the LLM.
#
#
###############################################################################


###############################################################################
#
#   References:
#
#   https://github.com/Textualize/rich?tab=readme-ov-file
#
#
###############################################################################


###############################################################################
#
#  Standard Python Imports
#
###############################################################################

from rich.console import Console
from rich.pretty import pprint
from rich import print
from rich.table import Table
from rich import box

import threading
import queue
import time
import sys


###############################################################################
#
#  Global Variables
#
###############################################################################

import global_variables


###############################################################################
#
#  FUNCTION: load_instructions()
#
###############################################################################

def load_instructions(path) :
    """Loads the instructions from a TXT file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            # We use json.load() to read the JSON and convert it back to a Python list of dicts
            loaded_instructions = f.read()
            #console.print(f"✅ Instructions successfully loaded from {path}")
            return loaded_instructions
        
    except FileNotFoundError:
        console.print(f"⚠️ File not found at {path}. Returning empty list.")
        return []
    
    return

    ###  END OF LOAD_INSTRUCTIONS  ###

