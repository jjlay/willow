

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
#   MODULE: housekeeper.py
#
#   PURPOSE:
#   To be implemented: Thread 9 that runs maintenance tasks every 60 seconds.
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

import time


###############################################################################
#
#  Class: Housekeeper
#
###############################################################################

class Housekeeper:
    
    #####################################################
    #
    #  Function: __init__()
    #
    #  Description:
    #     Thread 9: Runs maintenance tasks every 60 seconds.
    #
    #  Parameters:
    #     maintenance_interval - Seconds between maintenance cycles (default: 60)
    #
    #  Returns: 
    #     None
    #
    ######################################################

    def __init__(self, maintenance_interval: int = 60):

        self.interval = maintenance_interval

    ###  END OF __INIT__()  ###

    
    #####################################################
    #
    #  Function: run()
    #
    #  Description:
    #     Thread 9: Runs maintenance tasks every 60 seconds.
    #
    #  Parameters:
    #     maintenance_interval - Seconds between maintenance cycles (default: 60)
    #
    #  Returns: 
    #     None
    #
    ######################################################

    def run(self) -> None:

        while True:
            try:
                time.sleep(self.interval)
                self.perform_maintenance()
            except Exception as e:
                print(f"Housekeeper Error: {e}")
    
    ###  END OF RUN()  ###


    #####################################################
    #
    #  Function: perform_maintenance()
    #
    #  Description:
    #     Perform maintenance tasks. Override to add custom logic.
    #
    #  Parameters:
    #     None
    #
    #  Returns: 
    #     None
    #
    ######################################################

    def perform_maintenance(self) -> None:

        print(f"Housekeeper: Running maintenance at {time.strftime('%H:%M:%S')}")

    ###  END OF PERFORM_MAINTENANCE()  ###

