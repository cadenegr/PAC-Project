"""
Products Management View
Complete CRUD interface for products with auto-search and navigation
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.views.base_view import BaseView
from config.settings import *
from src.database.product_db import ProductDatabase
from src.models.product import Product


class ProductsView(BaseView):
    """Products management view with CRUD operations"""
    
    def __init__(self, container, app_controller):
        super().__init__(container, app_controller)
        self.db = ProductDatabase()
        self.current_product = None
        self.all_products = []  # Lista de todos los productos
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
        """Render the products management view"""
        self.clear_container()
        
        # Header
        header_frame = tk.Frame(self.container, bg=HEADER_BG_COLOR, height=60)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="Products Management",
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
        """Create the product entry form with auto-search and navigation"""
        form_title = tk.Label(
            parent,
            text="Datos del Producto",
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
        
        # Botón de búsqueda para abrir lista de productos
        btn_search_list = tk.Button(
            nav_frame,
            text="🔍 Search",
            command=self._open_products_list,
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
        
        # Pro.Part (Primary Key) - Con búsqueda automática
        self._create_field(fields_frame, "Part Number *:", 0)
        
        # Frame para Pro.Part con botón de búsqueda
        part_frame = tk.Frame(fields_frame, bg=FRAME_BG_COLOR)
        part_frame.grid(row=0, column=1, pady=8, sticky="ew", padx=(0, 10))
        
        self.entry_pro_part = tk.Entry(
            part_frame,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            width=12
        )
        self.entry_pro_part.pack(side="left", padx=(0, 5))
        
        # Validación de longitud máxima
        vcmd = (self.entry_pro_part.register(lambda text: len(text) <= 12), '%P')
        self.entry_pro_part.config(validate="key", validatecommand=vcmd)
        
        # Vincular evento cuando se presiona Enter en Pro.Part
        self.entry_pro_part.bind("<Return>", lambda e: self._search_by_part())
        self.entry_pro_part.bind("<FocusOut>", lambda e: self._search_by_part())
        
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
        
        # Pro.Description (también llave de búsqueda)
        self._create_field(fields_frame, "Description *:", 1)
        self.entry_pro_description = self._create_entry(fields_frame, 1, width=30, maxlength=30)
        self.entry_pro_description.bind("<Return>", lambda e: self._search_by_description())
        
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
        
        # Pro.Unit
        self._create_field(fields_frame, "Unit Measure *:", 2)
        self.entry_pro_unit = self._create_entry(fields_frame, 2, width=4, maxlength=4)
        
        # Pro.Price1
        self._create_field(fields_frame, "Price 1:", 3)
        self.entry_pro_price1 = self._create_entry(fields_frame, 3, self._format_number(0), width=12, maxlength=12)
        
        # Pro.Price2
        self._create_field(fields_frame, "Price 2:", 4)
        self.entry_pro_price2 = self._create_entry(fields_frame, 4, self._format_number(0), width=12, maxlength=12)
        
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
            command=self._save_product,
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
            command=self._update_product,
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
            command=self._delete_product,
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
    
    def _save_product(self):
        """Save new product to database"""
        # Validate required fields
        if not self.entry_pro_part.get() or not self.entry_pro_description.get() or not self.entry_pro_unit.get():
            messagebox.showerror("Error", "Por favor complete los campos obligatorios (*)")
            return
        
        try:
            product = Product(
                pro_part=self.entry_pro_part.get().strip(),
                pro_description=self.entry_pro_description.get().strip(),
                pro_unit=self.entry_pro_unit.get().strip(),
                pro_price1=self._parse_number(self.entry_pro_price1.get() or "0"),
                pro_price2=self._parse_number(self.entry_pro_price2.get() or "0")
            )
            
            product_id = self.db.create_product(product)
            
            if product_id:
                messagebox.showinfo("Éxito", "Producto guardado correctamente")
                self._clear_form()
            else:
                messagebox.showerror("Error", "El Pro.Part ya existe en la base de datos")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
    
    def _update_product(self):
        """Update existing product"""
        if not self.current_product:
            messagebox.showwarning("Advertencia", "Seleccione un producto de la lista primero")
            return
        
        try:
            product = Product(
                pro_part=self.entry_pro_part.get().strip(),
                pro_description=self.entry_pro_description.get().strip(),
                pro_unit=self.entry_pro_unit.get().strip(),
                pro_price1=self._parse_number(self.entry_pro_price1.get() or "0"),
                pro_price2=self._parse_number(self.entry_pro_price2.get() or "0")
            )
            
            if self.db.update_product(product):
                messagebox.showinfo("Éxito", "Producto actualizado correctamente")
                self._clear_form()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el producto")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
    
    def _delete_product(self):
        """Delete selected product"""
        if not self.current_product:
            messagebox.showwarning("Advertencia", "Seleccione un producto de la lista primero")
            return
        
        result = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de eliminar el producto '{self.current_product}'?"
        )
        
        if result:
            if self.db.delete_product(self.current_product):
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self._clear_form()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto")
    
    def _clear_form(self):
        """Clear all form fields"""
        self.current_product = None
        self.current_index = -1
        
        self.entry_pro_part.delete(0, tk.END)
        self.entry_pro_description.delete(0, tk.END)
        self.entry_pro_unit.delete(0, tk.END)
        self.entry_pro_price1.delete(0, tk.END)
        self.entry_pro_price1.insert(0, self._format_number(0))
        self.entry_pro_price2.delete(0, tk.END)
        self.entry_pro_price2.insert(0, self._format_number(0))
        
        self.status_label.config(text="")
        
        # Focus on Pro.Part field
        self.entry_pro_part.focus()
    
    def _search_by_part(self):
        """Búsqueda automática por Pro.Part"""
        pro_part = self.entry_pro_part.get().strip()
        
        if not pro_part:
            return
        
        # Buscar en la base de datos
        product = self.db.get_product_by_part(pro_part)
        
        if product:
            # Producto encontrado - cargar datos
            self.current_product = product.pro_part
            self._populate_form(product)
            self.status_label.config(
                text=f"✓ Producto encontrado: {product.pro_description}",
                fg=SUCCESS_COLOR
            )
            # Enfocar en el siguiente campo
            self.entry_pro_description.focus()
        else:
            # Producto no existe - preparar para nuevo registro
            self.current_product = None
            self.status_label.config(
                text=f"⚠ Producto '{pro_part}' no existe. Complete los datos para crear nuevo registro.",
                fg=WARNING_COLOR
            )
            # Enfocar en descripción para continuar llenando
            self.entry_pro_description.focus()
    
    def _search_by_description(self):
        """Búsqueda por Pro.Description"""
        description = self.entry_pro_description.get().strip()
        
        if not description:
            return
        
        # Buscar en la base de datos
        products = self.db.search_by_description(description)
        
        if products:
            if len(products) == 1:
                # Solo un resultado - cargarlo automáticamente
                product = products[0]
                self.current_product = product.pro_part
                self._populate_form(product)
                self.status_label.config(
                    text=f"✓ Producto encontrado: {product.pro_part}",
                    fg=SUCCESS_COLOR
                )
            else:
                # Múltiples resultados - abrir ventana de búsqueda
                self.status_label.config(
                    text=f"🔍 Se encontraron {len(products)} productos. Presione el botón Search para ver la lista.",
                    fg=INFO_COLOR
                )
        else:
            self.status_label.config(
                text=f"⚠ No se encontraron productos con la descripción '{description}'",
                fg=WARNING_COLOR
            )
    
    def _navigate_previous(self):
        """Navegar al registro anterior usando las flechas"""
        # Actualizar lista de productos
        self.all_products = self.db.get_all_products()
        
        if not self.all_products:
            messagebox.showinfo("Info", "No hay productos en la base de datos")
            return
        
        # Si no hay índice actual, empezar desde el final
        if self.current_index <= 0:
            self.current_index = len(self.all_products) - 1
        else:
            self.current_index -= 1
        
        # Cargar el producto en el índice actual
        product = self.all_products[self.current_index]
        self.current_product = product.pro_part
        self._populate_form(product)
        self.status_label.config(
            text=f"Registro {self.current_index + 1} de {len(self.all_products)}",
            fg=INFO_COLOR
        )
    
    def _navigate_next(self):
        """Navegar al siguiente registro usando las flechas"""
        # Actualizar lista de productos
        self.all_products = self.db.get_all_products()
        
        if not self.all_products:
            messagebox.showinfo("Info", "No hay productos en la base de datos")
            return
        
        # Si no hay índice actual o llegamos al final, empezar desde el principio
        if self.current_index >= len(self.all_products) - 1:
            self.current_index = 0
        else:
            self.current_index += 1
        
        # Cargar el producto en el índice actual
        product = self.all_products[self.current_index]
        self.current_product = product.pro_part
        self._populate_form(product)
        self.status_label.config(
            text=f"Registro {self.current_index + 1} de {len(self.all_products)}",
            fg=INFO_COLOR
        )
    
    def _populate_form(self, product):
        """Poblar el formulario con los datos del producto"""
        self.entry_pro_part.delete(0, tk.END)
        self.entry_pro_part.insert(0, product.pro_part)
        
        self.entry_pro_description.delete(0, tk.END)
        self.entry_pro_description.insert(0, product.pro_description)
        
        self.entry_pro_unit.delete(0, tk.END)
        self.entry_pro_unit.insert(0, product.pro_unit)
        
        self.entry_pro_price1.delete(0, tk.END)
        self.entry_pro_price1.insert(0, self._format_number(product.pro_price1))
        
        self.entry_pro_price2.delete(0, tk.END)
        self.entry_pro_price2.insert(0, self._format_number(product.pro_price2))
    
    def _open_products_list(self):
        """Abrir ventana emergente con la lista de productos"""
        # Crear ventana emergente
        list_window = tk.Toplevel(self.container)
        list_window.title("Lista de Productos")
        list_window.geometry("700x500")
        list_window.configure(bg=WINDOW_BG_COLOR)
        
        # Header
        header_frame = tk.Frame(list_window, bg=HEADER_BG_COLOR, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="Lista de Productos",
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
                products = self.db.search_by_description(search_term)
            else:
                products = self.db.get_all_products()
            
            for product in products:
                tree.insert("", "end", values=(
                    product.pro_part,
                    product.pro_description,
                    product.pro_unit,
                    f"${product.pro_price1:.2f}",
                    f"${product.pro_price2:.2f}"
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
            columns=("Part", "Description", "Unit", "Price1", "Price2"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )
        
        # Configure scrollbars
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        
        # Define columns
        tree.heading("Part", text="Pro.Part")
        tree.heading("Description", text="Description")
        tree.heading("Unit", text="Unit")
        tree.heading("Price1", text="Price 1")
        tree.heading("Price2", text="Price 2")
        
        tree.column("Part", width=100)
        tree.column("Description", width=250)
        tree.column("Unit", width=80)
        tree.column("Price1", width=100)
        tree.column("Price2", width=100)
        
        # Grid layout
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind selection to load product in main form
        def on_select_popup(event):
            selection = tree.selection()
            if selection:
                item = tree.item(selection[0])
                values = item['values']
                
                pro_part = values[0]
                product = self.db.get_product_by_part(pro_part)
                
                if product:
                    self.current_product = product.pro_part
                    self._populate_form(product)
                    self.status_label.config(
                        text=f"✓ Producto cargado: {product.pro_description}",
                        fg=SUCCESS_COLOR
                    )
                    # Cerrar ventana emergente después de seleccionar
                    list_window.destroy()
        
        tree.bind('<<TreeviewSelect>>', on_select_popup)
        
        # Load all products
        products = self.db.get_all_products()
        for product in products:
            tree.insert("", "end", values=(
                product.pro_part,
                product.pro_description,
                product.pro_unit,
                f"${product.pro_price1:.2f}",
                f"${product.pro_price2:.2f}"
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
