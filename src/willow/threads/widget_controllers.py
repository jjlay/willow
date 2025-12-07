"""Widget controller threads (Threads 1-7) for Willow."""

import queue
from typing import Callable
from ..image_utils import GifAnimator, ImageDisplayer

######################################################
#
#  Class: WidgetControllerBase
#
########################################################

class WidgetControllerBase:

    #####################################################
    #
    #  Function: __init__()
    #
    #  Description:
    #     Base class for widget controller threads.
    #
    #  Parameters:
    #     queue_obj - Queue to listen for commands
    #     thread_id - Thread identifier number
    #
    #  Returns: 
    #     None
    #
    ######################################################

    def __init__(self, queue_obj: queue.Queue, thread_id: int):

        self.queue = queue_obj
        self.thread_id = thread_id
    
    ###  END OF __INIT__()  ###


    #####################################################
    #
    #  Function: run()
    #
    #  Description:
    #     Run the controller loop. Override in subclasses.
    #
    #  Parameters:
    #     None
    #
    #  Returns: 
    #     None
    #
    ######################################################

    def run(self) -> None:
        """Run the controller loop. Override in subclasses."""
        raise NotImplementedError

    ###  END OF RUN()  ###


######################################################
#
#  Class: GifDisplayController
#
########################################################

class GifDisplayController(WidgetControllerBase):

    #####################################################
    #
    #  Function: __init__()
    #
    #  Description:
    #    Thread 1: Controls GIF animation in Widget 1. 
    #    Initialize GIF display controller.
    #
    #  Parameters:
    #    queue_obj: Queue to listen for GIF display commands
    #    gif_animator: GifAnimator instance for animation control
    #
    #  Returns: 
    #     None
    #
    ######################################################
    
    def __init__(self, queue_obj: queue.Queue, gif_animator: GifAnimator):

        super().__init__(queue_obj, 1)
        self.animator = gif_animator

    ###  END OF __INIT__()  ###


    #####################################################
    #
    #  Function: run()
    #
    #  Description:
    #     Listen for GIF display messages and load/animate GIFs.
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
                if msg.get("type") == "display_gif":
                    filepath = msg.get("filepath")
                    self.animator.load(filepath)
            except queue.Empty:
                pass
            except Exception as e:
                print(f"Widget 1 Controller Error: {e}")

    ###  END OF RUN()  ###


######################################################
#
#  Class: PngDisplayController
#
########################################################

class PngDisplayController(WidgetControllerBase):
    
    #####################################################
    #
    #  Function: __init__()
    #
    #  Description:
    #    Base class for PNG display controllers (Threads 2-5).
    #    Initialize PNG display controller.
    #
    #  Parameters:
    #    queue_obj: Queue to listen for PNG display commands
    #    widget: tkinter widget to display image in
    #    thread_id: Thread identifier (2-5)
    #
    #  Returns: 
    #     None
    #
    ######################################################

    def __init__(self, queue_obj: queue.Queue, widget, thread_id: int):

        super().__init__(queue_obj, thread_id)
        self.widget = widget

    ###  END OF __INIT__()  ###


    #####################################################
    #
    #  Function: run()
    #
    #  Description:
    #     Listen for PNG display messages and display images.
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
                if msg.get("type") == "display_image":
                    filepath = msg.get("filepath")
                    ImageDisplayer.display(self.widget, filepath)
            except queue.Empty:
                pass
            except Exception as e:
                print(f"Widget {self.thread_id} Controller Error: {e}")

    ###  END OF RUN()  ###


######################################################
#
#  Class: InputMonitorController
#
########################################################

class TextDisplayController(WidgetControllerBase):
    """"""
    
    #####################################################
    #
    #  Function: __init__()
    #
    #  Description:
    #    Thread 6: Controls read-only text display in Widget 6.
    #    Initialize text display controller.
    #
    #  Parameters:
    #    queue_obj: Queue to listen for text append commands
    #    text_widget: scrolledtext widget to append text to
    #    append_callback: Function to append text safely
    #
    #  Returns: 
    #     None
    #
    ######################################################

    def __init__(self, queue_obj: queue.Queue, text_widget, append_callback: Callable):

        super().__init__(queue_obj, 6)
        self.widget = text_widget
        self.append_callback = append_callback

    ###  END OF __INIT__()  ###
    

    #####################################################
    #
    #  Function: run()
    #
    #  Description:
    #     Listen for text append messages and append to widget.
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
                if msg.get("type") == "append_text":
                    text = msg.get("text", "")
                    self.append_callback(text)
            except queue.Empty:
                pass
            except Exception as e:
                print(f"Widget 6 Controller Error: {e}")

    ###  END OF RUN()  ###


######################################################
#
#  Class: InputMonitorController
#
########################################################

class InputMonitorController(WidgetControllerBase):

    #####################################################
    #
    #  Function: __init__()
    #
    #  Description:
    #     Thread 7: Monitors input text box in Widget 7 (passive).
    #     Initialize input monitor controller.
    #
    #  Parameters:
    #     queue_obj: Queue to listen for input messages
    #
    #  Returns: 
    #     None
    #
    ######################################################

    def __init__(self, queue_obj: queue.Queue):

        super().__init__(queue_obj, 7)

    ###  END OF __INIT__()  ###


    #####################################################
    #
    #  Function: run()
    #
    #  Description:
    #     Monitor queue (UI input handled via event binding).
    #
    #  Parameters:
    #     None
    #
    #  Returns: 
    #     None
    #
    ######################################################

    def run(self) -> None:
        """"""
        while True:
            try:
                msg = self.queue.get(timeout=1)
                # Thread 7 monitors but doesn't take action
                # UI input events are handled by event bindings
            except queue.Empty:
                pass
            except Exception as e:
                print(f"Widget 7 Controller Error: {e}")

    ###  END OF RUN()  ###
