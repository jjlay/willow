

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
#   MODULE: main.py
#
#   PURPOSE:
#   The main entry point.
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

import threading
import queue
import time
import sys

from google import genai
from google.genai import types
from google.genai.types import Content, Part

from rich.console import Console
from rich.pretty import pprint
from rich import print
from rich.table import Table
from rich import box

import json
from datetime import datetime
import copy
from dotenv import load_dotenv


###############################################################################
#
#  Project Includes
#
###############################################################################

from get_gemini_reply import get_gemini_reply
from load_history import load_history
from save_history import save_history
from load_instructions import load_instructions
from save_instructions import save_instructions
from llm_client_thread import llm_client_thread
from server_thread import server_thread
from client_receive_thread import client_receive_thread
from client_write_thread import client_write_thread
from saver_thread import saver_thread
from recorder_thread import recorder_thread
from load_config import load_config


###############################################################################
#
#  Global Variables
#
###############################################################################

import global_variables


###############################################################################
#
#  ENTRY POINT
#
###############################################################################

if __name__ == "__main__":
    load_config()
    
    # --- Saver Thread
    saver_t = threading.Thread(target=saver_thread, name='Saver-Thread')

    # --- Server Thread
    server_t = threading.Thread(target=server_thread, name='Server-Thread')

    # --- Recorder Thread
    recorder_t = threading.Thread(target=recorder_thread, name='Recorder-Thread')

    # --- Client Receiver for Human
    receive_t = threading.Thread(target=client_receive_thread, name='Client-Receive-Thread')

    # --- Client Transmission for Human
    write_t = threading.Thread(target=client_write_thread, name='Client-Write-Thread')

    # --- LLM Thread
    llm_t = threading.Thread(target=llm_client_thread, name='LLM-Client-Thread')
    


    try:
        # Start all threads
        saver_t.start()
        time.sleep(1)

        recorder_t.start()
        time.sleep(1)

        server_t.start()
        time.sleep(1)

        receive_t.start()
        time.sleep(1)

        llm_t.start() # Start the LLM thread
        time.sleep(1)
        
        # Start the write thread and wait for it to finish
        write_t.start()
        write_t.join()

    except KeyboardInterrupt:
        global_variables.console.print("\n\nApplication manually stopped.")
    finally:
        # Gracefully stop the other threads
        global_variables.STOP_EVENT.set()
        server_t.join()
        receive_t.join()
        llm_t.join()
        recorder_t.join()
        
        global_variables.console.print("\nAll threads cleaned up. Application finished.")

###  END OF ENTRY POINT CODE  ###
        