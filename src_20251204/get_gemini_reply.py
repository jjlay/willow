

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
#   MODULE: get_gemini_reply.py
#
#   PURPOSE:
#   Calls the Gemini API with the predefined instructions and the user's
#   input. Returns the reply from Gemini.
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

import os
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

import global_variables


###############################################################################
#
#  FUNCTION: get_gemini_reply
#
###############################################################################

def get_gemini_reply(sender:str, user_prompt: str, system_instructions: str, model_name: str = 'gemini-2.5-flash') -> str:
    """
    Calls the Gemini model with specific system instructions and a user prompt.

    Args:
        user_prompt: The main input/question from the user.
        system_instructions: The instructions to guide the model's behavior.
        model_name: The name of the Gemini model to use (default is 'gemini-2.5-flash').

    Returns:
        The text response from the Gemini model.
    """
    try:
        # The client automatically picks up the API key from the environment variable.
        client = genai.Client(api_key = global_variables.API_KEY)

        # Configure the request with system instructions
        config = types.GenerateContentConfig(
            system_instruction=system_instructions
        )

        now = datetime.now()
        now_formatted:str = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Add the history
        h = []

        with global_variables.global_content_lock:
            h = copy.deepcopy(global_variables.global_content)

        #c = Content(role = "user", parts = [Part.from_text(text=f"At {now_formatted}, {sender} said: {user_prompt}")])

        #h.append(c)

        #filepath = os.path.join(".", "debug", f"content_{now.strftime("%Y-%m-%d-%H-%M-%S")}.txt")

        #try :
            #string_list = [str(item) for item in h]
            #content_to_save = '\n'.join(string_list)

            #with open(filepath, "w", encoding="utf-8") as f:
                #f.write(content_to_save)

        #except Exception as e:
            #global_variables.console.print(f"Could not write content to {filepath}: {e}")

        # Call the API
        response = client.models.generate_content(
            model=model_name,
            contents=h,
            config=config,
        )

        # Return the text part of the response
        return response.text

    except Exception as e:
        return f"An error occurred: {e}"

    ###  END OF GET_gemini_reply  ###
