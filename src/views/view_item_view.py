"""
View Item View
Generic view for View report items (under Project)
"""

import tkinter as tk
from tkinter import ttk
import sqlite3
from src.views.base_view import BaseView
from config.settings import *


class ViewItemView(BaseView):
    """View for individual View report items"""
    
    def __init__(self, container, app_controller, item_id):
        super().__init__(container, app_controller)
        self.item_id = item_id
        self.current_chapter_index = 0
        self.chapters = []
        self.records = []
        
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
        title_label.pack(pady=20)
        
        # Load and display data based on item_id
        if self.item_id == "qty_project":
            self._render_qty_project_view(content_frame)
        elif self.item_id == "qty_done":
            self._render_qty_done_view(content_frame)
        elif self.item_id == "qty_progress":
            self._render_qty_progress_view(content_frame)
        elif self.item_id == "qty_to_finish":
            self._render_qty_to_finish_view(content_frame)
        else:
            self._render_placeholder(content_frame, title)
        
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
    
    def _render_placeholder(self, parent, title):
        """Render placeholder for non-implemented views"""
        # Description
        if self.item_data and "description" in self.item_data:
            desc_label = tk.Label(
                parent,
                text=self.item_data["description"],
                font=FONTS["text"],
                bg=FRAME_BG_COLOR,
                fg=SUBTITLE_COLOR,
                justify="center"
            )
            desc_label.pack(pady=20)
        
        # Placeholder message
        placeholder_label = tk.Label(
            parent,
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
    
    def _render_qty_project_view(self, parent):
        """Render Qty Project view with targets data"""
        # Load data
        self._load_targets_data("targ_qtyproject")
        
        if not self.records:
            no_data_label = tk.Label(
                parent,
                text="No hay datos disponibles",
                font=FONTS["text"],
                bg=FRAME_BG_COLOR,
                fg=WARNING_COLOR
            )
            no_data_label.pack(pady=40)
            return
        
        # Get unique chapters
        self._get_unique_chapters()
        
        # Navigation info
        nav_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        nav_frame.pack(pady=10)
        
        # Get chapter description
        chapter_desc = self._get_chapter_description(self.chapters[self.current_chapter_index])
        
        self.nav_label = tk.Label(
            nav_frame,
            text=f"Chapter {self.chapters[self.current_chapter_index]}: {chapter_desc}",
            font=FONTS["subtitle"],
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR
        )
        self.nav_label.pack()
        
        # Table frame
        table_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create Treeview
        columns = ("ProNumber", "Description", "Qty Project", "Unit")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.tree.heading("ProNumber", text="Pro Number")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Qty Project", text="Qty Project")
        self.tree.heading("Unit", text="Unit")
        
        self.tree.column("ProNumber", width=120, anchor="center")
        self.tree.column("Description", width=400, anchor="w")
        self.tree.column("Qty Project", width=120, anchor="e")
        self.tree.column("Unit", width=100, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate data
        self._populate_tree()
        
        # Navigation buttons
        nav_buttons_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        nav_buttons_frame.pack(pady=20)
        
        prev_button = tk.Button(
            nav_buttons_frame,
            text="▲ Anterior",
            command=self._prev_record,
            font=FONTS["button_small"],
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            state="normal" if self.current_chapter_index > 0 else "disabled"
        )
        prev_button.pack(side="left", padx=10)
        
        self.prev_button = prev_button
        
        next_button = tk.Button(
            nav_buttons_frame,
            text="▼ Siguiente",
            command=self._next_record,
            font=FONTS["button_small"],
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            state="normal" if self.current_chapter_index < len(self.chapters) - 1 else "disabled"
        )
        next_button.pack(side="left", padx=10)
        
        self.next_button = next_button
    
    def _render_qty_done_view(self, parent):
        """Render Qty Done view with targets data"""
        # Load data
        self._load_targets_data("targ_qtydone")
        
        if not self.records:
            no_data_label = tk.Label(
                parent,
                text="No hay datos disponibles",
                font=FONTS["text"],
                bg=FRAME_BG_COLOR,
                fg=WARNING_COLOR
            )
            no_data_label.pack(pady=40)
            return
        
        # Get unique chapters
        self._get_unique_chapters()
        
        # Navigation info
        nav_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        nav_frame.pack(pady=10)
        
        # Get chapter description
        chapter_desc = self._get_chapter_description(self.chapters[self.current_chapter_index])
        
        self.nav_label = tk.Label(
            nav_frame,
            text=f"Chapter {self.chapters[self.current_chapter_index]}: {chapter_desc}",
            font=FONTS["subtitle"],
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR
        )
        self.nav_label.pack()
        
        # Table frame
        table_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create Treeview
        columns = ("ProNumber", "Description", "Qty Done", "Unit")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.tree.heading("ProNumber", text="Pro Number")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Qty Done", text="Qty Done")
        self.tree.heading("Unit", text="Unit")
        
        self.tree.column("ProNumber", width=120, anchor="center")
        self.tree.column("Description", width=400, anchor="w")
        self.tree.column("Qty Done", width=120, anchor="e")
        self.tree.column("Unit", width=100, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate data
        self._populate_tree()
        
        # Navigation buttons
        nav_buttons_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        nav_buttons_frame.pack(pady=20)
        
        prev_button = tk.Button(
            nav_buttons_frame,
            text="▲ Anterior",
            command=self._prev_record,
            font=FONTS["button_small"],
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            state="normal" if self.current_chapter_index > 0 else "disabled"
        )
        prev_button.pack(side="left", padx=10)
        
        self.prev_button = prev_button
        
        next_button = tk.Button(
            nav_buttons_frame,
            text="▼ Siguiente",
            command=self._next_record,
            font=FONTS["button_small"],
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            state="normal" if self.current_chapter_index < len(self.chapters) - 1 else "disabled"
        )
        next_button.pack(side="left", padx=10)
        
        self.next_button = next_button
    
    def _render_qty_progress_view(self, parent):
        """Render Qty Progress view with targets data"""
        # Load data
        self._load_targets_data("targ_qtyprogress")
        
        if not self.records:
            no_data_label = tk.Label(
                parent,
                text="No hay datos disponibles",
                font=FONTS["text"],
                bg=FRAME_BG_COLOR,
                fg=WARNING_COLOR
            )
            no_data_label.pack(pady=40)
            return
        
        # Get unique chapters
        self._get_unique_chapters()
        
        # Navigation info
        nav_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        nav_frame.pack(pady=10)
        
        # Get chapter description
        chapter_desc = self._get_chapter_description(self.chapters[self.current_chapter_index])
        
        self.nav_label = tk.Label(
            nav_frame,
            text=f"Chapter {self.chapters[self.current_chapter_index]}: {chapter_desc}",
            font=FONTS["subtitle"],
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR
        )
        self.nav_label.pack()
        
        # Table frame
        table_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create Treeview
        columns = ("ProNumber", "Description", "Qty Progress", "Unit")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.tree.heading("ProNumber", text="Pro Number")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Qty Progress", text="Qty Progress")
        self.tree.heading("Unit", text="Unit")
        
        self.tree.column("ProNumber", width=120, anchor="center")
        self.tree.column("Description", width=400, anchor="w")
        self.tree.column("Qty Progress", width=120, anchor="e")
        self.tree.column("Unit", width=100, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate data
        self._populate_tree()
        
        # Navigation buttons
        nav_buttons_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        nav_buttons_frame.pack(pady=20)
        
        prev_button = tk.Button(
            nav_buttons_frame,
            text="▲ Anterior",
            command=self._prev_record,
            font=FONTS["button_small"],
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            state="normal" if self.current_chapter_index > 0 else "disabled"
        )
        prev_button.pack(side="left", padx=10)
        
        self.prev_button = prev_button
        
        next_button = tk.Button(
            nav_buttons_frame,
            text="▼ Siguiente",
            command=self._next_record,
            font=FONTS["button_small"],
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            state="normal" if self.current_chapter_index < len(self.chapters) - 1 else "disabled"
        )
        next_button.pack(side="left", padx=10)
        
        self.next_button = next_button
    
    def _render_qty_to_finish_view(self, parent):
        """Render Qty to Finish view with targets data"""
        # Load data
        self._load_targets_data("targ_qtyfinish")
        
        if not self.records:
            no_data_label = tk.Label(
                parent,
                text="No hay datos disponibles",
                font=FONTS["text"],
                bg=FRAME_BG_COLOR,
                fg=WARNING_COLOR
            )
            no_data_label.pack(pady=40)
            return
        
        # Get unique chapters
        self._get_unique_chapters()
        
        # Navigation info
        nav_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        nav_frame.pack(pady=10)
        
        # Get chapter description
        chapter_desc = self._get_chapter_description(self.chapters[self.current_chapter_index])
        
        self.nav_label = tk.Label(
            nav_frame,
            text=f"Chapter {self.chapters[self.current_chapter_index]}: {chapter_desc}",
            font=FONTS["subtitle"],
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR
        )
        self.nav_label.pack()
        
        # Table frame
        table_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create Treeview
        columns = ("ProNumber", "Description", "Qty to Finish", "Unit")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.tree.heading("ProNumber", text="Pro Number")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Qty to Finish", text="Qty to Finish")
        self.tree.heading("Unit", text="Unit")
        
        self.tree.column("ProNumber", width=120, anchor="center")
        self.tree.column("Description", width=400, anchor="w")
        self.tree.column("Qty to Finish", width=120, anchor="e")
        self.tree.column("Unit", width=100, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate data
        self._populate_tree()
        
        # Navigation buttons
        nav_buttons_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        nav_buttons_frame.pack(pady=20)
        
        prev_button = tk.Button(
            nav_buttons_frame,
            text="▲ Anterior",
            command=self._prev_record,
            font=FONTS["button_small"],
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            state="normal" if self.current_chapter_index > 0 else "disabled"
        )
        prev_button.pack(side="left", padx=10)
        
        self.prev_button = prev_button
        
        next_button = tk.Button(
            nav_buttons_frame,
            text="▼ Siguiente",
            command=self._next_record,
            font=FONTS["button_small"],
            bg=PRIMARY_COLOR,
            fg="white",
            activebackground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            state="normal" if self.current_chapter_index < len(self.chapters) - 1 else "disabled"
        )
        next_button.pack(side="left", padx=10)
        
        self.next_button = next_button
    
    def _load_targets_data(self, qty_field):
        """Load targets data from database"""
        try:
            conn = sqlite3.connect('data/pac.db')
            cursor = conn.cursor()
            
            query = f"""
                SELECT targ_prochapter, targ_pronumber, targ_prodescription, 
                       {qty_field}, targ_prounit
                FROM targets
                WHERE {qty_field} IS NOT NULL AND {qty_field} > 0
                ORDER BY targ_prochapter, targ_pronumber
            """
            
            cursor.execute(query)
            self.records = cursor.fetchall()
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            self.records = []
    
    def _get_unique_chapters(self):
        """Get unique chapters from records"""
        chapters_set = set()
        for record in self.records:
            chapters_set.add(record[0])  # targ_prochapter is first element
        self.chapters = sorted(list(chapters_set))
    
    def _get_chapter_description(self, chapter_number):
        """Get chapter description from database"""
        try:
            conn = sqlite3.connect('data/pac.db')
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT chap_description FROM chapters WHERE chap_number = ?",
                (chapter_number,)
            )
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return result[0]
            else:
                return "Sin descripción"
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return "Error al cargar descripción"
    
    def _get_current_chapter_records(self):
        """Get records for current chapter"""
        if not self.chapters:
            return []
        current_chapter = self.chapters[self.current_chapter_index]
        return [record for record in self.records if record[0] == current_chapter]
    
    def _populate_tree(self):
        """Populate tree with records from current chapter"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get records for current chapter
        chapter_records = self._get_current_chapter_records()
        
        # Insert records with formatted quantity
        for record in chapter_records:
            # Format the quantity (4th element, index 3) with 2 decimals
            formatted_record = (
                record[1],  # ProNumber
                record[2],  # Description
                f"{record[3]:.2f}" if record[3] is not None else "0.00",  # Qty with 2 decimals
                record[4]   # Unit
            )
            self.tree.insert("", "end", values=formatted_record)
    
    def _next_record(self):
        """Navigate to next chapter"""
        if self.current_chapter_index < len(self.chapters) - 1:
            self.current_chapter_index += 1
            self._update_navigation()
    
    def _prev_record(self):
        """Navigate to previous chapter"""
        if self.current_chapter_index > 0:
            self.current_chapter_index -= 1
            self._update_navigation()
    
    def _update_navigation(self):
        """Update navigation label and buttons"""
        current_chapter = self.chapters[self.current_chapter_index]
        chapter_desc = self._get_chapter_description(current_chapter)
        self.nav_label.config(
            text=f"Chapter {current_chapter}: {chapter_desc}"
        )
        
        # Update button states
        self.prev_button.config(state="normal" if self.current_chapter_index > 0 else "disabled")
        self.next_button.config(state="normal" if self.current_chapter_index < len(self.chapters) - 1 else "disabled")
        
        # Re-populate tree with current chapter records
        self._populate_tree()
