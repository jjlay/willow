
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
#   MODULE: save_thread.py
#
#   PURPOSE:
#   ** INCOMPLETE **
#   This will save chat history every few seconds.
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
from datetime import datetime


###############################################################################
#
#  Global Variables
#
###############################################################################

import global_variables


###############################################################################
#
#  Gemini Includes
#
###############################################################################

from google.genai.types import Content, Part


###############################################################################
#
#  FUNCTION: recorder_thread()
#
###############################################################################

def recorder_thread():

    # --- Main conversation loop

    while not global_variables.STOP_EVENT.is_set():
        try:
            stuff = global_variables.Recorder_In_Queue.get(timeout=0.1)
            speaker = stuff[0]
            message = stuff[1]
            role = stuff[2]
            timestamp = stuff[3]

            new_entry = {"timestamp" : timestamp, "role" : role, "username" : speaker}
            new_part = [{"text" : message}]
            new_entry["parts"] = new_part
            
            with global_variables.global_history_lock :
                global_variables.global_history.append(new_entry)

            new_parts = [Part.from_text(text=f"At {timestamp}, {speaker} said: {message}")]

            c = Content(role=role, parts=new_parts)
            
            with global_variables.global_content_lock :
                global_variables.global_content.append(c)

            global_variables.Recorder_In_Queue.task_done()
            
        except queue.Empty:
            continue
        except Exception as e:
            global_variables.console.print(f"Recorder error: {e}")
            global_variables.STOP_EVENT.set()
    
    global_variables.console.print("Recorder: Stopped.")

    ####  END OF RECORDER_THREAD  ###
    