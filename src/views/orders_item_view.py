"""
Orders Item Detail View
"""

import tkinter as tk
from src.views.base_view import BaseView
from config.settings import *


class OrdersItemView(BaseView):
    """Detail view for orders submenu items"""
    
    def __init__(self, container, app_controller, item_id):
        """
        Initialize the orders item view
        
        Args:
            container: The parent container widget
            app_controller: Reference to the main application controller
            item_id: ID of the orders item to display
        """
        super().__init__(container, app_controller)
        self.item_id = item_id
        self.item_data = self._get_item_data()
    
    def _get_item_data(self):
        """Get item data from configuration"""
        for item in ORDERS_SUBMENU:
            if item["id"] == self.item_id:
                return item
        return None
    
    def render(self):
        """Render the orders item detail view"""
        self.clear_container()
        
        if not self.item_data:
            self._render_error()
            return
        
        # For work_orders, show New/Update buttons like Teams Work
        if self.item_id == "work_orders":
            self._render_work_orders_menu()
        else:
            self._render_placeholder()
    
    def _render_work_orders_menu(self):
        """Render Work Orders menu with New/Update buttons"""
        # Header
        from src.components.ui_components import UIComponents
        UIComponents.create_header(self.container, "Work Orders")
        
        # Content frame
        content_frame = tk.Frame(self.container, bg=FRAME_BG_COLOR, relief="ridge", borderwidth=2)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            content_frame,
            text="Work Orders Management",
            font=FONTS["title"],
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR
        )
        title_label.pack(pady=30)
        
        # Description
        desc_label = tk.Label(
            content_frame,
            text="Select an option to manage work orders",
            font=FONTS["text"],
            bg=FRAME_BG_COLOR,
            fg=SUBTITLE_COLOR
        )
        desc_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        buttons_frame.pack(pady=40)
        
        # New button
        btn_new = tk.Button(
            buttons_frame,
            text="New",
            command=lambda: self.app_controller.show_work_order_form("new"),
            font=FONTS["button"],
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=40,
            pady=15,
            width=20
        )
        btn_new.pack(pady=10)
        
        # Update button
        btn_update = tk.Button(
            buttons_frame,
            text="Update",
            command=lambda: self.app_controller.show_work_order_form("update"),
            font=FONTS["button"],
            bg=INFO_COLOR,
            fg="white",
            activebackground="#138D75",
            relief="flat",
            cursor="hand2",
            padx=40,
            pady=15,
            width=20
        )
        btn_update.pack(pady=10)
        
        # View button
        btn_view = tk.Button(
            buttons_frame,
            text="View",
            command=lambda: self.app_controller.show_work_order_view(),
            font=FONTS["button"],
            bg=SUCCESS_COLOR,
            fg="white",
            activebackground="#229954",
            relief="flat",
            cursor="hand2",
            padx=40,
            pady=15,
            width=20
        )
        btn_view.pack(pady=10)
        
        # Footer with back button
        footer_frame = tk.Frame(self.container, bg=WINDOW_BG_COLOR)
        footer_frame.pack(fill="x", padx=20, pady=20)
        
        btn_back = tk.Button(
            footer_frame,
            text="← Back to Orders",
            command=self.app_controller.show_orders_submenu,
            font=FONTS["button_small"],
            bg=SECONDARY_COLOR,
            fg="white",
            activebackground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        )
        btn_back.pack(side="left")
    
    def _render_placeholder(self):
        """Render placeholder for other orders items"""
        # Title
        screen_title = tk.Label(
            self.container,
            text=self.item_data["title"],
            font=FONTS["subtitle"],
            bg=WINDOW_BG_COLOR,
            fg=TEXT_COLOR
        )
        screen_title.pack(pady=30)
        
        # Content area
        content_frame = tk.Frame(
            self.container,
            bg=FRAME_BG_COLOR,
            relief="solid",
            borderwidth=1
        )
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        content_label = tk.Label(
            content_frame,
            text=self.item_data["description"],
            font=FONTS["text"],
            bg=FRAME_BG_COLOR,
            fg=SUBTITLE_COLOR,
            justify="left",
            wraplength=350
        )
        content_label.pack(padx=20, pady=20)
        
        # Back button
        btn_back = tk.Button(
            self.container,
            text="← Back to Orders",
            command=self.app_controller.show_orders_submenu,
            font=FONTS["button_small"],
            bg=SECONDARY_COLOR,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        )
        btn_back.pack(pady=20)
    
    def _render_error(self):
        """Render error message if item not found"""
        error_label = tk.Label(
            self.container,
            text="Error: Item not found",
            font=FONTS["subtitle"],
            bg=WINDOW_BG_COLOR,
            fg=DANGER_COLOR
        )
        error_label.pack(pady=50)
        
        btn_back = tk.Button(
            self.container,
            text="← Back to Orders",
            command=self.app_controller.show_orders_submenu,
            font=FONTS["button_small"],
            bg=SECONDARY_COLOR,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        )
        btn_back.pack(pady=20)
