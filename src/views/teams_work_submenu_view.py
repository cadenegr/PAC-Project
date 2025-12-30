"""
Submenu View for Teams_Work
"""

import tkinter as tk
from src.views.base_view import BaseView
from config.settings import COLORS, FONTS, BUTTON_STYLES, TEAMS_WORK_SUBMENU


class TeamsWorkSubmenuView(BaseView):
    """Submenu view for Teams_Work section"""
    
    def render(self):
        """Render the teams work submenu"""
        self.clear_container()
        
        # Title
        title = tk.Label(
            self.container,
            text="Teams_Work",
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
        for item in TEAMS_WORK_SUBMENU:
            btn = tk.Button(
                self.container,
                text=item["title"],
                command=lambda item_id=item["id"]: self.app_controller.navigate_to_teams_work_item(item_id),
                **BUTTON_STYLES["main_menu"]
            )
            btn.pack(pady=8)
        
        # Back button
        btn_back = tk.Button(
            self.container,
            text="← Back to ABC_Catalog",
            command=self.app_controller.show_catalog_submenu,
            **BUTTON_STYLES["back"]
        )
        btn_back.pack(pady=30)
