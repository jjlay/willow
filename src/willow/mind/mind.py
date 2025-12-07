
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
#   MODULE: mind.py
#
#   PURPOSE:
#   Willow's mind functionality.
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

import queue


###############################################################################
#
#  Class: Mind
#
###############################################################################

class Mind:
    """Mental Functionality"""

    def __init__(self, mind_queue: queue.Queue):
        """Initialize mind.
        
        Args:
            mind_queue: Queue to listen for mind messages
        """
        self.queue = mind_queue
    
    def run(self) -> None:
        """Listen for messages and process them."""
        while True:
            try:
                msg = self.queue.get(timeout=1)
                if msg.get("type") == "process_thought":
                    self.process_thought(msg)
            except queue.Empty:
                pass
            except Exception as e:
                print(f"Mind Error: {e}")
    
    def process_thought(self, msg: dict) -> None:
        """Process a thought message.
        
        Args:
            msg: Message containing thought text
        """
        thought = msg.get("text")
        print(f"Processing thought: {thought}")
        