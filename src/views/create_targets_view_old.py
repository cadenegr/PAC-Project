"""
Create Targets View
Special form with validation against Chapters and Products databases
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.views.base_view import BaseView
from src.database.target_db import TargetDatabase
from src.database.chapter_db import ChapterDatabase
from src.database.product_db import ProductDatabase
from src.models.target import Target
from src.components.ui_components import UIComponents
from config.settings import *


class CreateTargetsView(BaseView):
    """Create Targets view with cross-database validation"""
    
    def __init__(self, container, app_controller):
        super().__init__(container, app_controller)
        self.target_db = TargetDatabase()
        self.chapter_db = ChapterDatabase()
        self.product_db = ProductDatabase()
        
        self.current_chapter = None
        self.current_product = None
        self.current_target = None
        self.all_targets = []
        self.current_index = -1
    
    def render(self):
        """Render the create targets view"""
        self.clear_container()
        
        # Header
        UIComponents.create_header(self.container, "Create Targets")
        
        # Main content area
        content_frame = tk.Frame(self.container, bg=WINDOW_BG_COLOR)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Form panel
        form_panel = tk.Frame(content_frame, bg=FRAME_BG_COLOR, relief="ridge", borderwidth=2)
        form_panel.pack(fill="both", expand=True)
        
        self._create_form(form_panel)
        
        # Footer with back button
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
    
    def _create_form(self, parent):
        """Create the target entry form with validations"""
        form_title = tk.Label(
            parent,
            text="Datos del Target",
            font=("Segoe UI", 14, "bold"),
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR
        )
        form_title.pack(pady=15)
        
        # Navigation buttons
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
        
        btn_search_list = tk.Button(
            nav_frame,
            text="🔍 Search",
            command=self._open_targets_list,
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
        
        # Form fields
        fields_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        fields_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Chapter Number (validates against Chapters DB)
        self._create_label(fields_frame, "Chapter Number *:", 0)
        
        chap_frame = tk.Frame(fields_frame, bg=FRAME_BG_COLOR)
        chap_frame.grid(row=0, column=1, pady=8, sticky="ew", padx=(0, 10))
        
        self.entry_chap_number = tk.Entry(
            chap_frame,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            width=5
        )
        self.entry_chap_number.pack(side="left", padx=(0, 5))
        
        vcmd = (self.entry_chap_number.register(lambda text: len(text) <= 3 and (text.isdigit() or text == "")), '%P')
        self.entry_chap_number.config(validate="key", validatecommand=vcmd)
        
        self.entry_chap_number.bind("<Return>", lambda e: self._validate_chapter())
        self.entry_chap_number.bind("<FocusOut>", lambda e: self._validate_chapter())
        
        btn_validate_chap = tk.Button(
            chap_frame,
            text="✓",
            command=self._validate_chapter,
            font=("Segoe UI", 10),
            bg=SUCCESS_COLOR,
            fg="white",
            activebackground="#229954",
            relief="flat",
            cursor="hand2",
            width=3
        )
        btn_validate_chap.pack(side="left")
        
        # Chapter Description (read-only, from DB)
        self._create_label(fields_frame, "Chapter Description:", 1)
        self.entry_chap_desc = self._create_entry(fields_frame, 1, width=30, readonly=True)
        
        # Product Number (validates against Products DB)
        self._create_label(fields_frame, "Product Number *:", 2)
        
        prod_frame = tk.Frame(fields_frame, bg=FRAME_BG_COLOR)
        prod_frame.grid(row=2, column=1, pady=8, sticky="ew", padx=(0, 10))
        
        self.entry_pro_number = tk.Entry(
            prod_frame,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            width=12
        )
        self.entry_pro_number.pack(side="left", padx=(0, 5))
        
        vcmd_pro = (self.entry_pro_number.register(lambda text: len(text) <= 12), '%P')
        self.entry_pro_number.config(validate="key", validatecommand=vcmd_pro)
        
        self.entry_pro_number.bind("<Return>", lambda e: self._validate_product())
        self.entry_pro_number.bind("<FocusOut>", lambda e: self._validate_product())
        
        btn_validate_prod = tk.Button(
            prod_frame,
            text="✓",
            command=self._validate_product,
            font=("Segoe UI", 10),
            bg=SUCCESS_COLOR,
            fg="white",
            activebackground="#229954",
            relief="flat",
            cursor="hand2",
            width=3
        )
        btn_validate_prod.pack(side="left")
        
        # Product Description (read-only, from DB)
        self._create_label(fields_frame, "Product Description:", 3)
        self.entry_pro_desc = self._create_entry(fields_frame, 3, width=30, readonly=True)
        
        # Product Unit (read-only, from DB)
        self._create_label(fields_frame, "Unit:", 4)
        self.entry_pro_unit = self._create_entry(fields_frame, 4, width=4, readonly=True)
        
        # Price (numeric)
        self._create_label(fields_frame, "Price:", 5)
        self.entry_price = self._create_numeric_entry(fields_frame, 5, width=15, maxlength=12)
        
        # Quantities (numeric)
        self._create_label(fields_frame, "Qty Project:", 6)
        self.entry_qty_project = self._create_numeric_entry(fields_frame, 6, width=15, maxlength=12)
        
        self._create_label(fields_frame, "Qty Done:", 7)
        self.entry_qty_done = self._create_numeric_entry(fields_frame, 7, width=15, maxlength=12)
        
        self._create_label(fields_frame, "Qty Progress:", 8)
        self.entry_qty_progress = self._create_numeric_entry(fields_frame, 8, width=15, maxlength=12)
        
        self._create_label(fields_frame, "Qty Finish:", 9)
        self.entry_qty_finish = self._create_numeric_entry(fields_frame, 9, width=15, maxlength=12)
        
        self._create_label(fields_frame, "Payment:", 10)
        self.entry_payment = self._create_numeric_entry(fields_frame, 10, width=15, maxlength=12)
        
        fields_frame.columnconfigure(1, weight=1)
        
        # Status label
        self.status_label = tk.Label(
            parent,
            text="",
            font=("Segoe UI", 9),
            bg=FRAME_BG_COLOR,
            fg=INFO_COLOR
        )
        self.status_label.pack(pady=5)
        
        # CRUD Buttons
        button_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        button_frame.pack(pady=20, padx=20, fill="x")
        
        btn_save = tk.Button(
            button_frame,
            text="💾 Guardar",
            command=self._save_target,
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
            command=self._update_target,
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
            command=self._delete_target,
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
    
    def _create_label(self, parent, text, row):
        """Create form label"""
        label = tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 10),
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR,
            anchor="w"
        )
        label.grid(row=row, column=0, pady=8, sticky="w", padx=10)
        return label
    
    def _create_entry(self, parent, row, width=None, readonly=False):
        """Create entry field"""
        entry = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            width=width if width else 0,
            state='readonly' if readonly else 'normal',
            readonlybackground='#F0F0F0' if readonly else 'white'
        )
        if width:
            entry.grid(row=row, column=1, pady=8, padx=(0, 10))
        else:
            entry.grid(row=row, column=1, pady=8, sticky="ew", padx=(0, 10))
        return entry
    
    def _create_numeric_entry(self, parent, row, width=None, maxlength=None):
        """Create numeric entry with formatting"""
        entry = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            width=width if width else 0
        )
        
        def format_number(event):
            value = entry.get().replace(',', '').strip()
            if value:
                try:
                    num = float(value)
                    formatted = f"{num:,.2f}"
                    entry.delete(0, tk.END)
                    entry.insert(0, formatted)
                except ValueError:
                    pass
        
        def unformat_number(event):
            value = entry.get().replace(',', '').strip()
            entry.delete(0, tk.END)
            entry.insert(0, value)
        
        def validate_numeric(text):
            if text == "":
                return True
            text_clean = text.replace(',', '')
            try:
                if '.' in text_clean:
                    parts = text_clean.split('.')
                    if len(parts) == 2 and len(parts[1]) <= 2:
                        float(text_clean)
                        return True
                    return False
                else:
                    float(text_clean)
                    return True
            except ValueError:
                return False
        
        validate_cmd = (entry.register(validate_numeric), '%P')
        entry.config(validate="key", validatecommand=validate_cmd)
        
        if maxlength:
            length_cmd = (entry.register(lambda text: len(text.replace(',', '')) <= maxlength), '%P')
            entry.config(validate="key", validatecommand=length_cmd)
        
        entry.bind("<FocusOut>", format_number)
        entry.bind("<FocusIn>", unformat_number)
        
        if width:
            entry.grid(row=row, column=1, pady=8, padx=(0, 10))
        else:
            entry.grid(row=row, column=1, pady=8, sticky="ew", padx=(0, 10))
        
        return entry
    
    def _validate_chapter(self):
        """Validate chapter number against Chapters database"""
        chap_number = self.entry_chap_number.get().strip()
        
        if not chap_number:
            return
        
        try:
            chap_num = int(chap_number)
            chapter = self.chapter_db.get_chapter_by_number(chap_num)
            
            if chapter:
                self.current_chapter = chapter
                # Update description field
                self.entry_chap_desc.config(state='normal')
                self.entry_chap_desc.delete(0, tk.END)
                self.entry_chap_desc.insert(0, chapter.chap_description)
                self.entry_chap_desc.config(state='readonly')
                
                self.status_label.config(
                    text=f"✓ Chapter encontrado: {chapter.chap_description}",
                    fg=SUCCESS_COLOR
                )
                # Move to next field
                self.entry_pro_number.focus()
            else:
                self.current_chapter = None
                self.entry_chap_desc.config(state='normal')
                self.entry_chap_desc.delete(0, tk.END)
                self.entry_chap_desc.config(state='readonly')
                
                messagebox.showerror(
                    "Chapter No Existe",
                    f"El Chapter número '{chap_number}' no existe en la base de datos.\n\n"
                    "Por favor ingrese un número de chapter válido."
                )
                self.status_label.config(
                    text=f"⚠ Chapter '{chap_number}' no encontrado",
                    fg=DANGER_COLOR
                )
                self.entry_chap_number.focus()
                self.entry_chap_number.select_range(0, tk.END)
                
        except ValueError:
            messagebox.showerror("Error", "El Chapter Number debe ser un número válido")
            self.entry_chap_number.focus()
    
    def _validate_product(self):
        """Validate product number against Products database"""
        if not self.current_chapter:
            messagebox.showwarning(
                "Advertencia",
                "Primero debe validar un Chapter Number antes de ingresar el Product Number"
            )
            self.entry_chap_number.focus()
            return
        
        pro_number = self.entry_pro_number.get().strip()
        
        if not pro_number:
            return
        
        product = self.product_db.get_product_by_part(pro_number)
        
        if product:
            self.current_product = product
            # Update fields
            self.entry_pro_desc.config(state='normal')
            self.entry_pro_desc.delete(0, tk.END)
            self.entry_pro_desc.insert(0, product.pro_description)
            self.entry_pro_desc.config(state='readonly')
            
            self.entry_pro_unit.config(state='normal')
            self.entry_pro_unit.delete(0, tk.END)
            self.entry_pro_unit.insert(0, product.pro_unit)
            self.entry_pro_unit.config(state='readonly')
            
            self.status_label.config(
                text=f"✓ Producto encontrado: {product.pro_description}",
                fg=SUCCESS_COLOR
            )
            # Move to price field
            self.entry_price.focus()
        else:
            self.current_product = None
            self.entry_pro_desc.config(state='normal')
            self.entry_pro_desc.delete(0, tk.END)
            self.entry_pro_desc.config(state='readonly')
            
            self.entry_pro_unit.config(state='normal')
            self.entry_pro_unit.delete(0, tk.END)
            self.entry_pro_unit.config(state='readonly')
            
            messagebox.showerror(
                "Producto No Existe",
                f"El producto '{pro_number}' no existe en la base de datos.\n\n"
                "Por favor ingrese un número de producto válido."
            )
            self.status_label.config(
                text=f"⚠ Producto '{pro_number}' no encontrado",
                fg=DANGER_COLOR
            )
            self.entry_pro_number.focus()
            self.entry_pro_number.select_range(0, tk.END)
    
    def _save_target(self):
        """Save new target"""
        if not self.current_chapter:
            messagebox.showerror("Error", "Debe validar un Chapter Number primero")
            self.entry_chap_number.focus()
            return
        
        if not self.current_product:
            messagebox.showerror("Error", "Debe validar un Product Number primero")
            self.entry_pro_number.focus()
            return
        
        try:
            target = Target(
                targ_prochapter=self.entry_chap_number.get().strip(),
                targ_pronumber=self.entry_pro_number.get().strip(),
                targ_prodescription=self.entry_pro_desc.get().strip(),
                targ_prounit=self.entry_pro_unit.get().strip(),
                targ_proprice1=float(self.entry_price.get().replace(',', '') or 0),
                targ_qtyproject=float(self.entry_qty_project.get().replace(',', '') or 0),
                targ_qtydone=float(self.entry_qty_done.get().replace(',', '') or 0),
                targ_qtyprogress=float(self.entry_qty_progress.get().replace(',', '') or 0),
                targ_qtyfinish=float(self.entry_qty_finish.get().replace(',', '') or 0),
                targ_payment=float(self.entry_payment.get().replace(',', '') or 0)
            )
            
            target_id = self.target_db.create_target(target)
            
            if target_id:
                messagebox.showinfo("Éxito", "Target guardado correctamente")
                self._clear_form()
            else:
                messagebox.showerror("Error", "El Target ProNumber ya existe en la base de datos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def _update_target(self):
        """Update existing target"""
        if not self.current_target:
            messagebox.showwarning("Advertencia", "Seleccione un target de la lista primero")
            return
        
        try:
            target = Target(
                targ_prochapter=self.entry_chap_number.get().strip(),
                targ_pronumber=self.entry_pro_number.get().strip(),
                targ_prodescription=self.entry_pro_desc.get().strip(),
                targ_prounit=self.entry_pro_unit.get().strip(),
                targ_proprice1=float(self.entry_price.get().replace(',', '') or 0),
                targ_qtyproject=float(self.entry_qty_project.get().replace(',', '') or 0),
                targ_qtydone=float(self.entry_qty_done.get().replace(',', '') or 0),
                targ_qtyprogress=float(self.entry_qty_progress.get().replace(',', '') or 0),
                targ_qtyfinish=float(self.entry_qty_finish.get().replace(',', '') or 0),
                targ_payment=float(self.entry_payment.get().replace(',', '') or 0)
            )
            
            if self.target_db.update_target(target):
                messagebox.showinfo("Éxito", "Target actualizado correctamente")
                self._clear_form()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el target")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
    
    def _delete_target(self):
        """Delete selected target"""
        if not self.current_target:
            messagebox.showwarning("Advertencia", "Seleccione un target de la lista primero")
            return
        
        result = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de eliminar el target '{self.current_target}'?"
        )
        
        if result:
            if self.target_db.delete_target(self.current_target):
                messagebox.showinfo("Éxito", "Target eliminado correctamente")
                self._clear_form()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el target")
    
    def _clear_form(self):
        """Clear all form fields"""
        self.current_chapter = None
        self.current_product = None
        self.current_target = None
        self.current_index = -1
        
        self.entry_chap_number.delete(0, tk.END)
        
        self.entry_chap_desc.config(state='normal')
        self.entry_chap_desc.delete(0, tk.END)
        self.entry_chap_desc.config(state='readonly')
        
        self.entry_pro_number.delete(0, tk.END)
        
        self.entry_pro_desc.config(state='normal')
        self.entry_pro_desc.delete(0, tk.END)
        self.entry_pro_desc.config(state='readonly')
        
        self.entry_pro_unit.config(state='normal')
        self.entry_pro_unit.delete(0, tk.END)
        self.entry_pro_unit.config(state='readonly')
        
        self.entry_price.delete(0, tk.END)
        self.entry_qty_project.delete(0, tk.END)
        self.entry_qty_done.delete(0, tk.END)
        self.entry_qty_progress.delete(0, tk.END)
        self.entry_qty_finish.delete(0, tk.END)
        self.entry_payment.delete(0, tk.END)
        
        self.status_label.config(text="")
        self.entry_chap_number.focus()
    
    def _populate_form(self, target):
        """Populate form with target data"""
        # Set chapter
        self.entry_chap_number.delete(0, tk.END)
        self.entry_chap_number.insert(0, target.targ_prochapter)
        self._validate_chapter()
        
        # Set product
        self.entry_pro_number.delete(0, tk.END)
        self.entry_pro_number.insert(0, target.targ_pronumber)
        self._validate_product()
        
        # Set numeric fields
        self.entry_price.delete(0, tk.END)
        self.entry_price.insert(0, f"{target.targ_proprice1:,.2f}")
        
        self.entry_qty_project.delete(0, tk.END)
        self.entry_qty_project.insert(0, f"{target.targ_qtyproject:,.2f}")
        
        self.entry_qty_done.delete(0, tk.END)
        self.entry_qty_done.insert(0, f"{target.targ_qtydone:,.2f}")
        
        self.entry_qty_progress.delete(0, tk.END)
        self.entry_qty_progress.insert(0, f"{target.targ_qtyprogress:,.2f}")
        
        self.entry_qty_finish.delete(0, tk.END)
        self.entry_qty_finish.insert(0, f"{target.targ_qtyfinish:,.2f}")
        
        self.entry_payment.delete(0, tk.END)
        self.entry_payment.insert(0, f"{target.targ_payment:,.2f}")
        
        self.current_target = target.targ_pronumber
    
    def _navigate_previous(self):
        """Navigate to previous record"""
        self.all_targets = self.target_db.get_all_targets()
        
        if not self.all_targets:
            messagebox.showinfo("Info", "No hay targets en la base de datos")
            return
        
        if self.current_index <= 0:
            self.current_index = len(self.all_targets) - 1
        else:
            self.current_index -= 1
        
        target = self.all_targets[self.current_index]
        self._populate_form(target)
        self.status_label.config(
            text=f"Registro {self.current_index + 1} de {len(self.all_targets)}",
            fg=INFO_COLOR
        )
    
    def _navigate_next(self):
        """Navigate to next record"""
        self.all_targets = self.target_db.get_all_targets()
        
        if not self.all_targets:
            messagebox.showinfo("Info", "No hay targets en la base de datos")
            return
        
        if self.current_index >= len(self.all_targets) - 1:
            self.current_index = 0
        else:
            self.current_index += 1
        
        target = self.all_targets[self.current_index]
        self._populate_form(target)
        self.status_label.config(
            text=f"Registro {self.current_index + 1} de {len(self.all_targets)}",
            fg=INFO_COLOR
        )
    
    def _open_targets_list(self):
        """Open popup window with targets list"""
        list_window = tk.Toplevel(self.container)
        list_window.title("Lista de Targets")
        list_window.geometry("1000x500")
        list_window.configure(bg=WINDOW_BG_COLOR)
        
        # Header
        header_frame = tk.Frame(list_window, bg=HEADER_BG_COLOR, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="Lista de Targets",
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
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("Chapter", "ProNumber", "Description", "Unit", "Price"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )
        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        
        tree.heading("Chapter", text="Chapter")
        tree.heading("ProNumber", text="ProNumber")
        tree.heading("Description", text="Description")
        tree.heading("Unit", text="Unit")
        tree.heading("Price", text="Price")
        
        tree.column("Chapter", width=80)
        tree.column("ProNumber", width=120)
        tree.column("Description", width=300)
        tree.column("Unit", width=80)
        tree.column("Price", width=120)
        
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        def load_targets(search_term=""):
            for item in tree.get_children():
                tree.delete(item)
            
            if search_term:
                targets = self.target_db.search_by_description(search_term)
            else:
                targets = self.target_db.get_all_targets()
            
            for target in targets:
                tree.insert("", "end", values=(
                    target.targ_prochapter,
                    target.targ_pronumber,
                    target.targ_prodescription,
                    target.targ_prounit,
                    f"{target.targ_proprice1:,.2f}"
                ))
        
        def search_in_popup():
            search_term = search_entry.get().strip()
            load_targets(search_term)
        
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
                
                pro_number = values[1]
                target = self.target_db.get_target_by_number(pro_number)
                
                if target:
                    self._populate_form(target)
                    self.status_label.config(
                        text=f"✓ Target cargado",
                        fg=SUCCESS_COLOR
                    )
                    list_window.destroy()
        
        tree.bind('<<TreeviewSelect>>', on_select_popup)
        
        # Load all targets
        load_targets()
        
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
