"""
Create Targets View (Refactored with BaseCRUDView)
Custom validation with cross-database lookups
"""

import tkinter as tk
from tkinter import messagebox
from src.views.base_crud_view import BaseCRUDView
from src.database.target_db import TargetDatabase
from src.database.chapter_db import ChapterDatabase
from src.database.product_db import ProductDatabase
from src.models.target import Target
from config.settings import *


class CreateTargetsView(BaseCRUDView):
    """Create Targets view with cross-database validation"""
    
    def __init__(self, container, app_controller):
        self.chapter_db = ChapterDatabase()
        self.product_db = ProductDatabase()
        self.current_chapter = None
        self.current_product = None
        super().__init__(container, app_controller)
        self.db = TargetDatabase()
    
    def get_title(self):
        return "Create Targets"
    
    def get_field_definitions(self):
        return [
            {'name': 'targ_prochapter', 'label': 'Chapter Number *:', 'type': 'text', 'width': 5, 'maxlength': 3},
            {'name': 'targ_pronumber', 'label': 'Product Number *:', 'type': 'primary', 'width': 12, 'maxlength': 12},
            {'name': 'targ_prodescription', 'label': 'Description:', 'type': 'text', 'width': 30, 'maxlength': 30},
            {'name': 'targ_prounit', 'label': 'Unit:', 'type': 'text', 'width': 4, 'maxlength': 4},
            {'name': 'targ_proprice1', 'label': 'Price:', 'type': 'numeric', 'width': 15, 'maxlength': 12, 'decimals': 2},
            {'name': 'targ_qtyproject', 'label': 'Qty Project:', 'type': 'numeric', 'width': 15, 'maxlength': 12, 'decimals': 2},
            {'name': 'targ_qtydone', 'label': 'Qty Done:', 'type': 'numeric', 'width': 15, 'maxlength': 12, 'decimals': 2},
            {'name': 'targ_qtyprogress', 'label': 'Qty Progress:', 'type': 'numeric', 'width': 15, 'maxlength': 12, 'decimals': 2},
            {'name': 'targ_qtyfinish', 'label': 'Qty Finish:', 'type': 'numeric', 'width': 15, 'maxlength': 12, 'decimals': 2},
            {'name': 'targ_payment', 'label': 'Payment:', 'type': 'numeric', 'width': 15, 'maxlength': 12, 'decimals': 2}
        ]
    
    def get_database(self):
        return self.db
    
    def get_model_class(self):
        return Target
    
    def get_primary_key_name(self):
        return 'targ_pronumber'
    
    def get_record_by_primary_key(self, key):
        return self.db.get_target_by_number(key)
    
    def search_by_secondary_key(self, value):
        return self.db.search_by_description(value)
    
    def get_all_records(self):
        return self.db.get_all_targets()
    
    def create_record(self, model):
        return self.db.create_target(model)
    
    def update_record(self, model):
        return self.db.update_target(model)
    
    def delete_record(self, primary_key):
        # For targets, we need both chapter and pronumber
        # Get chapter from form
        chapter = self.form_builder.entries['targ_prochapter'].get().strip()
        return self.db.delete_target(chapter, primary_key)
    
    def get_list_columns(self):
        return [
            ('targ_prochapter', 'Chapter', 80),
            ('targ_pronumber', 'ProNumber', 120),
            ('targ_prodescription', 'Description', 300),
            ('targ_prounit', 'Unit', 80),
            ('targ_proprice1', 'Price', 120)
        ]
    
    def _create_form(self, parent):
        """Override to add custom validation buttons"""
        # Form title
        form_title = tk.Label(
            parent,
            text=f"Datos del {self.get_title().replace(' Management', '')}",
            font=("Segoe UI", 14, "bold"),
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR
        )
        form_title.pack(pady=15)
        
        # Navigation buttons
        from src.components.ui_components import UIComponents
        UIComponents.create_navigation_buttons(
            parent,
            self._navigate_previous,
            self._open_list_popup,
            self._navigate_next
        )
        
        # Custom form with validation buttons
        fields_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        fields_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Chapter with validation button
        self._create_label(fields_frame, "Chapter Number *:", 0)
        chap_frame = tk.Frame(fields_frame, bg=FRAME_BG_COLOR)
        chap_frame.grid(row=0, column=1, pady=8, sticky="ew", padx=(0, 10))
        
        self.entry_chap = tk.Entry(chap_frame, font=("Segoe UI", 10), relief="solid", borderwidth=1, width=5)
        self.entry_chap.pack(side="left", padx=(0, 5))
        vcmd = (self.entry_chap.register(lambda text: len(text) <= 3 and (text.isdigit() or text == "")), '%P')
        self.entry_chap.config(validate="key", validatecommand=vcmd)
        
        btn_val_chap = tk.Button(chap_frame, text="✓", command=self._validate_chapter,
                                  font=("Segoe UI", 10), bg=SUCCESS_COLOR, fg="white",
                                  relief="flat", cursor="hand2", width=3)
        btn_val_chap.pack(side="left")
        
        self.lbl_chap_desc = tk.Label(fields_frame, text="", font=("Segoe UI", 9), bg=FRAME_BG_COLOR, fg=INFO_COLOR, anchor="w")
        self.lbl_chap_desc.grid(row=0, column=2, pady=8, sticky="w", padx=5)
        
        # Product with validation button  
        self._create_label(fields_frame, "Product Number *:", 1)
        prod_frame = tk.Frame(fields_frame, bg=FRAME_BG_COLOR)
        prod_frame.grid(row=1, column=1, pady=8, sticky="ew", padx=(0, 10))
        
        self.entry_prod = tk.Entry(prod_frame, font=("Segoe UI", 10), relief="solid", borderwidth=1, width=12)
        self.entry_prod.pack(side="left", padx=(0, 5))
        vcmd2 = (self.entry_prod.register(lambda text: len(text) <= 12), '%P')
        self.entry_prod.config(validate="key", validatecommand=vcmd2)
        
        btn_val_prod = tk.Button(prod_frame, text="✓", command=self._validate_product,
                                  font=("Segoe UI", 10), bg=SUCCESS_COLOR, fg="white",
                                  relief="flat", cursor="hand2", width=3)
        btn_val_prod.pack(side="left")
        
        self.lbl_prod_desc = tk.Label(fields_frame, text="", font=("Segoe UI", 9), bg=FRAME_BG_COLOR, fg=INFO_COLOR, anchor="w")
        self.lbl_prod_desc.grid(row=1, column=2, pady=8, sticky="w", padx=5)
        
        # Build rest of form dynamically (skip first 2 fields)
        from src.components.form_builder import FormBuilder
        self.form_builder = FormBuilder(fields_frame)
        
        # Manual entries for validated fields
        self.form_builder.entries = {
            'targ_prochapter': self.entry_chap,
            'targ_pronumber': self.entry_prod
        }
        
        # Create remaining fields starting from row 2
        field_defs = self.get_field_definitions()[2:]  # Skip chapter and pronumber
        for i, field_def in enumerate(field_defs, start=2):
            name = field_def['name']
            label = field_def['label']
            field_type = field_def.get('type', 'text')
            width = field_def.get('width', 20)
            maxlength = field_def.get('maxlength', None)
            
            self._create_label(fields_frame, label, i)
            
            if field_type == 'numeric':
                from src.components.ui_components import UIComponents
                entry = UIComponents.create_numeric_entry(fields_frame, i, width=width, maxlength=maxlength, decimals=2)
                # Make description and unit readonly
                if name in ['targ_prodescription', 'targ_prounit']:
                    entry.config(state='readonly', readonlybackground='#F0F0F0')
            else:
                entry = self._create_entry_simple(fields_frame, i, width=width, maxlength=maxlength)
                if name in ['targ_prodescription', 'targ_prounit']:
                    entry.config(state='readonly', readonlybackground='#F0F0F0')
            
            self.form_builder.entries[name] = entry
        
        fields_frame.columnconfigure(1, weight=1)
        
        # Status label
        from src.components.ui_components import UIComponents
        self.status_label = UIComponents.create_status_label(parent)
        
        # CRUD buttons
        UIComponents.create_crud_buttons(parent, self._save_record, self._update_record, self._delete_record, self._clear_form)
    
    def _create_label(self, parent, text, row):
        label = tk.Label(parent, text=text, font=("Segoe UI", 10), bg=FRAME_BG_COLOR, fg=TEXT_COLOR, anchor="w")
        label.grid(row=row, column=0, pady=8, sticky="w", padx=10)
        return label
    
    def _create_entry_simple(self, parent, row, width=None, maxlength=None):
        entry = tk.Entry(parent, font=("Segoe UI", 10), relief="solid", borderwidth=1, width=width if width else 0)
        if maxlength:
            vcmd = (entry.register(lambda text: len(text) <= maxlength), '%P')
            entry.config(validate="key", validatecommand=vcmd)
        entry.grid(row=row, column=1, pady=8, padx=(0, 10), sticky="ew" if not width else "")
        return entry
    
    def _validate_chapter(self):
        """Validate chapter against Chapters DB"""
        chap_number = self.entry_chap.get().strip()
        if not chap_number:
            return
        
        try:
            chap_num = int(chap_number)
            chapter = self.chapter_db.get_chapter_by_number(chap_num)
            
            if chapter:
                self.current_chapter = chapter
                self.lbl_chap_desc.config(text=f"✓ {chapter.chap_description}", fg=SUCCESS_COLOR)
                self.entry_prod.focus()
            else:
                self.current_chapter = None
                self.lbl_chap_desc.config(text="", fg=DANGER_COLOR)
                messagebox.showerror("Chapter No Existe", f"El Chapter '{chap_number}' no existe.\nPor favor ingrese un número válido.")
                self.entry_chap.focus()
                self.entry_chap.select_range(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "El Chapter Number debe ser un número válido")
            self.entry_chap.focus()
    
    def _validate_product(self):
        """Validate product against Products DB"""
        if not self.current_chapter:
            messagebox.showwarning("Advertencia", "Primero valide un Chapter Number")
            self.entry_chap.focus()
            return
        
        pro_number = self.entry_prod.get().strip()
        if not pro_number:
            return
        
        product = self.product_db.get_product_by_part(pro_number)
        
        if product:
            self.current_product = product
            self.lbl_prod_desc.config(text=f"✓ {product.pro_description} ({product.pro_unit})", fg=SUCCESS_COLOR)
            
            # Fill description, unit and price
            self.form_builder.entries['targ_prodescription'].config(state='normal')
            self.form_builder.entries['targ_prodescription'].delete(0, tk.END)
            self.form_builder.entries['targ_prodescription'].insert(0, product.pro_description)
            self.form_builder.entries['targ_prodescription'].config(state='readonly')
            
            self.form_builder.entries['targ_prounit'].config(state='normal')
            self.form_builder.entries['targ_prounit'].delete(0, tk.END)
            self.form_builder.entries['targ_prounit'].insert(0, product.pro_unit)
            self.form_builder.entries['targ_prounit'].config(state='readonly')
            
            # Fill price from product
            self.form_builder.entries['targ_proprice1'].delete(0, tk.END)
            if product.pro_price1:
                formatted_price = f"{product.pro_price1:,.2f}"
                self.form_builder.entries['targ_proprice1'].insert(0, formatted_price)
        else:
            self.current_product = None
            self.lbl_prod_desc.config(text="", fg=DANGER_COLOR)
            messagebox.showerror("Producto No Existe", f"El producto '{pro_number}' no existe.\nPor favor ingrese un número válido.")
            self.entry_prod.focus()
            self.entry_prod.select_range(0, tk.END)
    
    def _save_record(self):
        """Override to validate chapter first"""
        if not self.current_chapter:
            messagebox.showerror("Error", "Debe validar un Chapter Number primero")
            self.entry_chap.focus()
            return
        
        # Product validation is optional - user can enter any product number
        # Call parent save (which will call _clear_form if successful)
        super()._save_record()
        
        # After successful save, reset chapter validation state
        # (product state is reset in _clear_form)
        if self.current_record_key is None:  # Save was successful if key is cleared
            self.current_chapter = None
            self.current_product = None
            self.lbl_chap_desc.config(text="")
            self.lbl_prod_desc.config(text="")
    
    def _clear_form(self):
        """Override to reset validation labels and readonly fields"""
        self.current_chapter = None
        self.current_product = None
        self.lbl_chap_desc.config(text="")
        self.lbl_prod_desc.config(text="")
        
        # Temporarily enable readonly fields to clear them
        if 'targ_prodescription' in self.form_builder.entries:
            self.form_builder.entries['targ_prodescription'].config(state='normal')
        if 'targ_prounit' in self.form_builder.entries:
            self.form_builder.entries['targ_prounit'].config(state='normal')
        
        # Clear all fields
        super()._clear_form()
        
        # Set readonly fields back to readonly
        if 'targ_prodescription' in self.form_builder.entries:
            self.form_builder.entries['targ_prodescription'].config(state='readonly')
        if 'targ_prounit' in self.form_builder.entries:
            self.form_builder.entries['targ_prounit'].config(state='readonly')
    
    def render(self):
        """Override to use Project submenu back button"""
        self.clear_container()
        
        from src.components.ui_components import UIComponents
        UIComponents.create_header(self.container, self.get_title())
        
        content_frame = tk.Frame(self.container, bg=WINDOW_BG_COLOR)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        form_panel = tk.Frame(content_frame, bg=FRAME_BG_COLOR, relief="ridge", borderwidth=2)
        form_panel.pack(fill="both", expand=True)
        
        self._create_form(form_panel)
        
        # Footer
        footer_frame = tk.Frame(self.container, bg=WINDOW_BG_COLOR)
        footer_frame.pack(fill="x", padx=10, pady=10)
        
        btn_back = tk.Button(footer_frame, text="← Regresar a Project",
                            command=self.app_controller.show_project_submenu,
                            font=("Segoe UI", 10), bg=SECONDARY_COLOR, fg="white",
                            activebackground=ACCENT_COLOR, relief="flat", cursor="hand2", padx=20, pady=10)
        btn_back.pack(side="left")
