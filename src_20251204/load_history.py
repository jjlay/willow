

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
#   MODULE: load_history.py
#
#   PURPOSE:
#   Imports the historical conversations as a JSON object.
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

import json
import threading
import queue
import time
import sys


###############################################################################
#
#  Gemini Imports
#
###############################################################################

from google.genai.types import Content, Part


###############################################################################
#
#  Global Variables
#
###############################################################################

import global_variables


###############################################################################
#
#  FUNCTION: load_history()
#
###############################################################################

def load_history(path) :
    """Loads the chat history from a JSON file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            # We use json.load() to read the JSON and convert it back to a Python list of dicts
            loaded_history = json.load(f)

            for entry in loaded_history:
                role = entry.get("role", "unknown")
                username = entry.get("username", "N/A")
                timestamp = entry.get("timestamp", "N/A")
                parts = entry.get("parts", [])

                first_item = parts[0] if parts else {}
                text = first_item.get("text", "")

                new_text = f"At {timestamp}\, {username} said: {text}"
                print(f"[bold green]Loaded entry:[/bold green] {new_text}")
                print(f"The length of new_text is {len(new_text)} characters.")

                new_part = Part.from_text(text=new_text)
                new_parts = [new_part]

                c = Content(role=role, parts=new_parts)
                
                with global_variables.global_content_lock :
                    global_variables.global_content.append(c)

            return loaded_history
    
    except FileNotFoundError:
        console.print(f"⚠️ File not found at {path}. Returning empty list.")
        return []
    
    except json.JSONDecodeError as e:
        console.print(f"❌ Error decoding JSON: {e}")
        return []

    return

    ###  END OF LOAD_HISTORY  ###

