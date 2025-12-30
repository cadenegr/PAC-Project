"""
Submenu View for ABC_Catalog
"""

import tkinter as tk
from src.views.base_view import BaseView
from config.settings import COLORS, FONTS, BUTTON_STYLES, CATALOG_SUBMENU


class CatalogSubmenuView(BaseView):
    """Submenu view for ABC_Catalog section"""
    
    def render(self):
        """Render the catalog submenu"""
        self.clear_container()
        
        # Title
        title = tk.Label(
            self.container,
            text="ABC_Catalog",
            font=FONTS["subtitle"],
            bg=COLORS["background"],
            fg=COLORS["text_dark"]
        )
        title.pack(pady=30)
        
        # Subtitle
        subtitle = tk.Label(
            self.container,
            text="Select a category:",
            font=FONTS["text"],
            bg=COLORS["background"],
            fg=COLORS["text_light"]
        )
        subtitle.pack(pady=10)
        
        # Create submenu buttons
        for item in CATALOG_SUBMENU:
            # Check if item has its own submenu
            if item.get("has_submenu"):
                if item["id"] == "teams_work":
                    btn = tk.Button(
                        self.container,
                        text=item["title"],
                        command=self.app_controller.show_teams_work_submenu,
                        **BUTTON_STYLES["main_menu"]
                    )
                else:
                    btn = tk.Button(
                        self.container,
                        text=item["title"],
                        command=lambda item_id=item["id"]: self.app_controller.navigate_to_catalog_item(item_id),
                        **BUTTON_STYLES["main_menu"]
                    )
            else:
                btn = tk.Button(
                    self.container,
                    text=item["title"],
                    command=lambda item_id=item["id"]: self.app_controller.navigate_to_catalog_item(item_id),
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
