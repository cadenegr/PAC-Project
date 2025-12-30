"""
UI Components - Reusable UI elements for all views
Buttons, labels, entries, and navigation controls
"""

import tkinter as tk
from config.settings import *


class UIComponents:
    """Factory class for creating standardized UI components"""
    
    @staticmethod
    def create_header(parent, title_text):
        """Create standard header frame with title"""
        header_frame = tk.Frame(parent, bg=HEADER_BG_COLOR, height=60)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text=title_text,
            font=("Segoe UI", 18, "bold"),
            bg=HEADER_BG_COLOR,
            fg=HEADER_TEXT_COLOR
        )
        title.pack(pady=15)
        
        return header_frame
    
    @staticmethod
    def create_footer_back_button(parent, command):
        """Create footer with back button"""
        footer_frame = tk.Frame(parent, bg=WINDOW_BG_COLOR)
        footer_frame.pack(fill="x", padx=10, pady=10)
        
        btn_back = tk.Button(
            footer_frame,
            text="← Regresar al Catálogo",
            command=command,
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
        
        return footer_frame
    
    @staticmethod
    def create_navigation_buttons(parent, prev_command, search_command, next_command):
        """Create navigation frame with ▲ 🔍 ▼ buttons"""
        nav_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        nav_frame.pack(pady=5)
        
        btn_prev = tk.Button(
            nav_frame,
            text="▲",
            command=prev_command,
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
            command=search_command,
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
            command=next_command,
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
        
        return nav_frame
    
    @staticmethod
    def create_crud_buttons(parent, save_cmd, update_cmd, delete_cmd, clear_cmd):
        """Create CRUD operation buttons (Save, Update, Delete, Clear)"""
        button_frame = tk.Frame(parent, bg=FRAME_BG_COLOR)
        button_frame.pack(pady=20, padx=20, fill="x")
        
        btn_save = tk.Button(
            button_frame,
            text="💾 Guardar",
            command=save_cmd,
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
            command=update_cmd,
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
            command=delete_cmd,
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
            command=clear_cmd,
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
        
        return button_frame
    
    @staticmethod
    def create_status_label(parent):
        """Create status label for showing messages"""
        status_label = tk.Label(
            parent,
            text="",
            font=("Segoe UI", 9),
            bg=FRAME_BG_COLOR,
            fg=INFO_COLOR
        )
        status_label.pack(pady=5)
        return status_label
    
    @staticmethod
    def create_form_label(parent, label_text, row):
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
        return label
    
    @staticmethod
    def create_entry(parent, row, default="", width=None, maxlength=None):
        """Create a form entry field with optional width and max length validation"""
        entry = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            width=width if width else 0
        )
        entry.insert(0, default)
        
        if maxlength:
            validate_cmd = (entry.register(lambda text: len(text) <= maxlength), '%P')
            entry.config(validate="key", validatecommand=validate_cmd)
        
        if width:
            entry.grid(row=row, column=1, pady=8, padx=(0, 10))
        else:
            entry.grid(row=row, column=1, pady=8, sticky="ew", padx=(0, 10))
        
        return entry
    
    @staticmethod
    def create_numeric_entry(parent, row, width=None, maxlength=None, decimals=2):
        """Create numeric entry with formatting (1,234.56)"""
        entry = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            relief="solid",
            borderwidth=1,
            width=width if width else 0
        )
        
        def format_number(event):
            """Format number with commas on focus out"""
            value = entry.get().replace(',', '').strip()
            if value:
                try:
                    num = float(value)
                    formatted = f"{num:,.{decimals}f}"
                    entry.delete(0, tk.END)
                    entry.insert(0, formatted)
                except ValueError:
                    pass
        
        def unformat_number(event):
            """Remove commas on focus in for editing"""
            value = entry.get().replace(',', '').strip()
            entry.delete(0, tk.END)
            entry.insert(0, value)
        
        def validate_numeric(text):
            """Allow only numeric input with optional decimal point"""
            if text == "":
                return True
            text_clean = text.replace(',', '')
            try:
                if '.' in text_clean:
                    parts = text_clean.split('.')
                    if len(parts) == 2 and len(parts[1]) <= decimals:
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
    
    @staticmethod
    def create_search_button(parent, command):
        """Create small search button (🔍)"""
        btn_search = tk.Button(
            parent,
            text="🔍",
            command=command,
            font=("Segoe UI", 10),
            bg=INFO_COLOR,
            fg="white",
            activebackground="#138D75",
            relief="flat",
            cursor="hand2",
            width=3
        )
        return btn_search
