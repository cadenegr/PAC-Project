"""
Base view class for all application views
"""

import tkinter as tk
from abc import ABC, abstractmethod


class BaseView(ABC):
    """Abstract base class for all views"""
    
    def __init__(self, container, app_controller):
        """
        Initialize the base view
        
        Args:
            container: The parent container widget
            app_controller: Reference to the main application controller
        """
        self.container = container
        self.app_controller = app_controller
    
    @abstractmethod
    def render(self):
        """Render the view - must be implemented by subclasses"""
        pass
    
    def clear_container(self):
        """Clear all widgets from the container"""
        for widget in self.container.winfo_children():
            widget.destroy()
