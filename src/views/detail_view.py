"""
Detail View for individual sections
"""

import tkinter as tk
from src.views.base_view import BaseView
from config.settings import COLORS, FONTS, BUTTON_STYLES, MENU_ITEMS


class DetailView(BaseView):
    """Generic detail view for menu sections"""
    
    def __init__(self, container, app_controller, section_id):
        """
        Initialize the detail view
        
        Args:
            container: The parent container widget
            app_controller: Reference to the main application controller
            section_id: ID of the section to display
        """
        super().__init__(container, app_controller)
        self.section_id = section_id
        self.section_data = self._get_section_data()
    
    def _get_section_data(self):
        """Get section data from configuration"""
        for item in MENU_ITEMS:
            if item["id"] == self.section_id:
                return item
        return None
    
    def render(self):
        """Render the detail view"""
        self.clear_container()
        
        if not self.section_data:
            self._render_error()
            return
        
        # Title
        screen_title = tk.Label(
            self.container,
            text=self.section_data["title"],
            font=FONTS["subtitle"],
            bg=COLORS["background"],
            fg=COLORS["text_dark"]
        )
        screen_title.pack(pady=30)
        
        # Content area
        content_frame = tk.Frame(
            self.container,
            bg=COLORS["white"],
            relief="solid",
            borderwidth=1
        )
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        content_label = tk.Label(
            content_frame,
            text=self.section_data["description"],
            font=FONTS["text"],
            bg=COLORS["white"],
            fg=COLORS["text_light"],
            justify="left",
            wraplength=350
        )
        content_label.pack(padx=20, pady=20)
        
        # Back button
        btn_back = tk.Button(
            self.container,
            text="← Back to Menu",
            command=self.app_controller.show_main_menu,
            **BUTTON_STYLES["back"]
        )
        btn_back.pack(pady=20)
    
    def _render_error(self):
        """Render error message if section not found"""
        error_label = tk.Label(
            self.container,
            text="Error: Section not found",
            font=FONTS["subtitle"],
            bg=COLORS["background"],
            fg=COLORS["danger"]
        )
        error_label.pack(pady=50)
        
        btn_back = tk.Button(
            self.container,
            text="← Back to Menu",
            command=self.app_controller.show_main_menu,
            **BUTTON_STYLES["back"]
        )
        btn_back.pack(pady=20)
