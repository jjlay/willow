"""Backward-compatible wrapper for Willow application.

This module maintains compatibility with code that imports WillowApplication
from willow.py, while delegating to the modular willow package.

New code should use: from willow import WillowApplication
or: python main.py
"""

from willow import WillowApplication

__all__ = ["WillowApplication"]

# Entry point for backward compatibility
def main():
    """Entry point for the Willow application."""
    import tkinter as tk
    root = tk.Tk()
    app = WillowApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
