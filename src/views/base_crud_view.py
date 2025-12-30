"""
Base CRUD View - Abstract base class with complete CRUD logic
All view classes inherit from this to eliminate code duplication
"""

import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from src.views.base_view import BaseView
from src.components.ui_components import UIComponents
from src.components.form_builder import FormBuilder
from config.settings import *


class BaseCRUDView(BaseView, ABC):
    """
    Base class for all CRUD views
    
    Subclasses must implement:
    - get_title() -> str
    - get_field_definitions() -> list
    - get_database() -> database instance
    - get_model_class() -> model class
    - get_primary_key_name() -> str (e.g., 'mat_number', 'prod_code')
    - get_record_by_primary_key(key) -> model instance
    - search_by_secondary_key(value) -> list of model instances
    - get_all_records() -> list of model instances
    - create_record(model) -> record_id or None
    - update_record(model) -> bool
    - delete_record(primary_key) -> bool
    - get_list_columns() -> list of tuples (column_name, display_name, width)
    """
    
    def __init__(self, container, app_controller):
        super().__init__(container, app_controller)
        self.current_record_key = None
        self.all_records = []
        self.current_index = -1
        self.form_builder = None
        self.status_label = None
    
    @abstractmethod
    def get_title(self):
        """Return view title (e.g., 'Materials Management')"""
        pass
    
    @abstractmethod
    def get_field_definitions(self):
        """
        Return list of field definitions for form builder
        Example:
        [
            {'name': 'mat_number', 'label': 'Material Number *:', 'type': 'primary', 'width': 12, 'maxlength': 12},
            {'name': 'mat_name', 'label': 'Name *:', 'type': 'secondary', 'width': 30, 'maxlength': 30},
            {'name': 'mat_quantity', 'label': 'Quantity:', 'type': 'numeric', 'width': 15, 'maxlength': 12, 'decimals': 2}
        ]
        """
        pass
    
    @abstractmethod
    def get_database(self):
        """Return database instance"""
        pass
    
    @abstractmethod
    def get_model_class(self):
        """Return model class"""
        pass
    
    @abstractmethod
    def get_primary_key_name(self):
        """Return primary key field name (e.g., 'mat_number')"""
        pass
    
    @abstractmethod
    def get_record_by_primary_key(self, key):
        """Fetch record by primary key"""
        pass
    
    @abstractmethod
    def search_by_secondary_key(self, value):
        """Search records by secondary key (usually name)"""
        pass
    
    @abstractmethod
    def get_all_records(self):
        """Get all records from database"""
        pass
    
    @abstractmethod
    def create_record(self, model):
        """Create new record in database"""
        pass
    
    @abstractmethod
    def update_record(self, model):
        """Update existing record"""
        pass
    
    @abstractmethod
    def delete_record(self, primary_key):
        """Delete record by primary key"""
        pass
    
    @abstractmethod
    def get_list_columns(self):
        """
        Return list columns configuration
        Example: [('mat_number', 'Material Number', 120), ('mat_name', 'Name', 250)]
        """
        pass
    
    def render(self):
        """Render the CRUD view"""
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
        
        # Footer with back button
        UIComponents.create_footer_back_button(self.container, self.app_controller.show_catalog_submenu)
    
    def _create_form(self, parent):
        """Create the complete form"""
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
        UIComponents.create_navigation_buttons(
            parent,
            self._navigate_previous,
            self._open_list_popup,
            self._navigate_next
        )
        
        # Build dynamic form
        self.form_builder = FormBuilder(parent)
        self.form_builder.build_form(
            self.get_field_definitions(),
            primary_search_callback=self._search_by_primary,
            secondary_search_callback=self._search_by_secondary
        )
        
        # Status label
        self.status_label = UIComponents.create_status_label(parent)
        
        # CRUD buttons
        UIComponents.create_crud_buttons(
            parent,
            self._save_record,
            self._update_record,
            self._delete_record,
            self._clear_form
        )
    
    def _search_by_primary(self):
        """Search by primary key"""
        values = self.form_builder.get_values()
        primary_key = values.get(self.get_primary_key_name(), '').strip()
        
        if not primary_key:
            return
        
        record = self.get_record_by_primary_key(primary_key)
        
        if record:
            self.current_record_key = primary_key
            self._populate_form(record)
            self.status_label.config(
                text=f"✓ Registro encontrado",
                fg=SUCCESS_COLOR
            )
        else:
            self.current_record_key = None
            self.status_label.config(
                text=f"⚠ Registro '{primary_key}' no existe. Complete los datos para crear nuevo registro.",
                fg=WARNING_COLOR
            )
    
    def _search_by_secondary(self):
        """Search by secondary key (name)"""
        values = self.form_builder.get_values()
        field_defs = self.get_field_definitions()
        
        # Find secondary field
        secondary_field = None
        for field in field_defs:
            if field.get('type') == 'secondary':
                secondary_field = field['name']
                break
        
        if not secondary_field:
            return
        
        search_value = values.get(secondary_field, '').strip()
        
        if not search_value:
            return
        
        records = self.search_by_secondary_key(search_value)
        
        if records:
            if len(records) == 1:
                record = records[0]
                primary_key = getattr(record, self.get_primary_key_name())
                self.current_record_key = primary_key
                self._populate_form(record)
                self.status_label.config(
                    text=f"✓ Registro encontrado",
                    fg=SUCCESS_COLOR
                )
            else:
                self.status_label.config(
                    text=f"🔍 Se encontraron {len(records)} registros. Presione el botón Search para ver la lista.",
                    fg=INFO_COLOR
                )
        else:
            self.status_label.config(
                text=f"⚠ No se encontraron registros",
                fg=WARNING_COLOR
            )
    
    def _navigate_previous(self):
        """Navigate to previous record"""
        self.all_records = self.get_all_records()
        
        if not self.all_records:
            messagebox.showinfo("Info", "No hay registros en la base de datos")
            return
        
        if self.current_index <= 0:
            self.current_index = len(self.all_records) - 1
        else:
            self.current_index -= 1
        
        record = self.all_records[self.current_index]
        primary_key = getattr(record, self.get_primary_key_name())
        self.current_record_key = primary_key
        self._populate_form(record)
        self.status_label.config(
            text=f"Registro {self.current_index + 1} de {len(self.all_records)}",
            fg=INFO_COLOR
        )
    
    def _navigate_next(self):
        """Navigate to next record"""
        self.all_records = self.get_all_records()
        
        if not self.all_records:
            messagebox.showinfo("Info", "No hay registros en la base de datos")
            return
        
        if self.current_index >= len(self.all_records) - 1:
            self.current_index = 0
        else:
            self.current_index += 1
        
        record = self.all_records[self.current_index]
        primary_key = getattr(record, self.get_primary_key_name())
        self.current_record_key = primary_key
        self._populate_form(record)
        self.status_label.config(
            text=f"Registro {self.current_index + 1} de {len(self.all_records)}",
            fg=INFO_COLOR
        )
    
    def _populate_form(self, record):
        """Populate form with record data"""
        values = record.to_dict()
        self.form_builder.set_values(values)
    
    def _clear_form(self):
        """Clear all form fields"""
        self.current_record_key = None
        self.current_index = -1
        self.form_builder.clear_all()
        self.status_label.config(text="")
        self.form_builder.focus_first()
    
    def _save_record(self):
        """Save new record"""
        values = self.form_builder.get_values()
        
        # Validate required fields (marked with * in label)
        required_fields = [f['name'] for f in self.get_field_definitions() if '*' in f['label']]
        for field in required_fields:
            if not values.get(field):
                messagebox.showerror("Error", "Por favor complete los campos obligatorios (*)")
                return
        
        try:
            model_class = self.get_model_class()
            model = model_class(**values)
            
            record_id = self.create_record(model)
            
            if record_id:
                messagebox.showinfo("Éxito", "Registro guardado correctamente")
                self._clear_form()
            else:
                primary_label = self.get_primary_key_name().replace('_', '.').title()
                messagebox.showerror("Error", f"El {primary_label} ya existe en la base de datos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def _update_record(self):
        """Update existing record"""
        if not self.current_record_key:
            messagebox.showwarning("Advertencia", "Seleccione un registro de la lista primero")
            return
        
        values = self.form_builder.get_values()
        
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
    
    def _delete_record(self):
        """Delete selected record"""
        if not self.current_record_key:
            messagebox.showwarning("Advertencia", "Seleccione un registro de la lista primero")
            return
        
        result = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de eliminar el registro '{self.current_record_key}'?"
        )
        
        if result:
            if self.delete_record(self.current_record_key):
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                self._clear_form()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el registro")
    
    def _open_list_popup(self):
        """Open popup window with records list"""
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
                    values.append(getattr(record, col_name, ""))
                tree.insert("", "end", values=values)
        
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
                item = tree.item(selection[0])
                values = item['values']
                
                primary_key = str(values[0])  # Convert to string in case Treeview converts to int
                record = self.get_record_by_primary_key(primary_key)
                
                if record:
                    self.current_record_key = primary_key
                    self._populate_form(record)
                    self.status_label.config(
                        text=f"✓ Registro cargado",
                        fg=SUCCESS_COLOR
                    )
                    list_window.destroy()
        
        tree.bind('<<TreeviewSelect>>', on_select_popup)
        
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
