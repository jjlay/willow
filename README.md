
# willow

## About

Willow is an AI digital assistant. At the moment, it only has chat capabilities with memory. It uses the Google Gemini models available in AI Studio.

## Installation

1. Clone the repo.

2. Create a virtual Python environment in the `src` folder. This is performed by calling your installed Python:
    `/usr/local/bin/python3.14 -m venv .venv`

3. Activate the new environment:
   `source .venv/bin/activate`

4. Install the Python dependencies.
`pip install -r requirements.txt`

5. Modify the `.env` file in `src`.
     1. Set `CONFIG_ROOT` to the relative path of the folder containing the three configuration files. For example, if your folder structure was:

		```
		/
		+-- /home/
		    +-- /home/myname/
		        +-- /home/myname/projects/
		            +-- /home/myname/projects/willow/            <-- Cloned repo
		                +-- /home/myname/projects/willow/src/    <-- Cloned repo src folder
		            +-- /home/myname/projects/willowconfig/      <-- Configuration folder outside project            
		```

		Then your `CONFIG_ROOT` would be `CONFIG_ROOT = "../../willowconfig/"`
     
     2. If neither the `instructions.txt` nor the `history.json` file exists, they will be created. 
     3. Modify the system prompt file `instructions.txt` to meet your needs.
     4. Be extremely careful editing the `history.json` file. It can be corrupted easily at which point you need to edit the file to repair it or simply delete it and start over.
     5. You must create the `gemini_key.txt` file manually. It contains a single line with your Gemini API key from AI Studio. This file is simply loaded into a variable and sent with calls to the Google API.

## Launching

1. Activate the virtual environment. From the project's `src` folder (where the virtual environment you created is), type:
`source .venv/bin/activate`

2. Run the application from the `src` folder:
   `python main.py`

3. If an `instructions.txt` file is not found, it creates a simple one:
   ```
   You are Willow, a futuristic AI digital assistant.  
   You enjoy helping humans live better lives.
   When you reply do not prepend the response with "At yyyy-MM-dd HH:mm:ss, Willow said:". Just send the reply.
   ```

4. If the `history.json` file is not found, it creates an empty one.

## Using

1. When launched, willow provides information about what is happening:

```
(.venv) myname@MYHOST src % python main.py
**Configuration Loaded:**  /Users/myname/src/willowconfig
**Instructions File:**  /Users/myname/src/willowconfig/instructions.txt
**History File:**  /Users/myname/src/willowconfig/history.json
**Gemini Key File:**  /Users/myname/src/willowconfig/gemini_key.txt
**Error:** Instructions file not found at /Users/myname/src/willowconfig/instructions.txt
**Created new instructions file at:**  /Users/myname/src/willowconfig/instructions.txt
**Error:** History file not found at /Users/myname/src/willowconfig/history.json
**Created new history file at:**  /Users/myname/src/willowconfig/history.json
**Gemini Key Loaded Successfully. AIzaSyBQ-i99MU9g5OUBH0ECEDfq2h8lXVdGC7c**
Server: Starting up and routing messages...

+--------------------------------------------------------------------------------+
| Server | *** Human joined the chat. ***                  | 2025-11-28 11:06:52 |
+--------------------------------------------------------------------------------+
+--------------------------------------------------------------------------------+
| Server | *** Human joined the chat. ***                  | 2025-11-28 11:06:52 |
|        |                                                 |                     |
| Server | *** Willow is online. Say 'hello' to begin! *** | 2025-11-28 11:06:52 |
+--------------------------------------------------------------------------------+

LLM Client **(**Willow**)**: Initializing...
Please enter your username:
```

2. Enter the name you want willow to refer to you as and press `ENTER`.

   ```
   LLM Client **(**Willow**)**: Initializing...

   Please enter your username: myname

   Welcome, myname! You are chatting with Willow. Type 'quit' to exit.
   ```
   
3. Now you can begin chatting!
   ``` 
   Welcome, myname! You are chatting with Willow. Type 'quit' to exit.
   
   Hello willow. How are you?

   +--------------------------------------------------------------------------------+
   | Server | *** Human joined the chat. ***                  | 2025-11-28 11:06:52 |
   |        |                                                 |                     |
   | Server | *** Willow is online. Say 'hello' to begin! *** | 2025-11-28 11:06:52 |
   |        |                                                 |                     |
   | myname | Hello willow. How are you?                      | 2025-11-28 11:16:31 | 
   +--------------------------------------------------------------------------------+
   +--------------------------------------------------------------------------------+
   | Server | *** Human joined the chat. ***                  | 2025-11-28 11:06:52 |
   |        |                                                 |                     |
   | Server | *** Willow is online. Say 'hello' to begin! *** | 2025-11-28 11:06:52 |
   |        |                                                 |                     |
   | myname | Hello willow. How are you?                      | 2025-11-28 11:16:31 | 
   |        |                                                 |                     |
   | Willow | Hello! I am functioning perfectly and ready to  | 2025-11-28 11:16:33 |
   |        | assist you. How can I help you today?           |                     |
   +--------------------------------------------------------------------------------+
   ```

4. The application prints the entire history each time.

5. When you are finished, simply send `quit` as the only message. The threads will end and the history written.

   ```
   +--------------------------------------------------------------------------------+
   | Server | *** Human joined the chat. ***                  | 2025-11-28 11:06:52 |
   |        |                                                 |                     |
   | Server | *** Willow is online. Say 'hello' to begin! *** | 2025-11-28 11:06:52 |
   |        |                                                 |                     |
   | myname | Hello willow. How are you?                      | 2025-11-28 11:16:31 | 
   |        |                                                 |                     |
   | Willow | Hello! I am functioning perfectly and ready to  | 2025-11-28 11:16:33 |
   |        | assist you. How can I help you today?           |                     |
   +--------------------------------------------------------------------------------+
   quit

   Server: Shutting down.
   LLM Client **(**Willow**)**: Shutting down.
   Recorder: Stopped.
   Client Receiver: Stopped.
   All threads cleaned up. Application finished.
   Saver: Stopped.
   (.venv) myname@MYHOST src %
   ```
