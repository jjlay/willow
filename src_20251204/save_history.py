

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
#   MODULE: save_history.py
#
#   PURPOSE:
#   Writes the chat history to disk so that it can carry between sessions.
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

import json


###############################################################################
#
#  Global Variables
#
###############################################################################

import global_variables


###############################################################################
#
#  FUNCTION: save_history()
#
###############################################################################

def save_history(history, path) :
    """Saves the chat history (list of dicts) to a JSON file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            # We use json.dump() to write the Python list of dicts directly to the file
            json.dump(history, f, indent=4)
        
        #console.print(f"✅ History successfully saved to {path}")
    
    except IOError as e:
        global_variables.console.print(f"❌ Error saving file: {e}")
    
    return

    ###  END OF SAVE_HISTORY  ###

