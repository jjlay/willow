

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

import os
from dotenv import load_dotenv
from pathlib import Path


###############################################################################
#
#  Global Variables
#
###############################################################################

import global_variables


###############################################################################
#
#  FUNCTION: load_config()
#
###############################################################################

def load_config() :
    current_file_path = Path(__file__).resolve()
    current_path = current_file_path.parent

    load_dotenv()
    config_root = os.getenv("CONFIG_ROOT")
    instructions_file = os.getenv("INSTRUCTIONS_FILE")
    history_file = os.getenv("HISTORY_FILE")
    gemini_key_file = os.getenv("GEMINI_KEY_FILE")

    global_variables.global_config_root = (current_path / config_root).resolve()
    global_variables.global_instructions_file = global_variables.global_config_root / instructions_file
    global_variables.global_history_file = global_variables.global_config_root / history_file
    gemini_key_file_path = global_variables.global_config_root / gemini_key_file

    global_variables.console.print(f"[bold green]Configuration Loaded:[/bold green] {global_variables.global_config_root}")
    global_variables.console.print(f"[bold green]Instructions File:[/bold green] {global_variables.global_instructions_file}")
    global_variables.console.print(f"[bold green]History File:[/bold green] {global_variables.global_history_file}")
    global_variables.console.print(f"[bold green]Gemini Key File:[/bold green] {gemini_key_file_path}")

    ##############
    #
    # Check if instructions file exists
    #
    ###############

    if not global_variables.global_instructions_file.exists() :
        global_variables.console.print(f"[bold red]Error:[/bold red] Instructions file not found at {global_variables.global_instructions_file}")
    
        with open(global_variables.global_instructions_file, 'w', encoding='utf-8') as f:
            f.write("You are Willow, a futuristic AI digital assistant. You enjoy helping humans live better lives.")
            f.write('When you reply do not prepend the response with "At yyyy-MM-dd HH:mm:ss, Willow said:". Just send the reply.')
        
        global_variables.console.print(f"[bold green]Created new instructions file at:[/bold green] {global_variables.global_instructions_file}")

            
    ##############
    #
    # Check if history file exists
    #
    ###############
    
    if not global_variables.global_history_file.exists() :
        global_variables.console.print(f"[bold red]Error:[/bold red] History file not found at {global_variables.global_history_file}")
    
        with open(global_variables.global_history_file, 'w', encoding='utf-8') as f:
            # We use json.load() to read the JSON and convert it back to a Python list of dicts
            f.write("[]")
        
        global_variables.console.print(f"[bold green]Created new history file at:[/bold green] {global_variables.global_history_file}")


    ##############
    #
    # Check if Gemini key file exists
    #
    ###############
    
    if not gemini_key_file_path.exists() :
        global_variables.console.print(f"[bold red]Error:[/bold red] Gemini key file not found at {gemini_key_file_path}")
        os.abort()    

    else :
        with open(gemini_key_file_path, 'r', encoding='utf-8') as f:
            global_variables.API_KEY = f.read().strip()
        
        global_variables.console.print(f"[bold green]Gemini Key Loaded Successfully. {global_variables.API_KEY}[/bold green]")

        
    return

    ##  END OF LOAD_CONFIG FUNCTION

