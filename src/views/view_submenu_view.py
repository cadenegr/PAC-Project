"""
View Submenu View
Shows submenu options for Project → View section
"""

import tkinter as tk
from src.views.base_view import BaseView
from config.settings import *


class ViewSubmenuView(BaseView):
    """View for View submenu (under Project)"""
    
    def __init__(self, container, app_controller):
        super().__init__(container, app_controller)
        self.submenu_items = VIEW_SUBMENU
    
    def render(self):
        """Render the View submenu"""
        self.clear_container()
        
        # Header
        from src.components.ui_components import UIComponents
        UIComponents.create_header(self.container, "View - Reports")
        
        # Content frame
        content_frame = tk.Frame(self.container, bg=WINDOW_BG_COLOR)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            content_frame,
            text="Select Report Type",
            font=FONTS["subtitle"],
            bg=WINDOW_BG_COLOR,
            fg=TEXT_COLOR
        )
        title_label.pack(pady=(0, 20))
        
        # Submenu buttons
        for item in self.submenu_items:
            btn = tk.Button(
                content_frame,
                text=item["title"],
                command=lambda i=item["id"]: self.app_controller.navigate_to_view_item(i),
                **BUTTON_STYLES["main_menu"]
            )
            btn.pack(pady=8)
        
        # Footer with back button
        footer_frame = tk.Frame(self.container, bg=WINDOW_BG_COLOR)
        footer_frame.pack(fill="x", padx=20, pady=20)
        
        back_button = tk.Button(
            footer_frame,
            text="← Back to Project",
            command=self.app_controller.show_project_submenu,
            font=FONTS["button_small"],
            bg=SECONDARY_COLOR,
            fg="white",
            activebackground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        )
        back_button.pack(side="left")
