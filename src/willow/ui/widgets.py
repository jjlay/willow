
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
#   MODULE: widgets.py
#
#   PURPOSE:
#   Factory for creating and laying out all Willow widgets.
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
from tkinter import scrolledtext
from typing import Tuple, Dict


###############################################################################
#
#  Class: WidgetFactory
#
###############################################################################
 
class WidgetFactory:
    """Factory for creating and laying out all Willow widgets."""
    
    @staticmethod
    def create_all_widgets(root: tk.Tk) -> Dict[str, tk.Widget]:
        """Create and layout all seven widgets using grid geometry manager.
        
        Args:
            root: The root tkinter window
            
        Returns:
            Dictionary containing all created widgets
        """
        # Configure grid weights for responsiveness
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=2)
        root.grid_columnconfigure(2, weight=1)
        
        widgets = {}
        
        # Widget 1: GIF display (upper left, 25% x 25%)
        widgets['widget1'] = tk.Label(
            root, 
            bg="lightblue", 
            text="Widget 1\n(GIF)", 
            font=("Arial", 10)
        )
        widgets['widget1'].grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=2, pady=2)
        root.grid_rowconfigure(0, weight=1)
        
        # Widget 2: PNG display (below Widget 1, 25% x 25%)
        widgets['widget2'] = tk.Label(
            root, 
            bg="lightgreen", 
            text="Widget 2\n(PNG)", 
            font=("Arial", 10)
        )
        widgets['widget2'].grid(row=1, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=2, pady=2)
        root.grid_rowconfigure(1, weight=1)
        
        # Widget 3: PNG display (below Widget 2, 25% x 25%)
        widgets['widget3'] = tk.Label(
            root, 
            bg="lightyellow", 
            text="Widget 3\n(PNG)", 
            font=("Arial", 10)
        )
        widgets['widget3'].grid(row=2, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=2, pady=2)
        root.grid_rowconfigure(2, weight=1)
        
        # Widget 4: PNG display (below Widget 3, 25% x 25%)
        widgets['widget4'] = tk.Label(
            root, 
            bg="lightcoral", 
            text="Widget 4\n(PNG)", 
            font=("Arial", 10)
        )
        widgets['widget4'].grid(row=3, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=2, pady=2)
        root.grid_rowconfigure(3, weight=1)
        
        # Widget 5: PNG display (right of Widget 1, 50% x 100%)
        widgets['widget5'] = tk.Label(
            root, 
            bg="plum", 
            text="Widget 5\n(PNG)", 
            font=("Arial", 10)
        )
        widgets['widget5'].grid(row=0, column=1, rowspan=4, columnspan=1, sticky="nsew", padx=2, pady=2)
        
        # Widget 6: Read-only scrollable text (upper right)
        widget6_frame = tk.Frame(root, bg="white", relief="sunken", borderwidth=1)
        widget6_frame.grid(row=0, column=2, rowspan=3, columnspan=1, sticky="nsew", padx=2, pady=2)
        widget6_frame.grid_rowconfigure(0, weight=1)
        widget6_frame.grid_columnconfigure(0, weight=1)
        
        widgets['widget6'] = scrolledtext.ScrolledText(
            widget6_frame,
            height=15,
            width=30,
            state="disabled",
            wrap="word",
            bg="white",
            fg="black"
        )
        widgets['widget6'].grid(row=0, column=0, sticky="nsew")
        
        # Widget 7: User input text box (below Widget 6)
        widget7_frame = tk.Frame(root, bg="white", relief="sunken", borderwidth=1)
        widget7_frame.grid(row=3, column=2, rowspan=1, columnspan=1, sticky="nsew", padx=2, pady=2)
        widget7_frame.grid_rowconfigure(0, weight=1)
        widget7_frame.grid_columnconfigure(0, weight=1)
        
        widgets['widget7'] = tk.Text(
            widget7_frame,
            height=5,
            width=30,
            wrap="word",
            bg="white",
            fg="black"
        )
        widgets['widget7'].grid(row=0, column=0, sticky="nsew")
        
        return widgets
    
    @staticmethod
    def append_to_widget6(widget6: scrolledtext.ScrolledText, text: str) -> None:
        """Append text to Widget 6 (read-only text box).
        
        Args:
            widget6: The scrolled text widget
            text: Text to append
        """
        try:
            widget6.config(state="normal")
            widget6.insert(tk.END, text)
            widget6.see(tk.END)
            widget6.config(state="disabled")
        except Exception as e:
            print(f"Error appending to Widget 6: {e}")
