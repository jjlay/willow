

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
#   MODULE: save_instructions.py
#
#   PURPOSE:
#   Writes the instructions to disk. At the moment, the program does not 
#   modify the instructions. Future versions may allow the agent to modify 
#   its own instructions to change to better fit the user as time passes.
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
#  FUNCTION: save_instructions()
#
###############################################################################

def save_instructions(instructions, path) :
    """Saves the chat history (list of dicts) to a JSON file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(instructions)

        console.print(f"✅ Instructions successfully saved to {path}")
    
    except IOError as e:
        global_variables.console.print(f"❌ Error saving file: {e}")
    
    return

    ###  END OF SAVE_INSTRUCTIONS  ###

