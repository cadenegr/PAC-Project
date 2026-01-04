"""
Work Order Form View
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.views.base_view import BaseView
from src.database.work_order_db import WorkOrderDB
from src.models.work_order import WorkOrder
from src.models.database import Database, Team
from src.database.target_db import TargetDatabase
from config.settings import *


class WorkOrderFormView(BaseView):
    """View for creating/updating work orders"""
    
    def __init__(self, container, app_controller, mode="new"):
        """
        Initialize the work order form view
        
        Args:
            container: The parent container widget
            app_controller: Reference to the main application controller
            mode: "new" or "update"
        """
        super().__init__(container, app_controller)
        self.work_order_db = WorkOrderDB()
        self.mode = mode
        
        # Initialize databases
        self.db = Database()
        self.team_model = Team(self.db)
        self.target_db = TargetDatabase()
        
        # Form variables
        self.wo_number_var = tk.StringVar()
        self.wo_date_var = tk.StringVar()
        self.wo_time_var = tk.StringVar()
        self.wo_teamnumber_var = tk.StringVar()
        self.wo_chapter_var = tk.StringVar()
        self.wo_target_var = tk.StringVar()
        self.wo_qty_var = tk.StringVar()
        self.wo_price_var = tk.StringVar()
        self.wo_done_var = tk.StringVar()
        self.wo_payticket_var = tk.StringVar()
        self.wo_status_var = tk.StringVar()
        
        # Target info display variables
        self.targ_qtyproject_var = tk.StringVar()
        self.targ_qtydone_var = tk.StringVar()
        self.targ_qtyprogress_var = tk.StringVar()
        self.targ_qtyfinish_var = tk.StringVar()
        
        # Labels for lookups
        self.team_name_label = None
        self.chapter_description_label = None
        self.target_description_label = None
    
    def render(self):
        """Render the work order form view"""
        self.clear_container()
        
        # Header
        from src.components.ui_components import UIComponents
        UIComponents.create_header(self.container, "New Work Order")
        
        # Main content frame
        content_frame = tk.Frame(self.container, bg=FRAME_BG_COLOR, relief="ridge", borderwidth=2)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            content_frame,
            text="Work Order Form",
            font=FONTS["title"],
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR
        )
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        form_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        # WO Number field (read-only)
        self._create_field(form_frame, "WO Number:", self.wo_number_var, 0, width=6, state="readonly")
        
        # WO Date field (read-only)
        self._create_field(form_frame, "Date (YYYY-MM-DD):", self.wo_date_var, 1, width=15, state="readonly")
        
        # WO Time field (read-only)
        self._create_field(form_frame, "Time (HH:MM):", self.wo_time_var, 2, width=10, state="readonly")
        
        # Team Number field with lookup
        self.team_name_label = self._create_field_with_lookup(
            form_frame, 
            "Team Number:", 
            self.wo_teamnumber_var, 
            3, 
            width=6,
            on_validate=self._validate_team_number
        )
        
        # Chapter field with lookup
        self.chapter_description_label = self._create_field_with_lookup(
            form_frame, 
            "Chapter:", 
            self.wo_chapter_var, 
            4, 
            width=6,
            on_validate=self._validate_chapter
        )
        
        # Target field with lookup
        self.target_description_label = self._create_field_with_lookup(
            form_frame, 
            "Target:", 
            self.wo_target_var, 
            5, 
            width=6,
            on_validate=self._validate_target
        )
        
        # Quantity field
        self._create_field(form_frame, "Quantity:", self.wo_qty_var, 6, width=15)
        
        # Price field
        self._create_field(form_frame, "Price:", self.wo_price_var, 7, width=15)
        
        # Target quantities (read-only display)
        self._create_field(form_frame, "Qty Project:", self.targ_qtyproject_var, 8, width=15, state="readonly")
        self._create_field(form_frame, "Qty Done:", self.targ_qtydone_var, 9, width=15, state="readonly")
        self._create_field(form_frame, "Qty Progress:", self.targ_qtyprogress_var, 10, width=15, state="readonly")
        self._create_field(form_frame, "Qty Finish:", self.targ_qtyfinish_var, 11, width=15, state="readonly")
        
        # Done field (read-only)
        self._create_field(form_frame, "Done:", self.wo_done_var, 12, width=15, state="readonly")
        
        # Pay Ticket field (read-only)
        self._create_field(form_frame, "Pay Ticket:", self.wo_payticket_var, 13, width=25, state="readonly")
        
        # Status field (read-only)
        self._create_field(form_frame, "Status:", self.wo_status_var, 14, width=4, state="readonly")
        
        # Initialize form with next number
        self._initialize_form()
        
        # Buttons frame
        buttons_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        buttons_frame.pack(pady=20)
        
        # Accept button
        btn_accept = tk.Button(
            buttons_frame,
            text="✓ Accept",
            command=self._save_work_order,
            font=FONTS["button"],
            bg=SUCCESS_COLOR,
            fg="white",
            activebackground="#229954",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=12,
            width=12
        )
        btn_accept.pack(side="left", padx=10)
        
        # Cancel button
        btn_cancel = tk.Button(
            buttons_frame,
            text="✖ Cancel",
            command=self._cancel_form,
            font=FONTS["button"],
            bg=DANGER_COLOR,
            fg="white",
            activebackground="#C0392B",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=12,
            width=12
        )
        btn_cancel.pack(side="left", padx=10)
        
        # Footer with back button
        footer_frame = tk.Frame(self.container, bg=WINDOW_BG_COLOR)
        footer_frame.pack(fill="x", padx=20, pady=20)
        
        btn_back = tk.Button(
            footer_frame,
            text="← Back",
            command=self._go_back,
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
    
    def _create_field(self, parent, label_text, variable, row, width=30, state="normal"):
        """Create a form field with label and entry"""
        field_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        field_frame.pack(fill="x", pady=8)
        
        label = tk.Label(
            field_frame,
            text=label_text,
            font=FONTS["text"],
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR,
            width=20,
            anchor="w"
        )
        label.pack(side="left", padx=5)
        
        entry = tk.Entry(
            field_frame,
            textvariable=variable,
            font=FONTS["text"],
            width=width,
            state=state
        )
        entry.pack(side="left", padx=5)
        
        if row == 3:
            entry.focus()
    
    def _create_field_with_lookup(self, parent, label_text, variable, row, width=30, on_validate=None):
        """Create a form field with label, entry, and lookup label"""
        field_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        field_frame.pack(fill="x", pady=8)
        
        label = tk.Label(
            field_frame,
            text=label_text,
            font=FONTS["text"],
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR,
            width=20,
            anchor="w"
        )
        label.pack(side="left", padx=5)
        
        entry = tk.Entry(
            field_frame,
            textvariable=variable,
            font=FONTS["text"],
            width=width,
            relief="solid",
            borderwidth=1
        )
        entry.pack(side="left", padx=5)
        
        # Add search button for Team Number, Target, and Chapter fields
        if label_text == "Team Number:":
            search_btn = tk.Button(
                field_frame,
                text="🔍 Search",
                command=self._open_team_search,
                font=FONTS["button_small"],
                bg=INFO_COLOR,
                fg="white",
                relief="flat",
                cursor="hand2",
                padx=10,
                pady=5
            )
            search_btn.pack(side="left", padx=5)
        elif label_text == "Target:":
            search_btn = tk.Button(
                field_frame,
                text="🔍 Search",
                command=self._open_target_search,
                font=FONTS["button_small"],
                bg=INFO_COLOR,
                fg="white",
                relief="flat",
                cursor="hand2",
                padx=10,
                pady=5
            )
            search_btn.pack(side="left", padx=5)
        elif label_text == "Chapter:":
            search_btn = tk.Button(
                field_frame,
                text="🔍 Search",
                command=self._open_chapter_search,
                font=FONTS["button_small"],
                bg=INFO_COLOR,
                fg="white",
                relief="flat",
                cursor="hand2",
                padx=10,
                pady=5
            )
            search_btn.pack(side="left", padx=5)
        
        # Lookup label
        lookup_label = tk.Label(
            field_frame,
            text="",
            font=FONTS["text"],
            bg=FRAME_BG_COLOR,
            fg=SUCCESS_COLOR,
            anchor="w"
        )
        lookup_label.pack(side="left", padx=10)
        
        # Bind validation
        if on_validate:
            entry.bind("<FocusOut>", lambda e: on_validate())
            entry.bind("<Return>", lambda e: on_validate())
        
        if row == 3:
            entry.focus()
        
        return lookup_label
    
    def _validate_team_number(self):
        """Validate team number and display team name"""
        team_number = self.wo_teamnumber_var.get().strip()
        
        if not team_number:
            self.team_name_label.config(text="")
            return
        
        # Search for team in database
        db = Database()
        team_manager = Team(db)
        team = team_manager.get_by_number(team_number)
        
        if team:
            self.team_name_label.config(text=f"✓ {team['team_name']}", fg=SUCCESS_COLOR)
        else:
            self.team_name_label.config(text="✗ Not found", fg=DANGER_COLOR)
            messagebox.showwarning("Team Not Found", f"Team number {team_number} does not exist.")
            return False
        
        return True
    
    def _validate_chapter(self):
        """Validate chapter number and display chapter description"""
        from src.database.chapter_db import ChapterDB
        
        chapter_number = self.wo_chapter_var.get().strip()
        
        if not chapter_number:
            self.chapter_description_label.config(text="")
            return
        
        # Normalize to 4 characters if numeric
        if chapter_number.isdigit():
            chapter_number = chapter_number.zfill(4)
            self.wo_chapter_var.set(chapter_number)
        
        # Search for chapter in database
        chapter_db = ChapterDB()
        chapter = chapter_db.get_by_number(chapter_number)
        
        if chapter:
            description = chapter.chap_description or "No description"
            self.chapter_description_label.config(text=f"✓ {description}", fg=SUCCESS_COLOR)
        else:
            self.chapter_description_label.config(text="✗ Not found", fg=DANGER_COLOR)
            messagebox.showwarning("Chapter Not Found", f"Chapter number {chapter_number} does not exist.")
            return False
        
        return True
    
    def _open_team_search(self):
        """Open team search popup window"""
        # Create popup window
        popup = tk.Toplevel(self.container)
        popup.title("Select Team")
        popup.geometry("700x500")
        popup.configure(bg=WINDOW_BG_COLOR)
        popup.transient(self.container)
        popup.grab_set()
        
        # Header
        header_frame = tk.Frame(popup, bg=ACCENT_COLOR)
        header_frame.pack(fill="x")
        
        header_label = tk.Label(
            header_frame,
            text="Select Team",
            font=FONTS["header"],
            bg=ACCENT_COLOR,
            fg="white",
            pady=15
        )
        header_label.pack()
        
        # Content frame
        content_frame = tk.Frame(popup, bg=FRAME_BG_COLOR, relief="ridge", borderwidth=2)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Get all teams
        db = Database()
        team_manager = Team(db)
        all_teams = team_manager.get_all()
        
        if not all_teams:
            messagebox.showinfo("No Data", "No teams found in database")
            popup.destroy()
            return
        
        # Create treeview
        tree_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview
        tree = ttk.Treeview(
            tree_frame,
            columns=("Number", "Name"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15,
            selectmode="browse"
        )
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=tree.yview)
        
        # Configure selection colors
        style = ttk.Style()
        style.map('Treeview', background=[('selected', ACCENT_COLOR)], foreground=[('selected', 'white')])
        
        # Configure columns
        tree.heading("Number", text="Team Number")
        tree.heading("Name", text="Team Name")
        tree.column("Number", width=150, anchor="center")
        tree.column("Name", width=400, anchor="w")
        
        # Populate treeview
        for team in all_teams:
            tree.insert("", "end", values=(team['team_number'], team['team_name']))
        
        # Double-click to select
        def on_select(event):
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                team_number = item['values'][0]
                self.wo_teamnumber_var.set(str(team_number))
                self._validate_team_number()
                popup.destroy()
        
        tree.bind("<Double-Button-1>", on_select)
        
        # Button frame
        btn_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        # Close button
        btn_close = tk.Button(
            btn_frame,
            text="Close",
            command=popup.destroy,
            font=FONTS["button"],
            bg=SECONDARY_COLOR,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=12,
            width=12
        )
        btn_close.pack(side="left", padx=10)
    
    def _open_chapter_search(self):
        """Open chapter search popup window"""
        from src.database.chapter_db import ChapterDB
        
        # Create popup window
        popup = tk.Toplevel(self.container)
        popup.title("Select Chapter")
        popup.geometry("700x500")
        popup.configure(bg=WINDOW_BG_COLOR)
        popup.transient(self.container)
        popup.grab_set()
        
        # Header
        header_frame = tk.Frame(popup, bg=ACCENT_COLOR)
        header_frame.pack(fill="x")
        
        header_label = tk.Label(
            header_frame,
            text="Select Chapter",
            font=FONTS["header"],
            bg=ACCENT_COLOR,
            fg="white",
            pady=15
        )
        header_label.pack()
        
        # Content frame
        content_frame = tk.Frame(popup, bg=FRAME_BG_COLOR, relief="ridge", borderwidth=2)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Get all chapters
        chapter_db = ChapterDB()
        all_chapters = chapter_db.get_all()
        
        if not all_chapters:
            messagebox.showinfo("No Data", "No chapters found in database")
            popup.destroy()
            return
        
        # Tree frame
        tree_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        tree_frame.pack(fill="both", expand=True, pady=10)
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        columns = ("Number", "Description")
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15,
            selectmode="browse"
        )
        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        
        # Configure columns
        tree.heading("Number", text="Chapter Number")
        tree.heading("Description", text="Description")
        
        tree.column("Number", width=150, anchor="center")
        tree.column("Description", width=450, anchor="w")
        
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Populate tree
        for chapter in all_chapters:
            tree.insert("", "end", values=(
                chapter.chap_number,
                chapter.chap_description
            ))
        
        # Double-click to select
        def on_select(event):
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                chapter_number = item['values'][0]
                self.wo_chapter_var.set(chapter_number)
                self._validate_chapter()
                popup.destroy()
        
        tree.bind("<Double-Button-1>", on_select)
        
        # Buttons frame
        buttons_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        buttons_frame.pack(pady=10)
        
        # Close button
        btn_close = tk.Button(
            buttons_frame,
            text="Close",
            command=popup.destroy,
            font=FONTS["button"],
            bg=SECONDARY_COLOR,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=12,
            width=12
        )
        btn_close.pack(side="left", padx=10)
    
    def _validate_target(self):
        """Validate target number and display target description"""
        target_number = self.wo_target_var.get().strip()
        
        if not target_number:
            self.target_description_label.config(text="")
            # Clear target quantity fields
            self.targ_qtyproject_var.set("")
            self.targ_qtydone_var.set("")
            self.targ_qtyprogress_var.set("")
            self.targ_qtyfinish_var.set("")
            return
        
        # Search for target in database by pronumber
        target = self.target_db.get_target_by_number(target_number)
        
        if target:
            description = target.targ_prodescription or "No description"
            self.target_description_label.config(text=f"✓ {description}", fg=SUCCESS_COLOR)
            
            # Update target quantity fields
            self.targ_qtyproject_var.set(f"{target.targ_qtyproject:,.2f}" if target.targ_qtyproject else "0.00")
            self.targ_qtydone_var.set(f"{target.targ_qtydone:,.2f}" if target.targ_qtydone else "0.00")
            self.targ_qtyprogress_var.set(f"{target.targ_qtyprogress:,.2f}" if target.targ_qtyprogress else "0.00")
            
            # Calculate qty finish: qty project - qty done - qty progress
            qty_project = target.targ_qtyproject if target.targ_qtyproject else 0.0
            qty_done = target.targ_qtydone if target.targ_qtydone else 0.0
            qty_progress = target.targ_qtyprogress if target.targ_qtyprogress else 0.0
            qty_finish = qty_project - qty_done - qty_progress
            self.targ_qtyfinish_var.set(f"{qty_finish:,.2f}")
        else:
            self.target_description_label.config(text="✗ Not found", fg=DANGER_COLOR)
            # Clear target quantity fields
            self.targ_qtyproject_var.set("")
            self.targ_qtydone_var.set("")
            self.targ_qtyprogress_var.set("")
            self.targ_qtyfinish_var.set("")
            messagebox.showwarning("Target Not Found", f"Target number {target_number} does not exist.")
            return False
        
        return True
    
    def _open_target_search(self):
        """Open target search popup window"""
        from src.database.chapter_db import ChapterDB
        
        # Get chapter from form field
        selected_chapter = self.wo_chapter_var.get().strip()
        
        # Validate chapter is entered
        if not selected_chapter:
            messagebox.showwarning("Chapter Required", "Por favor ingrese un Chapter Number antes de buscar targets")
            return
        
        # Normalize chapter to 4 characters if numeric
        if selected_chapter.isdigit():
            selected_chapter = selected_chapter.zfill(4)
        
        # Create popup window
        popup = tk.Toplevel(self.container)
        popup.title("Select Target")
        popup.geometry("900x600")
        popup.configure(bg=WINDOW_BG_COLOR)
        popup.transient(self.container)
        popup.grab_set()
        
        # Header
        header_frame = tk.Frame(popup, bg=ACCENT_COLOR)
        header_frame.pack(fill="x")
        
        header_label = tk.Label(
            header_frame,
            text="Select Target",
            font=FONTS["header"],
            bg=ACCENT_COLOR,
            fg="white",
            pady=15
        )
        header_label.pack()
        
        # Content frame
        content_frame = tk.Frame(popup, bg=FRAME_BG_COLOR, relief="ridge", borderwidth=2)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Get all targets and filter by selected chapter
        all_targets = self.target_db.get_all_targets()
        if not all_targets:
            messagebox.showinfo("No Data", "No targets found in database")
            popup.destroy()
            return
        
        # Filter targets by the selected chapter
        filtered_targets = [t for t in all_targets if str(t.targ_prochapter).zfill(4) == selected_chapter]
        
        if not filtered_targets:
            messagebox.showinfo("No Data", f"No targets found for chapter {selected_chapter}")
            popup.destroy()
            return
        
        # Chapter info label
        chapter_db = ChapterDB()
        chapter_obj = chapter_db.get_by_number(selected_chapter)
        chapter_desc = chapter_obj.chap_description if chapter_obj else ""
        
        info_label = tk.Label(
            content_frame,
            text=f"Chapter {selected_chapter}: {chapter_desc}",
            font=FONTS["subtitle"],
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR,
            pady=10
        )
        info_label.pack()
        
        # Tree frame
        tree_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        tree_frame.pack(fill="both", expand=True, pady=10)
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        columns = ("Number", "Description", "Unit", "Qty Project")
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15,
            selectmode="browse"
        )
        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        
        # Configure columns
        tree.heading("Number", text="Number")
        tree.heading("Description", text="Description")
        tree.heading("Unit", text="Unit")
        tree.heading("Qty Project", text="Qty Project")
        
        tree.column("Number", width=100, anchor="center")
        tree.column("Description", width=400, anchor="w")
        tree.column("Unit", width=100, anchor="center")
        tree.column("Qty Project", width=150, anchor="e")
        
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Populate tree with filtered targets
        for target in filtered_targets:
            qty = target.targ_qtyproject if target.targ_qtyproject else 0
            values = (
                target.targ_pronumber or "",
                target.targ_prodescription or "",
                target.targ_prounit or "",
                f"{qty:,.2f}"
            )
            tree.insert("", "end", values=values)
        
        # Double-click to select
        def on_select(event):
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                target_number = item['values'][0]
                self.wo_target_var.set(target_number)
                self._validate_target()
                popup.destroy()
        
        tree.bind("<Double-Button-1>", on_select)
        
        # Buttons frame
        buttons_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        buttons_frame.pack(pady=10)
        
        # Close button
        btn_close = tk.Button(
            buttons_frame,
            text="Close",
            command=popup.destroy,
            font=FONTS["button"],
            bg=SECONDARY_COLOR,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=12,
            width=12
        )
        btn_close.pack(side="left", padx=10)
        
        # Initial population
        populate_tree()
    
    def _initialize_form(self):
        """Initialize form with default values"""
        work_orders = self.work_order_db.get_all()
        
        if work_orders:
            max_number = 0
            for wo in work_orders:
                try:
                    num = int(wo.wo_number)
                    if num > max_number:
                        max_number = num
                except ValueError:
                    pass
            next_number = max_number + 1
        else:
            next_number = 1
        
        self.wo_number_var.set(str(next_number).zfill(4))
        
        now = datetime.now()
        self.wo_date_var.set(now.strftime("%Y-%m-%d"))
        self.wo_time_var.set(now.strftime("%H:%M"))
        
        self.wo_qty_var.set("0.00")
        self.wo_price_var.set("0.00")
        self.wo_done_var.set("0.00")
        self.wo_status_var.set("2")
    
    def _save_work_order(self):
        """Save the work order to database"""
        wo_number = self.wo_number_var.get().strip()
        wo_date = self.wo_date_var.get().strip()
        wo_time = self.wo_time_var.get().strip()
        
        if not wo_number or not wo_date or not wo_time:
            messagebox.showwarning("Validation Error", "WO Number, Date, and Time are required")
            return
        
        try:
            datetime.strptime(wo_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Validation Error", "Date must be in format YYYY-MM-DD")
            return
        
        try:
            datetime.strptime(wo_time, "%H:%M")
        except ValueError:
            messagebox.showerror("Validation Error", "Time must be in format HH:MM")
            return
        
        try:
            wo_qty = float(self.wo_qty_var.get() or 0)
            wo_price = float(self.wo_price_var.get() or 0)
            wo_done = float(self.wo_done_var.get() or 0)
            wo_status = 2
        except ValueError:
            messagebox.showerror("Validation Error", "Quantity and Price must be numeric")
            return
        
        work_order = WorkOrder(
            wo_number=wo_number,
            wo_date=wo_date,
            wo_time=wo_time,
            wo_teamnumber=self.wo_teamnumber_var.get().strip() or None,
            wo_chapter=self.wo_chapter_var.get().strip() or None,
            wo_target=self.wo_target_var.get().strip() or None,
            wo_qty=wo_qty,
            wo_price=wo_price,
            wo_done=wo_done,
            wo_payticket=self.wo_payticket_var.get().strip() or None,
            wo_status=wo_status
        )
        
        if self.work_order_db.create(work_order):
            messagebox.showinfo("Success", f"Work Order {wo_number} created successfully")
            self._go_back()
        else:
            messagebox.showerror("Error", "Failed to create work order. Number may already exist.")
    
    def _cancel_form(self):
        """Clear the form"""
        result = messagebox.askyesno("Confirm", "Are you sure you want to cancel? All data will be lost.")
        if result:
            self._go_back()
    
    def _go_back(self):
        """Go back to work orders menu"""
        self.app_controller.navigate_to_orders_item("work_orders")
