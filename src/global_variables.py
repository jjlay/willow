
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
#   MODULE: global_variables.py
#
#   PURPOSE:
#   Global variables shared among all threads.
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
from google.genai.types import Content, Part # Import Content and Part classes

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
#  Global Variables
#
###############################################################################

# Google AI Studio API Key
API_KEY:str = ""

console = Console(width=100)


# 1. Thread-Safe Communication Queues
# Human Client Queues
Server_Queue = queue.Queue()             # Human input -> Server
Client_Receive_Queue = queue.Queue()     # Server -> Human output

# LLM Client Queues
LLM_In_Queue = queue.Queue()             # Server -> LLM input
LLM_Out_Queue = queue.Queue()            # LLM output -> Server

# Archival Queue
Recorder_In_Queue = queue.Queue()        # All -> Archivist

# Global variable to control all threads
STOP_EVENT = threading.Event()
HUMAN_USERNAME = "Human" # Placeholder for dynamic input
LLM_USERNAME = "Willow" # LLM's dedicated username


###############################################################################
#
#  Threading Variables
#
###############################################################################

global_history = {}
global_history_lock = threading.Lock()
SAVE_INTERVAL = 10 # Seconds

global_content = []
global_content_lock = threading.Lock()
