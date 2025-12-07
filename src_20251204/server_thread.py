
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
#   MODULE: server_thread.py
#
#   PURPOSE:
#   The orchestrator.
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
import copy
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
#  FUNCTION: server_thread()
#
###############################################################################

# --- 3. The Server Component (Thread) - Now a Router ---
def server_thread():
    """Acts as the central router: reads from input queues and broadcasts to output queues."""
    global_variables.console.print("Server: Starting up and routing messages...")
    
    # Broadcast initial system messages to the Human Client
    global_variables.Client_Receive_Queue.put(["Server", f"*** {global_variables.HUMAN_USERNAME} joined the chat. ***"])
    global_variables.Client_Receive_Queue.put(["Server", f"*** {global_variables.LLM_USERNAME} is online. Say 'hello' to begin! ***"])
    

    while not global_variables.STOP_EVENT.is_set():
        try:
            now = datetime.now()
            now_formatted:str = now.strftime("%Y-%m-%d %H:%M:%S")

            # 3a. Check for incoming messages from the Human Client
            human_message = global_variables.Server_Queue.get(timeout=0.05)
            

            if human_message.startswith("SYSTEM_QUIT"):
                # Handle the explicit quit command from the client
                global_variables.Server_Queue.task_done()
                continue

            # Determine if the human is talking to the LLM or to another simulated user (not implemented)
            # For simplicity, we'll assume ALL human messages go to the LLM for a response.
            #console.print(f"Server routing Human message: {human_message}")

            global_variables.LLM_In_Queue.put((global_variables.HUMAN_USERNAME, human_message))
            
            # Put the human's message into the general receive queue so the human sees their own message
            global_variables.Client_Receive_Queue.put([f"{global_variables.HUMAN_USERNAME}",  f"{human_message}"])
            
            # Add the message to the recording
            global_variables.Recorder_In_Queue.put([f"{global_variables.HUMAN_USERNAME}",  f"{human_message}", "user", f"{now_formatted}"])

            global_variables.Server_Queue.task_done()
            
        except queue.Empty:
            pass # No human message, check LLM next

        try:
            now = datetime.now()
            now_formatted:str = now.strftime("%Y-%m-%d %H:%M:%S")

            # 3b. Check for outgoing messages from the LLM
            sender, llm_response = global_variables.LLM_Out_Queue.get(timeout=0.05)
            
            # Broadcast the LLM's response to the Human Client
            global_variables.Client_Receive_Queue.put([f"{sender}", f"{llm_response}"])
            
            # Add the message to the recording
            global_variables.Recorder_In_Queue.put([f"{sender}",  f"{llm_response}", "model", f"{now_formatted}"])

            global_variables.LLM_Out_Queue.task_done()
            
        except queue.Empty:
            pass # No LLM message, continue

        except Exception as e:
            global_variables.console.print(f"Server error: {e}")
            global_variables.STOP_EVENT.set()
    
    global_variables.console.print("Server: Shutting down.")

    ###  END OF SERVER_THREAD  ###
    
