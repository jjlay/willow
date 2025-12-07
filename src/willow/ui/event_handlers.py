"""Event handlers for Willow UI interactions."""

import tkinter as tk
import queue
from typing import Dict


class WidgetEventHandlers:
    """Handles UI events from widgets."""
    
    def __init__(self, queues: Dict[int, queue.Queue]):
        """Initialize event handlers.
        
        Args:
            queues: Dictionary of queues for thread communication
        """
        self.queues = queues
    
    def on_widget7_input(self, event: tk.Event, widget7: tk.Text) -> str:
        """Handle user input from Widget 7 (input text box).
        
        When user presses ENTER, sends the text to the orchestrator (Thread 8).
        
        Args:
            event: The tkinter event object
            widget7: The text widget containing user input
            
        Returns:
            "break" to prevent default newline insertion
        """
        text = widget7.get("1.0", tk.END).strip()
        if text:
            # Send to orchestrator (Thread 8)
            self.queues[8].put({"type": "user_input", "text": text})
            # Clear input
            widget7.delete("1.0", tk.END)
        return "break"  # Prevent newline insertion
