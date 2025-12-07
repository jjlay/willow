"""Entry point for Willow application."""

import tkinter as tk
from willow import WillowApplication


def main():
    """Launch Willow application."""
    root = tk.Tk()
    app = WillowApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
