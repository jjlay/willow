

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
#   MODULE: archiver_thread.py
#
#   PURPOSE:
#   Archive chat history so that it can carry between sessions.
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
import copy


###############################################################################
#
#  Global Variables
#
###############################################################################

import global_variables


###############################################################################
#
#  Project Includes
#
###############################################################################

from load_history import load_history


###############################################################################
#
#  FUNCTION: saver_thread()
#
###############################################################################

def saver_thread() :


    #
    # Load existing history
    #

    json_history = load_history("history.json")

    with global_variables.global_history_lock :
        global_variables.global_history = copy.deepcopy(json_history)
        

    # --- Main conversation loop

    while not global_variables.STOP_EVENT.is_set():
        try:
            # Save history every ten seconds
            time.sleep(10)

            with global_variables.global_history_lock :
                localhistory = copy.deepcopy(global_variables.global_history)
            
            with open("history.json", "w") as history_file :
                json.dump(localhistory, history_file, indent=5)

            #ai2_globals.console.print("Saver: History saved.")

        except Exception as e:
            global_variables.console.print(f"Saver error: {e}")
            global_variables.STOP_EVENT.set()
    
    global_variables.console.print("Saver: Stopped.")



    ###  END OF ARCHIVE_THREAD  ###
