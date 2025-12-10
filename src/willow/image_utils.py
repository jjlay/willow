
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
#   MODULE: widget_controllers.py
#
#   PURPOSE:
#   Code that manages the controller threads for each widget in the GUI.
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
from PIL import Image, ImageTk
from typing import List, Optional


class GifAnimator:
    """Handles GIF loading and frame animation."""
    

    #####################################################
    #
    #  Function: __init__()
    #
    #  Description:
    # 
    #
    #  Parameters:
    # 
    #
    #  Returns: 
    #     None
    #
    ######################################################
        
    def __init__(self, widget: tk.Label, root: tk.Tk):
        """Initialize GIF animator.
        
        Args:
            widget: The tkinter Label widget to display the GIF
            root: The root tkinter window for scheduling animations
        """
        self.widget = widget
        self.root = root
        self.frames: List[ImageTk.PhotoImage] = []
        self.current_frame = 0
        self.animation_id: Optional[int] = None
    
    def load(self, filepath: str) -> None:
        """Load GIF file and prepare frames for animation.
        
        Args:
            filepath: Path to the GIF file
        """
        try:
            with Image.open(filepath) as gif:
                self.frames = []
                for frame_idx in range(gif.n_frames):
                    gif.seek(frame_idx)
                    # Resize to fit widget while maintaining aspect ratio
                    frame = gif.convert("RGBA")
                    frame.thumbnail((250, 200), Image.Resampling.LANCZOS)
                    self.frames.append(ImageTk.PhotoImage(frame))
                
                self.current_frame = 0
                self.animate()
        except Exception as e:
            print(f"Error loading GIF: {e}")
    
    def animate(self) -> None:
        """Cycle through GIF frames every 100ms."""
        if not self.frames:
            return
        
        self.widget.config(image=self.frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.animation_id = self.root.after(100, self.animate)
    
    def stop(self) -> None:
        """Stop animation and cleanup."""
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
        self.frames.clear()
        self.current_frame = 0


class ImageDisplayer:
    """Handles PNG image display with automatic scaling."""
    
    @staticmethod
    def display(widget: tk.Label, filepath: str) -> None:
        """Display PNG image in specified widget.
        
        Args:
            widget: The tkinter Label widget to display the image
            filepath: Path to the PNG file
        """
        try:
            image = Image.open(filepath)
            # Determine widget size and resize accordingly
            widget_width = widget.winfo_width() or 200
            widget_height = widget.winfo_height() or 200
            image.thumbnail((widget_width - 10, widget_height - 10), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            widget.config(image=photo)
            widget.image = photo  # Keep reference to prevent garbage collection
        except Exception as e:
            print(f"Error displaying image: {e}")
