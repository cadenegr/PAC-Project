"""
Payments Item Detail View
"""

import tkinter as tk
from src.views.base_view import BaseView
from config.settings import COLORS, FONTS, BUTTON_STYLES, PAYMENTS_SUBMENU


class PaymentsItemView(BaseView):
    """Detail view for payments submenu items"""
    
    def __init__(self, container, app_controller, item_id):
        """
        Initialize the payments item view
        
        Args:
            container: The parent container widget
            app_controller: Reference to the main application controller
            item_id: ID of the payments item to display
        """
        super().__init__(container, app_controller)
        self.item_id = item_id
        self.item_data = self._get_item_data()
    
    def _get_item_data(self):
        """Get item data from configuration"""
        for item in PAYMENTS_SUBMENU:
            if item["id"] == self.item_id:
                return item
        return None
    
    def render(self):
        """Render the payments item detail view"""
        self.clear_container()
        
        if not self.item_data:
            self._render_error()
            return
        
        # Title
        screen_title = tk.Label(
            self.container,
            text=self.item_data["title"],
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
            text=self.item_data["description"],
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
            text="← Back to Payments",
            command=self.app_controller.show_payments_submenu,
            **BUTTON_STYLES["back"]
        )
        btn_back.pack(pady=20)
    
    def _render_error(self):
        """Render error message if item not found"""
        error_label = tk.Label(
            self.container,
            text="Error: Item not found",
            font=FONTS["subtitle"],
            bg=COLORS["background"],
            fg=COLORS["danger"]
        )
        error_label.pack(pady=50)
        
        btn_back = tk.Button(
            self.container,
            text="← Back to Payments",
            command=self.app_controller.show_payments_submenu,
            **BUTTON_STYLES["back"]
        )
        btn_back.pack(pady=20)
