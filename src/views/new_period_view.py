"""
New Period View - Display periods list with New button
"""

import tkinter as tk
from tkinter import ttk
from src.views.base_view import BaseView
from src.database.period_db import PeriodDB
from config.settings import *


class NewPeriodView(BaseView):
    """View for displaying periods list"""
    
    def __init__(self, container, app_controller):
        """
        Initialize the new period view
        
        Args:
            container: The parent container widget
            app_controller: Reference to the main application controller
        """
        super().__init__(container, app_controller)
        self.period_db = PeriodDB()
    
    def render(self):
        """Render the periods list view"""
        self.clear_container()
        
        # Header
        from src.components.ui_components import UIComponents
        UIComponents.create_header(self.container, "Periods")
        
        # Main content frame
        content_frame = tk.Frame(self.container, bg=FRAME_BG_COLOR, relief="ridge", borderwidth=2)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            content_frame,
            text="Period List",
            font=FONTS["title"],
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR
        )
        title_label.pack(pady=20)
        
        # List frame
        list_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Configure grid
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollbars
        vsb = ttk.Scrollbar(list_frame, orient="vertical")
        hsb = ttk.Scrollbar(list_frame, orient="horizontal")
        
        # Treeview for periods list
        columns = ("Period Number", "Period Date")
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading("Period Number", text="Period Number")
        self.tree.heading("Period Date", text="Period Date")
        
        self.tree.column("Period Number", width=150, anchor="center")
        self.tree.column("Period Date", width=200, anchor="center")
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Populate the list
        self._populate_list()
        
        # Button frame
        button_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        button_frame.pack(pady=20)
        
        # New button
        btn_new = tk.Button(
            button_frame,
            text="📝 NEW",
            command=self._show_new_period_form,
            font=FONTS["button"],
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=40,
            pady=15,
            width=15
        )
        btn_new.pack()
        
        # Footer with back button
        footer_frame = tk.Frame(self.container, bg=WINDOW_BG_COLOR)
        footer_frame.pack(fill="x", padx=20, pady=20)
        
        btn_back = tk.Button(
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
        btn_back.pack(side="left")
    
    def _populate_list(self):
        """Populate the treeview with periods from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all periods from database
        periods = self.period_db.get_all()
        
        # Insert periods into treeview
        for period in periods:
            values = (
                period.per_number,
                period.per_date
            )
            self.tree.insert("", "end", values=values)
    
    def _show_new_period_form(self):
        """Show form to create new period"""
        from datetime import date
        from tkinter import messagebox
        from src.models.period import Period
        
        # Get all periods to determine next number
        periods = self.period_db.get_all()
        
        # Calculate next period number
        if periods:
            # Get the maximum period number
            max_number = max(period.per_number for period in periods)
            next_number = max_number + 1
        else:
            next_number = 1
        
        # Get today's date
        today = date.today().strftime("%Y-%m-%d")
        
        # Create new period
        new_period = Period(
            per_number=next_number,
            per_date=today
        )
        
        # Save to database
        if self.period_db.create(new_period):
            messagebox.showinfo("Success", f"Period {next_number} created successfully with date {today}")
            # Refresh the list
            self._populate_list()
        else:
            messagebox.showerror("Error", "Failed to create period")
