"""
Submenu View for Payments
"""

import tkinter as tk
from src.views.base_view import BaseView
from config.settings import COLORS, FONTS, BUTTON_STYLES, PAYMENTS_SUBMENU


class PaymentsSubmenuView(BaseView):
    """Submenu view for Payments section"""
    
    def render(self):
        """Render the payments submenu"""
        self.clear_container()
        
        # Title
        title = tk.Label(
            self.container,
            text="Payments",
            font=FONTS["subtitle"],
            bg=COLORS["background"],
            fg=COLORS["text_dark"]
        )
        title.pack(pady=30)
        
        # Subtitle
        subtitle = tk.Label(
            self.container,
            text="Select an option:",
            font=FONTS["text"],
            bg=COLORS["background"],
            fg=COLORS["text_light"]
        )
        subtitle.pack(pady=10)
        
        # Create submenu buttons
        for item in PAYMENTS_SUBMENU:
            btn = tk.Button(
                self.container,
                text=item["title"],
                command=lambda item_id=item["id"]: self.app_controller.navigate_to_payments_item(item_id),
                **BUTTON_STYLES["main_menu"]
            )
            btn.pack(pady=8)
        
        # Back button
        btn_back = tk.Button(
            self.container,
            text="← Back to Main Menu",
            command=self.app_controller.show_main_menu,
            **BUTTON_STYLES["back"]
        )
        btn_back.pack(pady=30)
