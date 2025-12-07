

import queue
from typing import Dict, Any, List


class Archivist:

    #####################################################
    #
    #  Function: __init__()
    #
    #  Description:
    #     Thread 10: Stores messages as JSON in archive.
    #
    #  Parameters:
    #     archivist_queue - Queue to listen for archive messages
    #
    #  Returns: 
    #     None
    #
    ######################################################
    
    def __init__(self, archivist_queue: queue.Queue):

        self.queue = archivist_queue
        self.archive: List[Dict[str, Any]] = []
    
    ###  END OF __INIT__()  ###


    #####################################################
    #
    #  Function: run()
    #
    #  Description:
    #     Listen for messages and store them in archive.
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
                if msg.get("type") == "archive_message":
                    self.archive_message(msg)
            except queue.Empty:
                pass
            except Exception as e:
                print(f"Archivist Error: {e}")
    
    ###  END OF RUN()  ###


    #####################################################
    #
    #  Function: archive_message()
    #
    #  Description:
    #     Store message in archive with timestamp.
    #
    #  Parameters:
    #     msg - Message containing text and timestamp
    #
    #  Returns: 
    #     None
    #
    ######################################################

    def archive_message(self, msg: Dict) -> None:

        archive_entry = {
            "timestamp": msg.get("timestamp"),
            "message": msg.get("text")
        }
        self.archive.append(archive_entry)
        print(f"Archived: {archive_entry}")
    
    ###  END OF ARCHIVE_MESSAGE()  ###


    #####################################################
    #
    #  Function: get_archive()
    #
    #  Description:
    #     Get the current archive.
    #
    #  Parameters:
    #     None
    #
    #  Returns: 
    #     List of archived messages
    #
    ######################################################

    def get_archive(self) -> List[Dict[str, Any]]:

        return self.archive.copy()

    ###  END OF GET_ARCHIVE()  ###

    