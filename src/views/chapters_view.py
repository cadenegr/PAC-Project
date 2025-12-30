"""
Chapters Management View (Using Refactored Pattern)
Manages project chapters with CRUD operations
"""

import tkinter as tk
from src.views.base_crud_view import BaseCRUDView
from src.database.chapter_db import ChapterDatabase
from src.models.chapter import Chapter
from src.components.ui_components import UIComponents
from config.settings import *


class ChaptersView(BaseCRUDView):
    """Chapters management view - inherits all CRUD logic from base"""
    
    def __init__(self, container, app_controller):
        super().__init__(container, app_controller)
        self.db = ChapterDatabase()
    
    def get_title(self):
        return "Chapters Management"
    
    def get_field_definitions(self):
        return [
            {'name': 'chap_number', 'label': 'Chapter Number *:', 'type': 'primary', 'width': 5, 'maxlength': 3},
            {'name': 'chap_description', 'label': 'Description *:', 'type': 'secondary', 'width': 30, 'maxlength': 30}
        ]
    
    def get_database(self):
        return self.db
    
    def get_model_class(self):
        return Chapter
    
    def get_primary_key_name(self):
        return 'chap_number'
    
    def get_record_by_primary_key(self, key):
        try:
            key_int = int(key)
            return self.db.get_chapter_by_number(key_int)
        except (ValueError, TypeError):
            return None
    
    def search_by_secondary_key(self, value):
        return self.db.search_by_description(value)
    
    def get_all_records(self):
        return self.db.get_all_chapters()
    
    def create_record(self, model):
        return self.db.create_chapter(model)
    
    def update_record(self, model):
        return self.db.update_chapter(model)
    
    def delete_record(self, primary_key):
        try:
            key_int = int(primary_key)
            return self.db.delete_chapter(key_int)
        except (ValueError, TypeError):
            return False
    
    def get_list_columns(self):
        return [
            ('chap_number', 'Chapter #', 100),
            ('chap_description', 'Description', 400)
        ]
    
    def render(self):
        """Override render to use Project submenu back button"""
        self.clear_container()
        
        # Header
        UIComponents.create_header(self.container, self.get_title())
        
        # Main content area
        content_frame = tk.Frame(self.container, bg=WINDOW_BG_COLOR)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Form panel
        form_panel = tk.Frame(content_frame, bg=FRAME_BG_COLOR, relief="ridge", borderwidth=2)
        form_panel.pack(fill="both", expand=True)
        
        self._create_form(form_panel)
        
        # Footer with back button to Project submenu
        footer_frame = tk.Frame(self.container, bg=WINDOW_BG_COLOR)
        footer_frame.pack(fill="x", padx=10, pady=10)
        
        btn_back = tk.Button(
            footer_frame,
            text="← Regresar a Project",
            command=self.app_controller.show_project_submenu,
            font=("Segoe UI", 10),
            bg=SECONDARY_COLOR,
            fg="white",
            activebackground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        )
        btn_back.pack(side="left")
