"""
Main Menu View
"""

import tkinter as tk
from src.views.base_view import BaseView
from config.settings import COLORS, FONTS, BUTTON_STYLES, MENU_ITEMS


class MainMenuView(BaseView):
    """Main menu view with navigation buttons"""
    
    def render(self):
        """Render the main menu"""
        self.clear_container()
        
        # Title
        title = tk.Label(
            self.container,
            text="PAC Menu",
            font=FONTS["title"],
            bg=COLORS["background"],
            fg=COLORS["text_dark"]
        )
        title.pack(pady=30)
        
        # Create menu buttons from configuration
        for item in MENU_ITEMS:
            btn = tk.Button(
                self.container,
                text=item["title"],
                command=lambda item_id=item["id"]: self.app_controller.navigate_to(item_id),
                **BUTTON_STYLES["main_menu"]
            )
            btn.pack(pady=10)
        
        # Exit button
        btn_exit = tk.Button(
            self.container,
            text="Exit",
            command=self.app_controller.exit_app,
            **BUTTON_STYLES["exit"]
        )
        btn_exit.pack(pady=30)
