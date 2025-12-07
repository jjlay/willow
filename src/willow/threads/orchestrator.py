"""Orchestrator thread (Thread 8) for routing messages between widgets."""

import queue
import time
from typing import Dict


class Orchestrator:

    #####################################################
    #
    #  Function: __init__()
    #
    #  Description:
    #     Thread 8: Routes messages between widget controllers and archiving.
    #     This function initializes the orchestrator with necessary queues.
    #
    #  Parameters:
    #     orchestrator_queue - Queue to listen for user input messages
    #     widget6_queue - Queue for sending text to Widget 6
    #     archivist_queue - Queue for sending messages to archivist
    #
    #  Returns: 
    #     None
    #
    ######################################################

    def __init__(self, orchestrator_queue: queue.Queue, widget6_queue: queue.Queue, 
                 archivist_queue: queue.Queue):

        self.queue = orchestrator_queue
        self.widget6_queue = widget6_queue
        self.archivist_queue = archivist_queue

        ###  END OF __INIT__()  ###


    #####################################################
    #
    #  Function: run()
    #
    #  Description:
    #     Listen for messages and route them to appropriate destinations.
    #
    #  Parameters:
    #     None
    #
    #  Returns: 
    #     None
    #
    ######################################################

    def run(self) -> None:

        while True:
            try:
                msg = self.queue.get(timeout=1)
                if msg.get("type") == "user_input":
                    self.handle_user_input(msg)
            except queue.Empty:
                pass
            except Exception as e:
                print(f"Orchestrator Error: {e}")
    
    ###  END OF RUN()  ###

    
    #####################################################
    #
    #  Function: handle_user_input()
    #
    #  Description:
    #     Route user input messages to Widget 6 and Archivist.
    #
    #  Parameters:
    #     msg - Message containing user input text
    #
    #  Returns: 
    #     None
    #
    ######################################################

    def handle_user_input(self, msg: Dict) -> None:

        text = msg.get("text")
        timestamp = time.time()
        
        # Send to Widget 6 (Thread 6) with timestamp
        self.widget6_queue.put({
            "type": "append_text",
            "text": f"[{time.strftime('%H:%M:%S', time.localtime(timestamp))}] {text}\n"
        })
        
        # Send to Archivist (Thread 10)
        self.archivist_queue.put({
            "type": "archive_message",
            "text": text,
            "timestamp": timestamp
        })

        # Send to Mind (Thread 11)
        self.archivist_queue.put({
            "type": "process_thought",
            "text": text
        })  

    ###  End of handle_user_input()  ###
