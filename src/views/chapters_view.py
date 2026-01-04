"""
Chapters Management View
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.views.base_view import BaseView
from src.database.chapter_db import ChapterDB
from src.models.chapter import Chapter
from config.settings import *


class ChaptersView(BaseView):
    """View for managing chapters"""
    
    def __init__(self, container, app_controller):
        super().__init__(container, app_controller)
        self.db = ChapterDB()
        
        # Form variables
        self.chap_number_var = tk.StringVar()
        self.chap_description_var = tk.StringVar()
        
        # Current mode: 'new', 'update', or 'view'
        self.current_mode = 'new'
    
    def render(self):
        """Render the chapters view"""
        self.clear_container()
        
        # Header
        from src.components.ui_components import UIComponents
        UIComponents.create_header(self.container, "Chapters Management")
        
        # Main content frame
        content_frame = tk.Frame(self.container, bg=FRAME_BG_COLOR, relief="ridge", borderwidth=2)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            content_frame,
            text="Chapter Information",
            font=FONTS["title"],
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR
        )
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        form_frame.pack(pady=10, padx=40, fill="x")
        
        # Chapter Number field (read-only for auto-assignment)
        self.chap_number_entry = self._create_field(form_frame, "Chapter Number:", self.chap_number_var, 0, width=6, state="readonly")
        
        # Chapter Description field
        self.chap_description_entry = self._create_field(form_frame, "Description:", self.chap_description_var, 1, width=50)
        
        # Buttons frame
        buttons_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        buttons_frame.pack(pady=20)
        
        # Nuevo button
        btn_new = tk.Button(
            buttons_frame,
            text="Nuevo",
            command=self._save_new,
            font=FONTS["button"],
            bg=SUCCESS_COLOR,
            fg="white",
            activebackground="#229954",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            width=10
        )
        btn_new.pack(side="left", padx=5)
        
        # Actualizar button
        btn_update = tk.Button(
            buttons_frame,
            text="Actualizar",
            command=self._update_record,
            font=FONTS["button"],
            bg=WARNING_COLOR,
            fg="white",
            activebackground="#E67E22",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            width=10
        )
        btn_update.pack(side="left", padx=5)
        
        # Eliminar button
        btn_delete = tk.Button(
            buttons_frame,
            text="Eliminar",
            command=self._delete_record,
            font=FONTS["button"],
            bg=DANGER_COLOR,
            fg="white",
            activebackground="#C0392B",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            width=10
        )
        btn_delete.pack(side="left", padx=5)
        
        # List frame
        list_frame = tk.Frame(content_frame, bg=FRAME_BG_COLOR)
        list_frame.pack(fill="both", expand=True, pady=10, padx=40)
        
        # Treeview for displaying chapters
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollbars
        vsb = ttk.Scrollbar(list_frame, orient="vertical")
        hsb = ttk.Scrollbar(list_frame, orient="horizontal")
        
        # Treeview
        columns = ("Number", "Description")
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=10
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading("Number", text="Chapter Number")
        self.tree.heading("Description", text="Description")
        
        self.tree.column("Number", width=150, anchor="center")
        self.tree.column("Description", width=500, anchor="w")
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Bind double-click to load record
        self.tree.bind("<Double-Button-1>", self._on_tree_select)
        
        # Footer with back button
        footer_frame = tk.Frame(self.container, bg=WINDOW_BG_COLOR)
        footer_frame.pack(fill="x", padx=20, pady=20)
        
        btn_back = tk.Button(
            footer_frame,
            text="← Back",
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
        
        # Initialize form for new record
        self._prepare_new_form()
        
        # Load all chapters
        self._refresh_list()
    
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
        
        if row == 1:
            entry.focus()
        
        return entry
    
    def _prepare_new_form(self):
        """Prepare form for new record (auto-assign number)"""
        self.current_mode = 'new'
        self._clear_form()
        
        # Auto-assign next chapter number
        chapters = self.db.get_all()
        
        if chapters:
            # Find the highest numeric chapter number
            max_number = 0
            for chapter in chapters:
                try:
                    num = int(chapter.chap_number)
                    if num > max_number:
                        max_number = num
                except ValueError:
                    pass
            next_number = max_number + 1
        else:
            next_number = 1
        
        # Set the next number with zero padding
        self.chap_number_var.set(str(next_number).zfill(4))
    
    def _save_new(self):
        """Save new chapter"""
        chap_number = self.chap_number_var.get().strip()
        chap_description = self.chap_description_var.get().strip()
        
        if not chap_number or not chap_description:
            messagebox.showwarning("Validación", "Todos los campos son obligatorios")
            return
        
        # Create chapter
        chapter = Chapter(
            chap_number=chap_number,
            chap_description=chap_description
        )
        
        # Save to database
        if self.db.create(chapter):
            messagebox.showinfo("Éxito", f"Capítulo {chap_number} creado correctamente")
            self._refresh_list()
            self._prepare_new_form()
        else:
            messagebox.showerror("Error", f"El capítulo {chap_number} ya existe")
    
    def _update_record(self):
        """Update existing record"""
        chap_number = self.chap_number_var.get().strip()
        chap_description = self.chap_description_var.get().strip()
        
        if not chap_number:
            messagebox.showwarning("Validación", "Primero busque un registro para actualizar")
            return
        
        if not chap_description:
            messagebox.showwarning("Validación", "La descripción es obligatoria")
            return
        
        # Check if chapter exists
        existing = self.db.get_by_number(chap_number)
        if not existing:
            messagebox.showerror("Error", f"El capítulo {chap_number} no existe")
            return
        
        # Create updated chapter
        chapter = Chapter(
            chap_number=chap_number,
            chap_description=chap_description
        )
        
        # Update in database
        if self.db.update(chapter):
            messagebox.showinfo("Éxito", f"Capítulo {chap_number} actualizado correctamente")
            self._refresh_list()
            self._prepare_new_form()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el capítulo")
    
    def _delete_record(self):
        """Delete selected chapter"""
        chap_number = self.chap_number_var.get().strip()
        
        if not chap_number:
            messagebox.showwarning("Validación", "Primero seleccione un capítulo para eliminar")
            return
        
        # Check if chapter exists
        existing = self.db.get_by_number(chap_number)
        if not existing:
            messagebox.showerror("Error", f"El capítulo {chap_number} no existe")
            return
        
        # Confirm deletion
        response = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar el capítulo {chap_number}?\n\n"
            f"Descripción: {existing.chap_description}\n\n"
            "Esta acción no se puede deshacer."
        )
        
        if not response:
            return
        
        # Delete from database
        if self.db.delete(chap_number):
            messagebox.showinfo("Éxito", f"Capítulo {chap_number} eliminado correctamente")
            self._refresh_list()
            self._prepare_new_form()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el capítulo")
    
    def _search_record(self):
        """Search and load record"""
        # Create search popup
        search_window = tk.Toplevel(self.container)
        search_window.title("Buscar Capítulo")
        search_window.geometry("400x150")
        search_window.configure(bg=FRAME_BG_COLOR)
        search_window.transient(self.container)
        search_window.grab_set()
        
        # Search label
        label = tk.Label(
            search_window,
            text="Ingrese número de capítulo:",
            font=FONTS["text"],
            bg=FRAME_BG_COLOR,
            fg=TEXT_COLOR
        )
        label.pack(pady=20)
        
        # Search entry
        search_var = tk.StringVar()
        entry = tk.Entry(
            search_window,
            textvariable=search_var,
            font=FONTS["text"],
            width=20
        )
        entry.pack(pady=10)
        entry.focus()
        
        def do_search():
            search_term = search_var.get().strip()
            if not search_term:
                messagebox.showwarning("Validación", "Ingrese un número de capítulo")
                return
            
            # Normalize to 4 characters
            if search_term.isdigit():
                search_term = search_term.zfill(4)
            
            chapter = self.db.get_by_number(search_term)
            
            if chapter:
                self.chap_number_var.set(chapter.chap_number)
                self.chap_description_var.set(chapter.chap_description)
                self.current_mode = 'update'
                search_window.destroy()
                messagebox.showinfo("Encontrado", f"Capítulo {chapter.chap_number} cargado")
            else:
                messagebox.showwarning("No encontrado", f"No existe el capítulo {search_term}")
        
        # Search button
        btn_search = tk.Button(
            search_window,
            text="Buscar",
            command=do_search,
            font=FONTS["button"],
            bg=INFO_COLOR,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=10
        )
        btn_search.pack(pady=10)
        
        # Bind Enter key
        entry.bind("<Return>", lambda e: do_search())
    
    def _clear_form(self):
        """Clear all form fields"""
        self.chap_number_var.set("")
        self.chap_description_var.set("")
        self.current_mode = 'new'
    
    def _refresh_list(self):
        """Refresh the chapters list"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load all chapters
        chapters = self.db.get_all()
        
        for chapter in chapters:
            self.tree.insert("", "end", values=(
                chapter.chap_number,
                chapter.chap_description
            ))
    
    def _on_tree_select(self, event):
        """Handle double-click on tree item"""
        print("DEBUG: Double-click detected")  # Debug
        selection = self.tree.selection()
        print(f"DEBUG: Selection = {selection}")  # Debug
        
        if not selection:
            print("DEBUG: No selection")  # Debug
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        print(f"DEBUG: Values = {values}")  # Debug
        
        if values:
            chap_number = values[0]
            print(f"DEBUG: Raw chapter number = {chap_number} (type: {type(chap_number)})")  # Debug
            
            # Normalize to 4-digit string
            chap_number = str(chap_number).zfill(4)
            print(f"DEBUG: Normalized chapter number = {chap_number}")  # Debug
            
            chapter = self.db.get_by_number(chap_number)
            print(f"DEBUG: Found chapter = {chapter}")  # Debug
            
            if chapter:
                print(f"DEBUG: Setting fields - Number: {chapter.chap_number}, Desc: {chapter.chap_description}")  # Debug
                
                # Enable the readonly field temporarily to update it
                self.chap_number_entry.config(state="normal")
                self.chap_number_var.set(chapter.chap_number)
                self.chap_number_entry.config(state="readonly")
                
                # Update description
                self.chap_description_var.set(chapter.chap_description)
                self.current_mode = 'update'
                
                print(f"DEBUG: Fields set. Number var = {self.chap_number_var.get()}, Desc var = {self.chap_description_var.get()}")  # Debug
                
                # Focus on description field for editing
                self.chap_description_entry.focus()


