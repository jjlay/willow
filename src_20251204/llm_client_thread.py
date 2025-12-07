
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
#   MODULE: llm_client_thread.py
#
#   PURPOSE:
#   This allows the LLM to pretend to be another user to the server.
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
#  Project Includes
#
###############################################################################

from load_history import load_history
from load_instructions import load_instructions
from get_gemini_reply import get_gemini_reply


###############################################################################
#
#  FUNCTION: llm_client_thread()
#
###############################################################################

# --- 2. The LLM Component (Thread) ---
def llm_client_thread():
    """Simulates the LLM's thought process and response generation."""
    global_variables.console.print(f"\n🧠 LLM Client ({global_variables.LLM_USERNAME}): Initializing...")
    
    my_instructions = load_instructions(global_variables.global_instructions_file)

    while not global_variables.STOP_EVENT.is_set():
        try:
            # Check for incoming messages from the Server (directed to the LLM)
            message_tuple = global_variables.LLM_In_Queue.get(timeout=0.1)
            
            sender, message = message_tuple
            
            if sender != "Server" :
                gemini_reply = get_gemini_reply(sender, message, my_instructions)

                # Put the LLM's response into its output queue for the Server to broadcast
                global_variables.LLM_Out_Queue.put((global_variables.LLM_USERNAME, gemini_reply))
            
            global_variables.LLM_In_Queue.task_done()

        except queue.Empty:
            continue
        except Exception as e:
            global_variables.console.print(f"LLM Client error: {e}")
            global_variables.STOP_EVENT.set()
            
    global_variables.console.print(f"🧠 LLM Client ({global_variables.LLM_USERNAME}): Shutting down.")

    ###  END OF LLM_CLIENT_THREAD  ###
    