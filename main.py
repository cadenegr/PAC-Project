"""
PAC - Menu Application
Entry point for the application
"""

import tkinter as tk
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_BG_COLOR
from src.controllers.app_controller import AppController


class MenuApp:
    """Main application class"""
    
    def __init__(self, root):
        """
        Initialize the application
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self._configure_window()
        
        # Create main container
        self.container = tk.Frame(root, bg=WINDOW_BG_COLOR)
        self.container.pack(fill="both", expand=True)
        
        # Initialize controller
        self.controller = AppController(self.container, self.root)
        
        # Show main menu
        self.controller.show_main_menu()
    
    def _configure_window(self):
        """Configure the main window settings"""
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=WINDOW_BG_COLOR)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
