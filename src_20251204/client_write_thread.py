

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
#   MODULE: client_write_thread.py
#
#   PURPOSE:
#   Accepts input from the human user and sends it to the server.
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
#  FUNCTION: client_write_thread()
#
###############################################################################

# --- 5. The Client Write Component (Input Thread) ---
def client_write_thread():
    """Reads input and puts messages into Server_Queue."""
    global_variables.HUMAN_USERNAME = input("Please enter your username: ")
    global_variables.console.print(f"\nWelcome, {global_variables.HUMAN_USERNAME}! You are chatting with {global_variables.LLM_USERNAME}. Type 'quit' to exit.\n")
    
    while not global_variables.STOP_EVENT.is_set():
        try:
            user_input = input("")
            
            if user_input.lower() == 'quit':
                global_variables.STOP_EVENT.set()
                # Send a final system message to the server for cleanup
                global_variables.Server_Queue.put(f"SYSTEM_QUIT: {global_variables.HUMAN_USERNAME} is leaving.")
                break
                
            # Put the user's message into the Server's input queue
            global_variables.Server_Queue.put(user_input)
            
        except EOFError:
            global_variables.console.print("Client Write: EOF received.")
            global_variables.STOP_EVENT.set()
        except Exception as e:
            global_variables.console.print(f"Client Write error: {e}")
            global_variables.STOP_EVENT.set()

    ###  END OF CLIENT_WRITE_THREAD  ###
    