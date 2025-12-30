"""
View Item View
Generic view for View report items (under Project)
"""

import tkinter as tk
from src.views.base_view import BaseView
from config.settings import *


class ViewItemView(BaseView):
    """View for individual View report items"""
    
    def __init__(self, container, app_controller, item_id):
        super().__init__(container, app_controller)
        self.item_id = item_id
        
        # Find item details
        self.item_data = None
        for item in VIEW_SUBMENU:
            if item["id"] == item_id:
                self.item_data = item
                break
    
    def render(self):
        """Render the report view"""
        self.clear_container()
        
        # Header
        from src.components.ui_components import UIComponents
        title = self.item_data["title"] if self.item_data else "Products Report"
        UIComponents.create_header(self.container, title)
        
        # Content frame
        content_frame = tk.Frame(self.container, bg=FRAME_BG_COLOR, relief="ridge", borderwidth=2)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            content_frame,
            text=title,
            font=FONTS["title"],
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR
        )
        title_label.pack(pady=30)
        
        # Description
        if self.item_data and "description" in self.item_data:
            desc_label = tk.Label(
                content_frame,
                text=self.item_data["description"],
                font=FONTS["text"],
                bg=FRAME_BG_COLOR,
                fg=SUBTITLE_COLOR,
                justify="center"
            )
            desc_label.pack(pady=20)
        
        # Placeholder message
        placeholder_label = tk.Label(
            content_frame,
            text="Report visualization coming soon...\n\n"
                 "This section will display:\n"
                 "• Detailed quantity reports\n"
                 "• Charts and graphs\n"
                 "• Export to PDF/Excel\n"
                 "• Filter by date/product",
            font=FONTS["text"],
            bg=FRAME_BG_COLOR,
            fg=INFO_COLOR,
            justify="center"
        )
        placeholder_label.pack(pady=40)
        
        # Footer with back button
        footer_frame = tk.Frame(self.container, bg=WINDOW_BG_COLOR)
        footer_frame.pack(fill="x", padx=20, pady=20)
        
        back_button = tk.Button(
            footer_frame,
            text="← Back to View",
            command=self.app_controller.show_view_submenu,
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
