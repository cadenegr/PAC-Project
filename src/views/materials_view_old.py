"""
Materials Management View
Complete CRUD interface for materials with auto-search and navigation
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.views.base_view import BaseView
from config.settings import *
from src.database.material_db import MaterialDatabase
from src.models.material import Material


class MaterialsView(BaseView):
    """Materials management view with CRUD operations"""
    
    def __init__(self, container, app_controller):
        super().__init__(container, app_controller)
        self.db = MaterialDatabase()
        self.current_material = None
        self.all_materials = []  # Lista de todos los materiales
        self.current_index = -1  # Índice actual en la lista
    
    def _format_number(self, value):
        """Formatear número con comas para miles y punto para decimales"""
        try:
            num = float(value)
            return f"{num:,.2f}"
        except (ValueError, TypeError):
            return "0.00"
    
    def _parse_number(self, formatted_str):
        """Parsear número formateado removiendo comas"""
        try:
            # Remover comas y convertir a float
            clean_str = formatted_str.replace(",", "")
            return float(clean_str)
        except (ValueError, AttributeError):
            return 0.0
    
    def render(self):
        """Render the materials management view"""
        self.clear_container()
        
        # Header
        header_frame = tk.Frame(self.container, bg=HEADER_BG_COLOR, height=60)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="Materials Management",
            font=("Segoe UI", 18, "bold"),
            bg=HEADER_BG_COLOR,
            fg=HEADER_TEXT_COLOR
        )
        title.pack(pady=15)
        
        # Main content area - Solo el formulario para móvil
        content_frame = tk.Frame(self.container, bg=WINDOW_BG_COLOR)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Panel del formulario (ocupa todo el ancho)
        form_panel = tk.Frame(content_frame, bg=FRAME_BG_COLOR, relief="ridge", borderwidth=2)
        form_panel.pack(fill="both", expand=True)
        
        self._create_form(form_panel)
        
        # Footer with back button
        footer_frame = tk.Frame(self.container, bg=WINDOW_BG_COLOR)
        footer_frame.pack(fill="x", padx=10, pady=10)
        
        btn_back = tk.Button(
            footer_frame,
            text="← Regresar al Catálogo",
            command=self.app_controller.show_catalog_submenu,
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
    
    def _create_form(self, parent):
        """Create the material entry form with auto-search and navigation"""
        form_title = tk.Label(
            parent,
            text="Datos del Material",
            font=("Segoe UI", 14, "bold"),
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR
        )
        form_title.pack(pady=15)
        
        # Navigation frame with arrows and search button
        nav_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        nav_frame.pack(pady=5)
        
        btn_prev = tk.Button(
            nav_frame,
            text="▲",
            command=self._navigate_previous,
            font=("Segoe UI", 14, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            activebackground=SECONDARY_COLOR,
            relief="flat",
            cursor="hand2",
            width=3,
            height=1
        )
        btn_prev.pack(side="left", padx=5)
        
        # Botón de búsqueda para abrir lista de materiales
        btn_search_list = tk.Button(
            nav_frame,
            text="🔍 Search",
            command=self._open_materials_list,
            font=("Segoe UI", 10, "bold"),
            bg=INFO_COLOR,
            fg="white",
            activebackground="#138D75",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5
        )
        btn_search_list.pack(side="left", padx=10)
        
        btn_next = tk.Button(
            nav_frame,
            text="▼",
            command=self._navigate_next,
            font=("Segoe UI", 14, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            activebackground=SECONDARY_COLOR,
            relief="flat",
            cursor="hand2",
            width=3,
            height=1
        )
        btn_next.pack(side="left", padx=5)
        
        # Form fields container
        fields_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        fields_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Raw.Part (Primary Key) - Con búsqueda automática
        self._create_field(fields_frame, "Part Number *:", 0)
        
        # Frame para Raw.Part con botón de búsqueda
        part_frame = tk.Frame(fields_frame, bg=FRAME_BG_COLOR)
        part_frame.grid(row=0, column=1, pady=8, sticky="ew", padx=(0, 10))
        
        self.entry_raw_part = tk.Entry(
            part_frame,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            width=20
        )
        self.entry_raw_part.pack(side="left", padx=(0, 5))
        
        # Validación de longitud máxima
        vcmd = (self.entry_raw_part.register(lambda text: len(text) <= 20), '%P')
        self.entry_raw_part.config(validate="key", validatecommand=vcmd)
        
        # Vincular evento cuando se presiona Enter en Raw.Part
        self.entry_raw_part.bind("<Return>", lambda e: self._search_by_part())
        self.entry_raw_part.bind("<FocusOut>", lambda e: self._search_by_part())
        
        btn_search = tk.Button(
            part_frame,
            text="🔍",
            command=self._search_by_part,
            font=("Segoe UI", 10),
            bg=INFO_COLOR,
            fg="white",
            activebackground="#138D75",
            relief="flat",
            cursor="hand2",
            width=3
        )
        btn_search.pack(side="left")
        
        # Raw.Description (también llave de búsqueda)
        self._create_field(fields_frame, "Description *:", 1)
        self.entry_raw_description = self._create_entry(fields_frame, 1, width=50, maxlength=100)
        self.entry_raw_description.bind("<Return>", lambda e: self._search_by_description())
        
        btn_search_desc = tk.Button(
            fields_frame,
            text="🔍",
            command=self._search_by_description,
            font=("Segoe UI", 10),
            bg=INFO_COLOR,
            fg="white",
            activebackground="#138D75",
            relief="flat",
            cursor="hand2",
            width=3
        )
        btn_search_desc.grid(row=1, column=2, pady=8, padx=5)
        
        # Raw.Unit
        self._create_field(fields_frame, "Unit Measure *:", 2)
        self.entry_raw_unit = self._create_entry(fields_frame, 2, width=10, maxlength=10)
        
        # Raw.Price1
        self._create_field(fields_frame, "Actual Price:", 3)
        self.entry_raw_price1 = self._create_entry(fields_frame, 3, self._format_number(0), width=12, maxlength=12)
        
        # Raw.Price2
        self._create_field(fields_frame, "Preview Price:", 4)
        self.entry_raw_price2 = self._create_entry(fields_frame, 4, self._format_number(0), width=12, maxlength=12)
        
        # Raw.Balance
        self._create_field(fields_frame, "Unit Balance:", 5)
        self.entry_raw_balance = self._create_entry(fields_frame, 5, self._format_number(0), width=12, maxlength=12)
        self.entry_raw_balance.config(state="readonly", readonlybackground="#F8F9F9")
        
        # Raw.IN
        self._create_field(fields_frame, "Total IN:", 6)
        self.entry_raw_in = self._create_entry(fields_frame, 6, "0", width=10, maxlength=10)
        
        # Raw.OUT
        self._create_field(fields_frame, "Total OUT:", 7)
        self.entry_raw_out = self._create_entry(fields_frame, 7, "0", width=10, maxlength=10)
        
        fields_frame.columnconfigure(1, weight=1)
        
        # Status label para mostrar mensajes
        self.status_label = tk.Label(
            parent,
            text="",
            font=("Segoe UI", 9),
            bg=FRAME_BG_COLOR,
            fg=INFO_COLOR
        )
        self.status_label.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        button_frame.pack(pady=20, padx=20, fill="x")
        
        btn_save = tk.Button(
            button_frame,
            text="💾 Guardar",
            command=self._save_material,
            font=("Segoe UI", 10, "bold"),
            bg=SUCCESS_COLOR,
            fg="white",
            activebackground="#229954",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )
        btn_save.pack(side="left", padx=5)
        
        btn_update = tk.Button(
            button_frame,
            text="✏️ Actualizar",
            command=self._update_material,
            font=("Segoe UI", 10, "bold"),
            bg=WARNING_COLOR,
            fg="white",
            activebackground="#D68910",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )
        btn_update.pack(side="left", padx=5)
        
        btn_delete = tk.Button(
            button_frame,
            text="🗑️ Eliminar",
            command=self._delete_material,
            font=("Segoe UI", 10, "bold"),
            bg=DANGER_COLOR,
            fg="white",
            activebackground="#C0392B",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )
        btn_delete.pack(side="left", padx=5)
        
        btn_clear = tk.Button(
            button_frame,
            text="🔄 Limpiar",
            command=self._clear_form,
            font=("Segoe UI", 10),
            bg=SECONDARY_COLOR,
            fg="white",
            activebackground=ACCENT_COLOR,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )
        btn_clear.pack(side="left", padx=5)
    
    def _create_field(self, parent, label_text, row):
        """Create a form field label"""
        label = tk.Label(
            parent,
            text=label_text,
            font=("Segoe UI", 10),
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR,
            anchor="w"
        )
        label.grid(row=row, column=0, pady=8, sticky="w", padx=10)
    
    def _create_entry(self, parent, row, default="", width=None, maxlength=None):
        """Create a form entry field with optional width and max length validation"""
        entry = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            width=width if width else 0
        )
        entry.insert(0, default)
        
        # Aplicar validación de longitud máxima si se especifica
        if maxlength:
            validate_cmd = (entry.register(lambda text: len(text) <= maxlength), '%P')
            entry.config(validate="key", validatecommand=validate_cmd)
        
        if width:
            entry.grid(row=row, column=1, pady=8, padx=(0, 10))
        else:
            entry.grid(row=row, column=1, pady=8, sticky="ew", padx=(0, 10))
        
        return entry
    
    def _create_list(self, parent):
        """Create the materials list/table"""
        list_title = tk.Label(
            parent,
            text="Lista de Materiales",
            font=("Segoe UI", 14, "bold"),
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR
        )
        list_title.pack(pady=15)
        
        # Search bar
        search_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        search_frame.pack(padx=20, pady=10, fill="x")
        
        tk.Label(
            search_frame,
            text="Search:",
            font=("Segoe UI", 10),
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR
        ).pack(side="left", padx=(0, 10))
        
        self.search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', lambda e: self._search_materials())
        
        btn_search = tk.Button(
            search_frame,
            text="🔍",
            command=self._search_materials,
            font=("Segoe UI", 10),
            bg=INFO_COLOR,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=5
        )
        btn_search.pack(side="left")
        
        # Treeview
        tree_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        tree_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Create treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("part", "description", "unit", "price1", "balance"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Define columns
        self.tree.heading("part", text="Part")
        self.tree.heading("description", text="Description")
        self.tree.heading("unit", text="Unit")
        self.tree.heading("price1", text="Price")
        self.tree.heading("balance", text="Balance")
        
        self.tree.column("part", width=100)
        self.tree.column("description", width=200)
        self.tree.column("unit", width=70)
        self.tree.column("price1", width=80)
        self.tree.column("balance", width=80)
        
        # Pack scrollbars and treeview
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind selection
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        
        # Delete button
        btn_delete = tk.Button(
            parent,
            text="🗑️ Eliminar Seleccionado",
            command=self._delete_material,
            font=("Segoe UI", 10),
            bg=DANGER_COLOR,
            fg="white",
            activebackground="#C0392B",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )
        btn_delete.pack(pady=10)
        
        # Load initial data
        self._load_materials()
    
    def _save_material(self):
        """Save new material to database"""
        # Validate required fields
        if not self.entry_raw_part.get() or not self.entry_raw_description.get() or not self.entry_raw_unit.get():
            messagebox.showerror("Error", "Por favor complete los campos obligatorios (*)")
            return
        
        try:
            material = Material(
                raw_part=self.entry_raw_part.get().strip(),
                raw_description=self.entry_raw_description.get().strip(),
                raw_unit=self.entry_raw_unit.get().strip(),
                raw_price1=self._parse_number(self.entry_raw_price1.get() or "0"),
                raw_price2=self._parse_number(self.entry_raw_price2.get() or "0"),
                raw_balance=self._parse_number(self.entry_raw_balance.get() or "0"),
                raw_in=int(self.entry_raw_in.get() or 0),
                raw_out=int(self.entry_raw_out.get() or 0)
            )
            
            material_id = self.db.create_material(material)
            
            if material_id:
                messagebox.showinfo("Éxito", "Material guardado correctamente")
                self._clear_form()
            else:
                messagebox.showerror("Error", "El Raw.Part ya existe en la base de datos")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
    
    def _update_material(self):
        """Update existing material"""
        if not self.current_material:
            messagebox.showwarning("Advertencia", "Seleccione un material de la lista primero")
            return
        
        try:
            material = Material(
                raw_part=self.entry_raw_part.get().strip(),
                raw_description=self.entry_raw_description.get().strip(),
                raw_unit=self.entry_raw_unit.get().strip(),
                raw_price1=self._parse_number(self.entry_raw_price1.get() or "0"),
                raw_price2=self._parse_number(self.entry_raw_price2.get() or "0"),
                raw_balance=self._parse_number(self.entry_raw_balance.get() or "0"),
                raw_in=int(self.entry_raw_in.get() or 0),
                raw_out=int(self.entry_raw_out.get() or 0)
            )
            
            if self.db.update_material(material):
                messagebox.showinfo("Éxito", "Material actualizado correctamente")
                self._clear_form()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el material")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
    
    def _delete_material(self):
        """Delete selected material"""
        if not self.current_material:
            messagebox.showwarning("Advertencia", "Seleccione un material de la lista primero")
            return
        
        result = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de eliminar el material '{self.current_material}'?"
        )
        
        if result:
            if self.db.delete_material(self.current_material):
                messagebox.showinfo("Éxito", "Material eliminado correctamente")
                self._clear_form()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el material")
    
    def _load_materials(self):
        """Load all materials into the treeview - No longer used in main view"""
        # Este método ya no se usa porque la lista está en ventana emergente
        pass
    
    def _search_materials(self):
        """Search materials by description - No longer used in main view"""
        # Este método ya no se usa porque la lista está en ventana emergente
        pass
    
    def _on_select(self, event):
        """Handle material selection from list - No longer used in main view"""
        # Este método ya no se usa porque la lista está en ventana emergente
        pass
    
    def _clear_form(self):
        """Clear all form fields"""
        self.current_material = None
        self.current_index = -1
        
        self.entry_raw_part.delete(0, tk.END)
        self.entry_raw_description.delete(0, tk.END)
        self.entry_raw_unit.delete(0, tk.END)
        self.entry_raw_price1.delete(0, tk.END)
        self.entry_raw_price1.insert(0, self._format_number(0))
        self.entry_raw_price2.delete(0, tk.END)
        self.entry_raw_price2.insert(0, self._format_number(0))
        
        # Enable balance field temporarily to clear it
        self.entry_raw_balance.config(state="normal")
        self.entry_raw_balance.delete(0, tk.END)
        self.entry_raw_balance.insert(0, self._format_number(0))
        self.entry_raw_balance.config(state="readonly")
        
        self.entry_raw_in.delete(0, tk.END)
        self.entry_raw_in.insert(0, "0")
        self.entry_raw_out.delete(0, tk.END)
        self.entry_raw_out.insert(0, "0")
        
        self.status_label.config(text="")
        
        # Clear tree selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)
        
        # Focus on Raw.Part field
        self.entry_raw_part.focus()
    
    def _search_by_part(self):
        """Búsqueda automática por Raw.Part"""
        raw_part = self.entry_raw_part.get().strip()
        
        if not raw_part:
            return
        
        # Buscar en la base de datos
        material = self.db.get_material_by_part(raw_part)
        
        if material:
            # Material encontrado - cargar datos
            self.current_material = material.raw_part
            self._populate_form(material)
            self.status_label.config(
                text=f"✓ Material encontrado: {material.raw_description}",
                fg=SUCCESS_COLOR
            )
            # Enfocar en el siguiente campo
            self.entry_raw_description.focus()
        else:
            # Material no existe - preparar para nuevo registro
            self.current_material = None
            self.status_label.config(
                text=f"⚠ Material '{raw_part}' no existe. Complete los datos para crear nuevo registro.",
                fg=WARNING_COLOR
            )
            # Enfocar en descripción para continuar llenando
            self.entry_raw_description.focus()
    
    def _search_by_description(self):
        """Búsqueda por Raw.Description"""
        description = self.entry_raw_description.get().strip()
        
        if not description:
            return
        
        # Buscar en la base de datos
        materials = self.db.search_by_description(description)
        
        if materials:
            if len(materials) == 1:
                # Solo un resultado - cargarlo automáticamente
                material = materials[0]
                self.current_material = material.raw_part
                self._populate_form(material)
                self.status_label.config(
                    text=f"✓ Material encontrado: {material.raw_part}",
                    fg=SUCCESS_COLOR
                )
            else:
                # Múltiples resultados - mostrar en la lista
                self._clear_tree()
                for material in materials:
                    self.tree.insert("", "end", values=(
                        material.raw_part,
                        material.raw_description,
                        material.raw_unit,
                        f"${material.raw_price1:.2f}",
                        f"${material.raw_balance:.2f}"
                    ))
                self.status_label.config(
                    text=f"🔍 Se encontraron {len(materials)} materiales. Seleccione uno de la lista.",
                    fg=INFO_COLOR
                )
        else:
            self.status_label.config(
                text=f"⚠ No se encontraron materiales con la descripción '{description}'",
                fg=WARNING_COLOR
            )
    
    def _navigate_previous(self):
        """Navegar al registro anterior usando las flechas"""
        # Actualizar lista de materiales
        self.all_materials = self.db.get_all_materials()
        
        if not self.all_materials:
            messagebox.showinfo("Info", "No hay materiales en la base de datos")
            return
        
        # Si no hay índice actual, empezar desde el final
        if self.current_index <= 0:
            self.current_index = len(self.all_materials) - 1
        else:
            self.current_index -= 1
        
        # Cargar el material en el índice actual
        material = self.all_materials[self.current_index]
        self.current_material = material.raw_part
        self._populate_form(material)
        self.status_label.config(
            text=f"Registro {self.current_index + 1} de {len(self.all_materials)}",
            fg=INFO_COLOR
        )
    
    def _navigate_next(self):
        """Navegar al siguiente registro usando las flechas"""
        # Actualizar lista de materiales
        self.all_materials = self.db.get_all_materials()
        
        if not self.all_materials:
            messagebox.showinfo("Info", "No hay materiales en la base de datos")
            return
        
        # Si no hay índice actual o llegamos al final, empezar desde el principio
        if self.current_index >= len(self.all_materials) - 1:
            self.current_index = 0
        else:
            self.current_index += 1
        
        # Cargar el material en el índice actual
        material = self.all_materials[self.current_index]
        self.current_material = material.raw_part
        self._populate_form(material)
        self.status_label.config(
            text=f"Registro {self.current_index + 1} de {len(self.all_materials)}",
            fg=INFO_COLOR
        )
    
    def _populate_form(self, material):
        """Poblar el formulario con los datos del material"""
        self.entry_raw_part.delete(0, tk.END)
        self.entry_raw_part.insert(0, material.raw_part)
        
        self.entry_raw_description.delete(0, tk.END)
        self.entry_raw_description.insert(0, material.raw_description)
        
        self.entry_raw_unit.delete(0, tk.END)
        self.entry_raw_unit.insert(0, material.raw_unit)
        
        self.entry_raw_price1.delete(0, tk.END)
        self.entry_raw_price1.insert(0, self._format_number(material.raw_price1))
        
        self.entry_raw_price2.delete(0, tk.END)
        self.entry_raw_price2.insert(0, self._format_number(material.raw_price2))
        
        # Enable balance field temporarily to update it
        self.entry_raw_balance.config(state="normal")
        self.entry_raw_balance.delete(0, tk.END)
        self.entry_raw_balance.insert(0, self._format_number(material.raw_balance))
        self.entry_raw_balance.config(state="readonly")
        
        self.entry_raw_in.delete(0, tk.END)
        self.entry_raw_in.insert(0, str(material.raw_in))
        
        self.entry_raw_out.delete(0, tk.END)
        self.entry_raw_out.insert(0, str(material.raw_out))
    
    def _clear_tree(self):
        """Limpiar todos los elementos del tree view"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def _open_materials_list(self):
        """Abrir ventana emergente con la lista de materiales"""
        # Crear ventana emergente
        list_window = tk.Toplevel(self.container)
        list_window.title("Lista de Materiales")
        list_window.geometry("700x500")
        list_window.configure(bg=WINDOW_BG_COLOR)
        
        # Header
        header_frame = tk.Frame(list_window, bg=HEADER_BG_COLOR, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="Lista de Materiales",
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
        
        def search_in_popup():
            search_term = search_entry.get().strip()
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)
            
            # Search in database
            if search_term:
                materials = self.db.search_by_description(search_term)
            else:
                materials = self.db.get_all_materials()
            
            for material in materials:
                tree.insert("", "end", values=(
                    material.raw_part,
                    material.raw_description,
                    material.raw_unit,
                    f"${material.raw_price1:.2f}",
                    f"${material.raw_balance:.2f}"
                ))
        
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
        
        # Tree frame
        tree_frame = tk.Frame(list_window, bg=FRAME_BG_COLOR)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        tree = ttk.Treeview(
            tree_frame,
            columns=("Part", "Description", "Unit", "Price", "Balance"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )
        
        # Configure scrollbars
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        
        # Define columns
        tree.heading("Part", text="Raw.Part")
        tree.heading("Description", text="Description")
        tree.heading("Unit", text="Unit")
        tree.heading("Price", text="Price 1")
        tree.heading("Balance", text="Balance")
        
        tree.column("Part", width=100)
        tree.column("Description", width=250)
        tree.column("Unit", width=80)
        tree.column("Price", width=100)
        tree.column("Balance", width=100)
        
        # Grid layout
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind selection to load material in main form
        def on_select_popup(event):
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                values = item['values']
                
                raw_part = values[0]
                material = self.db.get_material_by_part(raw_part)
                
                if material:
                    self.current_material = material.raw_part
                    self._populate_form(material)
                    self.status_label.config(
                        text=f"✓ Material cargado: {material.raw_description}",
                        fg=SUCCESS_COLOR
                    )
                    # Cerrar ventana emergente después de seleccionar
                    list_window.destroy()
        
        tree.bind('<<TreeviewSelect>>', on_select_popup)
        
        # Load all materials
        materials = self.db.get_all_materials()
        for material in materials:
            tree.insert("", "end", values=(
                material.raw_part,
                material.raw_description,
                material.raw_unit,
                f"${material.raw_price1:.2f}",
                f"${material.raw_balance:.2f}"
            ))
        
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
        
        # Focus on search entry
        search_entry.focus()


