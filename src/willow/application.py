
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
#   MODULE: application.py
#
#   PURPOSE:
#   The primary application class that initializes the UI and manages threads.
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

import tkinter as tk
import threading
import queue
from typing import Dict, Any, List, Optional


###############################################################################
#
#  Project Specific Imports
#
###############################################################################

from .ui import WidgetFactory, WidgetEventHandlers
from .image_utils import GifAnimator
from .threads import (
    GifDisplayController,
    PngDisplayController,
    TextDisplayController,
    InputMonitorController,
    Orchestrator,
    Housekeeper,
    Archivist
)


###############################################################################
#
#  Class: WillowApplication
#
###############################################################################

class WillowApplication:
    """Main Willow application class managing UI and thread coordination.
    
    Architecture:
    - Widgets 1-7: Seven UI components with responsive grid layout
    - Threads 1-7: Widget content controllers
    - Thread 8: Orchestrator (routes messages between threads)
    - Thread 9: Housekeeper (runs every 60 seconds)
    - Thread 10: Archivist (stores JSON messages)
    - Thread 11: LLM
    """
    
    def __init__(self, root: tk.Tk):
        """Initialize Willow application.
        
        Args:
            root: The root tkinter window
        """
        self.root = root
        self.root.title("Willow")
        self.root.geometry("1200x800")
        
        # Create thread queues
        self.queues: Dict[int, queue.Queue] = {
            i: queue.Queue() for i in range(1, 11)  # Threads 1-10
        }
        
        # Setup UI
        self.widgets = WidgetFactory.create_all_widgets(root)
        
        # Setup GIF animator
        self.gif_animator = GifAnimator(self.widgets['widget1'], root)
        
        # Setup event handlers
        self.event_handlers = WidgetEventHandlers(self.queues)
        self.widgets['widget7'].bind(
            "<Return>",
            lambda e: self.event_handlers.on_widget7_input(e, self.widgets['widget7'])
        )
        
        # Start all threads
        self.threads = []
        self.start_threads()
        
        # Start monitoring queues
        self.monitor_queues()
    
    def start_threads(self) -> None:
        """Start all 10 worker threads."""
        thread_specs = [
            ("Thread 1: Widget 1 Controller", self._create_gif_controller),
            ("Thread 2: Widget 2 Controller", self._create_png_controller(2)),
            ("Thread 3: Widget 3 Controller", self._create_png_controller(3)),
            ("Thread 4: Widget 4 Controller", self._create_png_controller(4)),
            ("Thread 5: Widget 5 Controller", self._create_png_controller(5)),
            ("Thread 6: Widget 6 Controller", self._create_text_controller),
            ("Thread 7: Widget 7 Controller", self._create_input_monitor),
            ("Thread 8: Orchestrator", self._create_orchestrator),
            ("Thread 9: Housekeeper", self._create_housekeeper),
            ("Thread 10: Archivist", self._create_archivist),
            ("Thread 11: Mind", self._create_mind),
        ]
        
        for name, controller_creator in thread_specs:
            controller = controller_creator()
            thread = threading.Thread(name=name, target=controller.run, daemon=True)
            thread.start()
            self.threads.append(thread)
    
    def _create_mind(self) :
        """Create Mind thread (Thread 11)."""
        from .mind.mind import Mind  # Import here to avoid circular dependency
        return Mind(self.queues[10])
    
    def _create_gif_controller(self) -> GifDisplayController:
        """Create GIF display controller (Thread 1)."""
        return GifDisplayController(self.queues[1], self.gif_animator)
    
    def _create_png_controller(self, thread_id: int):
        """Create PNG display controller factory (Threads 2-5)."""
        def create():
            return PngDisplayController(
                self.queues[thread_id],
                self.widgets[f'widget{thread_id}'],
                thread_id
            )
        return create
    
    def _create_text_controller(self) -> TextDisplayController:
        """Create text display controller (Thread 6)."""
        return TextDisplayController(
            self.queues[6],
            self.widgets['widget6'],
            lambda text: WidgetFactory.append_to_widget6(self.widgets['widget6'], text)
        )
    
    def _create_input_monitor(self) -> InputMonitorController:
        """Create input monitor controller (Thread 7)."""
        return InputMonitorController(self.queues[7])
    
    def _create_orchestrator(self) -> Orchestrator:
        """Create orchestrator (Thread 8)."""
        return Orchestrator(self.queues[8], self.queues[6], self.queues[10])
    
    def _create_housekeeper(self) -> Housekeeper:
        """Create housekeeper (Thread 9)."""
        return Housekeeper(maintenance_interval=60)
    
    def _create_archivist(self) -> Archivist:
        """Create archivist (Thread 10)."""
        return Archivist(self.queues[10])
    
    def monitor_queues(self) -> None:
        """Monitor queues for UI updates from threads."""
        try:
            # This runs periodically to process any UI-related messages
            pass
        except Exception as e:
            print(f"Queue monitoring error: {e}")
        finally:
            self.root.after(100, self.monitor_queues)
