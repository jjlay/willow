
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
#   MODULE: client_receive_thread.py
#
#   PURPOSE:
#   Displays messages received from other threads.
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
#  Project Includes
#
###############################################################################



###############################################################################
#
#  FUNCTION: client_receive_thread()
#
###############################################################################

# --- 4. The Client Receive Component (Thread) ---
def client_receive_thread():
    """Receives and displays messages from the Client_Receive_Queue."""
    #console.print("📥 Client Receiver: Ready to display messages.")
    
    # --- Table for chat storage

    history = Table(box=box.ASCII, show_header=False, show_edge=True, show_lines=True, leading=2)
    history.add_column("Sender",  no_wrap=True,    width=20, justify="right")
    history.add_column("Message", no_wrap=False,   width=55, justify="left")
    history.add_column("Timestamp", no_wrap=True, width=25, justify="center")

    # --- Import our past conversations

    for m in global_variables.global_history :
        m_timestamp:str = m["timestamp"]
        m_role:str = m["role"]
        m_username:str = m["username"]
        m_parts = m["parts"]
        m_parts_zero = m_parts[0]
        m_text:str = m_parts_zero["text"]

        my_color:str = "[white]"
        speaker:str = "Unknown"

        if m_role == "user" :
            my_color:str = "[yellow]"
            speaker:str = f"{my_color}{m_username}"

        if m_role == "model" :
            my_color:str = "[cyan]"
            speaker:str = f"{global_variables.LLM_USERNAME}"

        history.add_row(f"{my_color}{speaker}", f"{my_color}{m_text}", f"{my_color}{m_timestamp}")


    # --- Main conversation loop

    while not global_variables.STOP_EVENT.is_set():
        try:
            stuff = global_variables.Client_Receive_Queue.get(timeout=0.1)
            speaker = stuff[0]
            message = stuff[1]

            # Overwrite the current input line to display the message cleanly

            my_color = "[white]"
            role = "unknown"

            if speaker == "Server" :
                my_color = "[magenta]"

            if speaker == "JJ" :
                my_color = "[yellow]"
                role = "user"

            if speaker == "Willow" :
                my_color = "[cyan]"
                role = "model"

            # Get the current local date and time
            now = datetime.now()
            now_formatted:str = now.strftime("%Y-%m-%d %H:%M:%S")

            history.add_row(f"{my_color}{speaker}", f"{my_color}{message}", f"{my_color}{now_formatted}")

            global_variables.console.print(history)

            global_variables.Client_Receive_Queue.task_done()
            
        except queue.Empty:
            continue
        except Exception as e:
            global_variables.console.print(f"Client Receive error: {e}")
            global_variables.STOP_EVENT.set()
    
    global_variables.console.print("📥 Client Receiver: Stopped.")

    ####  END OF CLIENT_RECEIVE_THREAD  ###
    