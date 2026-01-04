"""
Create Targets View (Refactored with BaseCRUDView)
Custom validation with cross-database lookups
"""

import tkinter as tk
from tkinter import messagebox
from src.views.base_crud_view import BaseCRUDView
from src.database.target_db import TargetDatabase
from src.database.chapter_db import ChapterDB
from src.database.product_db import ProductDatabase
from src.models.target import Target
from config.settings import *


class CreateTargetsView(BaseCRUDView):
    """Create Targets view with cross-database validation"""
    
    def __init__(self, container, app_controller):
        self.chapter_db = ChapterDB()
        self.product_db = ProductDatabase()
        self.current_chapter = None
        self.current_product = None
        super().__init__(container, app_controller)
        self.db = TargetDatabase()
    
    def get_title(self):
        return "Create Targets"
    
    def get_field_definitions(self):
        return [
            {'name': 'targ_prochapter', 'label': 'Chapter Number *:', 'type': 'text', 'width': 5, 'maxlength': 4},
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
        return 'target_id'
    
    def get_record_by_primary_key(self, key):
        return self.db.get_target_by_id(key)
    
    def search_by_secondary_key(self, value):
        return self.db.search_by_description(value)
    
    def get_all_records(self):
        return self.db.get_all_targets()
    
    def create_record(self, model):
        return self.db.create_target(model)
    
    def update_record(self, model):
        return self.db.update_target(model)
    
    def delete_record(self, primary_key):
        return self.db.delete_target_by_id(primary_key)
    
    def get_list_columns(self):
        return [
            ('targ_prochapter', 'Chapter', 80),
            ('targ_pronumber', 'ProNumber', 120),
            ('targ_prodescription', 'Description', 300),
            ('targ_prounit', 'Unit', 80),
            ('targ_proprice1', 'Price', 120)
        ]
    
    def _open_list_popup(self):
        """Override to handle composite key (chapter + pronumber)"""
        import tkinter as tk
        from tkinter import ttk
        
        list_window = tk.Toplevel(self.container)
        list_window.title(f"Lista de {self.get_title()}")
        list_window.geometry("900x500")
        list_window.configure(bg=WINDOW_BG_COLOR)
        
        # Header
        header_frame = tk.Frame(list_window, bg=HEADER_BG_COLOR, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text=f"Lista de {self.get_title()}",
            font=("Segoe UI", 16, "bold"),
            bg=HEADER_BG_COLOR,
            fg=HEADER_TEXT_COLOR
        )
        title.pack(pady=10)
        
        # Search frame
        search_frame = tk.Frame(list_window, bg=WINDOW_BG_COLOR)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(
            search_frame,
            text="Search:",
            font=("Segoe UI", 10),
            bg=WINDOW_BG_COLOR,
            fg=TEXT_COLOR
        ).pack(side="left", padx=5)
        
        search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Tree frame
        tree_frame = tk.Frame(list_window, bg=FRAME_BG_COLOR)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        columns = self.get_list_columns()
        column_names = [col[0] for col in columns]
        
        tree = ttk.Treeview(
            tree_frame,
            columns=column_names,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )
        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        
        for col_name, col_display, col_width in columns:
            tree.heading(col_name, text=col_display)
            # Alinear columna Price a la derecha
            if col_name == 'targ_proprice1':
                tree.column(col_name, width=col_width, anchor='e')
            else:
                tree.column(col_name, width=col_width)
        
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        def load_records(search_term=""):
            """Load records into tree"""
            for item in tree.get_children():
                tree.delete(item)
            
            if search_term:
                records = self.search_by_secondary_key(search_term)
            else:
                records = self.get_all_records()
            
            for record in records:
                values = []
                for col_name, _, _ in columns:
                    value = getattr(record, col_name, "")
                    # Normalize chapter number to 4 characters for display
                    if col_name == 'targ_prochapter' and value:
                        value = str(value).zfill(4) if str(value).isdigit() else str(value)
                    values.append(value)
                # Store target_id as hidden data using tags
                tree.insert("", "end", values=values, tags=(str(record.target_id),))
        
        def search_in_popup():
            search_term = search_entry.get().strip()
            load_records(search_term)
        
        btn_search = tk.Button(
            search_frame,
            text="🔍 Search",
            command=search_in_popup,
            font=("Segoe UI", 10),
            bg=INFO_COLOR,
            fg="white",
            activebackground="#138D75",
            relief="flat",
            cursor="hand2",
            padx=10
        )
        btn_search.pack(side="left", padx=5)
        
        search_entry.bind("<Return>", lambda e: search_in_popup())
        
        def on_select_popup(event):
            selection = tree.selection()
            if selection:
                item = selection[0]
                # Get target_id from tags
                tags = tree.item(item, 'tags')
                if tags:
                    target_id = tags[0]
                    
                    record = self.db.get_target_by_id(target_id)
                    
                    if record:
                        self.current_record_key = str(target_id)
                        self._populate_form(record)
                        self.status_label.config(
                            text=f"✓ Registro cargado",
                            fg=SUCCESS_COLOR
                        )
                        list_window.destroy()
        
        # Bind both double-click and Enter key
        tree.bind('<Double-Button-1>', on_select_popup)
        tree.bind('<Return>', on_select_popup)
        
        # Load all records initially
        load_records()
        
        # Button frame
        button_frame = tk.Frame(list_window, bg=WINDOW_BG_COLOR)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        btn_close = tk.Button(
            button_frame,
            text="Cerrar",
            command=list_window.destroy,
            font=("Segoe UI", 10),
            bg=SECONDARY_COLOR,
            fg="white",
            activebackground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8
        )
        btn_close.pack(side="right")
        
        search_entry.focus()
    
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
        vcmd = (self.entry_chap.register(lambda text: len(text) <= 4), '%P')
        self.entry_chap.config(validate="key", validatecommand=vcmd)
        self.entry_chap.bind("<FocusOut>", lambda e: self._validate_chapter())
        
        btn_search_chap = tk.Button(chap_frame, text="Search", command=self._open_chapter_search,
                                     font=("Segoe UI", 9), bg=INFO_COLOR, fg="white",
                                     relief="flat", cursor="hand2", padx=10, pady=5)
        btn_search_chap.pack(side="left")
        
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
        self.entry_prod.bind("<FocusOut>", lambda e: self._validate_product())
        
        btn_search_prod = tk.Button(prod_frame, text="Search", command=self._open_product_search,
                                     font=("Segoe UI", 9), bg=INFO_COLOR, fg="white",
                                     relief="flat", cursor="hand2", padx=10, pady=5)
        btn_search_prod.pack(side="left")
        
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
        
        # Hidden field to store target_id for updates
        self.target_id_var = tk.StringVar()
        
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
            else:
                entry = self._create_entry_simple(fields_frame, i, width=width, maxlength=maxlength)
                # Description and unit are editable (will be filled automatically if product exists)
            
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
        """Validate chapter against Chapters DB (optional)"""
        chap_number = self.entry_chap.get().strip()
        if not chap_number:
            self.lbl_chap_desc.config(text="", fg=INFO_COLOR)
            return
        
        # Normalize to 4 characters if numeric
        if chap_number.isdigit():
            chap_number = chap_number.zfill(4)
            self.entry_chap.delete(0, tk.END)
            self.entry_chap.insert(0, chap_number)
        
        # Don't allow 0000 as a valid chapter
        if chap_number == "0000":
            self.current_chapter = None
            self.lbl_chap_desc.config(text="✗ Chapter 0000 no es válido", fg=DANGER_COLOR)
            return
        
        try:
            chapter = self.chapter_db.get_by_number(chap_number)
            
            if chapter:
                self.current_chapter = chapter
                self.lbl_chap_desc.config(text=f"✓ {chapter.chap_description}", fg=SUCCESS_COLOR)
            else:
                self.current_chapter = None
                self.lbl_chap_desc.config(text="⚠ Chapter no encontrado (se guardará de todos modos)", fg=WARNING_COLOR)
            
            self.entry_prod.focus()
        except ValueError:
            self.lbl_chap_desc.config(text="⚠ Formato inválido", fg=WARNING_COLOR)
            self.entry_prod.focus()
    
    def _validate_product(self):
        """Validate product against Products DB (optional - autocomplete if exists)"""
        pro_number = self.entry_prod.get().strip()
        if not pro_number:
            return
        
        product = self.product_db.get_product_by_part(pro_number)
        
        if product:
            self.current_product = product
            self.lbl_prod_desc.config(text=f"✓ {product.pro_description} ({product.pro_unit})", fg=SUCCESS_COLOR)
            
            # Fill description, unit and price (campos editables)
            self.form_builder.entries['targ_prodescription'].delete(0, tk.END)
            self.form_builder.entries['targ_prodescription'].insert(0, product.pro_description)
            
            self.form_builder.entries['targ_prounit'].delete(0, tk.END)
            self.form_builder.entries['targ_prounit'].insert(0, product.pro_unit)
            
            # Fill price from product
            self.form_builder.entries['targ_proprice1'].delete(0, tk.END)
            if product.pro_price1:
                formatted_price = f"{product.pro_price1:,.2f}"
                self.form_builder.entries['targ_proprice1'].insert(0, formatted_price)
        else:
            self.current_product = None
            self.lbl_prod_desc.config(text="⚠ Producto no encontrado (puede ingresar descripción manualmente)", fg=WARNING_COLOR)
    
    def _populate_form(self, record):
        """Override to populate form including target_id"""
        # Store target_id for updates
        if hasattr(record, 'target_id') and record.target_id:
            self.target_id_var.set(str(record.target_id))
        
        # Call parent populate
        super()._populate_form(record)
        
        # Update validation labels if chapter/product exist
        if record.targ_prochapter:
            # Normalize chapter number to 4 characters for lookup
            chapter_num = str(record.targ_prochapter).zfill(4) if str(record.targ_prochapter).isdigit() else str(record.targ_prochapter)
            chapter = self.chapter_db.get_by_number(chapter_num)
            if chapter:
                self.lbl_chap_desc.config(text=f"✓ {chapter.chap_description}", fg=SUCCESS_COLOR)
        
        if record.targ_pronumber:
            product = self.product_db.get_product_by_part(record.targ_pronumber)
            if product:
                self.lbl_prod_desc.config(text=f"✓ {product.pro_description} ({product.pro_unit})", fg=SUCCESS_COLOR)
    
    def _update_record(self):
        """Override to include target_id in update"""
        if not self.current_record_key:
            messagebox.showwarning("Advertencia", "Seleccione un registro de la lista primero")
            return
        
        values = self.form_builder.get_values()
        
        # Include target_id from stored value
        target_id = self.target_id_var.get()
        if target_id:
            values['target_id'] = int(target_id)
        
        try:
            model_class = self.get_model_class()
            model = model_class(**values)
            
            if self.update_record(model):
                messagebox.showinfo("Éxito", "Registro actualizado correctamente")
                self._clear_form()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el registro")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
    
    def _save_record(self):
        """Override to add chapter validation before save"""
        # Validate chapter number
        chap_number = self.entry_chap.get().strip()
        if not chap_number or chap_number == "0000":
            messagebox.showerror("Validación", "Debe ingresar un Chapter Number válido (no puede ser 0000 o vacío)")
            self.entry_chap.focus()
            return
        
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
        """Override to reset validation labels and target_id"""
        self.current_chapter = None
        self.current_product = None
        self.lbl_chap_desc.config(text="")
        self.lbl_prod_desc.config(text="")
        self.target_id_var.set("")  # Clear target_id
        
        # Clear all fields
        super()._clear_form()
    
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
    
    def _open_chapter_search(self):
        """Open chapter search popup window"""
        from tkinter import ttk
        
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
        all_chapters = self.chapter_db.get_all()
        
        if not all_chapters:
            messagebox.showinfo("No Data", "No chapters found in database")
            popup.destroy()
            return
        
        # Create treeview
        tree_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
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
                self.entry_chap.delete(0, tk.END)
                self.entry_chap.insert(0, chapter_number)
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
    
    def _open_product_search(self):
        """Open product search popup window"""
        from tkinter import ttk
        
        # Create popup window
        popup = tk.Toplevel(self.container)
        popup.title("Select Product")
        popup.geometry("900x600")
        popup.configure(bg=WINDOW_BG_COLOR)
        popup.transient(self.container)
        popup.grab_set()
        
        # Header
        header_frame = tk.Frame(popup, bg=ACCENT_COLOR)
        header_frame.pack(fill="x")
        
        header_label = tk.Label(
            header_frame,
            text="Select Product",
            font=FONTS["header"],
            bg=ACCENT_COLOR,
            fg="white",
            pady=15
        )
        header_label.pack()
        
        # Content frame
        content_frame = tk.Frame(popup, bg=FRAME_BG_COLOR, relief="ridge", borderwidth=2)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Get all products
        all_products = self.product_db.get_all_products()
        
        if not all_products:
            messagebox.showinfo("No Data", "No products found in database")
            popup.destroy()
            return
        
        # Create treeview
        tree_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        columns = ("Part", "Description", "Unit", "Price")
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
        tree.heading("Part", text="Part Number")
        tree.heading("Description", text="Description")
        tree.heading("Unit", text="Unit")
        tree.heading("Price", text="Price")
        
        tree.column("Part", width=150, anchor="center")
        tree.column("Description", width=400, anchor="w")
        tree.column("Unit", width=100, anchor="center")
        tree.column("Price", width=150, anchor="e")
        
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Populate tree
        for product in all_products:
            price = f"${product.pro_price1:,.2f}" if product.pro_price1 else "$0.00"
            tree.insert("", "end", values=(
                product.pro_part,
                product.pro_description or "",
                product.pro_unit or "",
                price
            ))
        
        # Double-click to select
        def on_select(event):
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                part_number = item['values'][0]
                self.entry_prod.delete(0, tk.END)
                self.entry_prod.insert(0, part_number)
                self._validate_product()
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
