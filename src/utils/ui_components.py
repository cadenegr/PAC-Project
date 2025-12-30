"""
UI Utilities - Componentes reutilizables para mejorar la interfaz
"""

import tkinter as tk
from config.settings import COLORS, FONTS


class ModernEntry(tk.Entry):
    """Entry mejorado con estilo moderno"""
    
    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(parent, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = COLORS["text_light"]
        self.default_fg_color = COLORS["text_dark"]
        
        # Aplicar estilo
        self.configure(
            font=FONTS["text"],
            bg=COLORS["input_bg"],
            fg=self.default_fg_color,
            relief="solid",
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS["input_border"],
            highlightcolor=COLORS["secondary"]
        )
        
        # Placeholder
        if placeholder:
            self.insert(0, placeholder)
            self.configure(fg=self.placeholder_color)
            self.bind("<FocusIn>", self._on_focus_in)
            self.bind("<FocusOut>", self._on_focus_out)
    
    def _on_focus_in(self, event):
        """Quitar placeholder al hacer focus"""
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.configure(fg=self.default_fg_color)
    
    def _on_focus_out(self, event):
        """Mostrar placeholder si está vacío"""
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(fg=self.placeholder_color)
    
    def get_value(self):
        """Obtener valor real (sin placeholder)"""
        value = self.get()
        return "" if value == self.placeholder else value


class ModernLabel(tk.Label):
    """Label mejorado con estilo moderno"""
    
    def __init__(self, parent, text="", is_header=False, **kwargs):
        super().__init__(parent, text=text, **kwargs)
        
        if is_header:
            self.configure(
                font=FONTS["header"],
                bg=COLORS["background"],
                fg=COLORS["text_dark"],
                anchor="w"
            )
        else:
            self.configure(
                font=FONTS["label"],
                bg=COLORS["background"],
                fg=COLORS["text_dark"],
                anchor="w"
            )


class ModernFrame(tk.Frame):
    """Frame mejorado con estilo de tarjeta"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg=COLORS["card_bg"],
            relief="solid",
            borderwidth=1,
            highlightbackground=COLORS["input_border"],
            highlightthickness=1
        )


class ScrollableFrame(tk.Frame):
    """Frame con scroll para formularios largos"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Canvas y scrollbar
        self.canvas = tk.Canvas(self, bg=COLORS["background"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS["background"])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Habilitar scroll con rueda del mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        """Scroll con rueda del mouse"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


def create_form_field(parent, label_text, row, entry_width=30, placeholder=""):
    """
    Crear un campo de formulario con label y entry
    
    Args:
        parent: Widget padre
        label_text: Texto del label
        row: Fila en el grid
        entry_width: Ancho del entry
        placeholder: Texto placeholder
    
    Returns:
        ModernEntry widget
    """
    # Label
    label = ModernLabel(parent, text=label_text)
    label.grid(row=row, column=0, sticky="w", padx=10, pady=8)
    
    # Entry
    entry = ModernEntry(parent, placeholder=placeholder, width=entry_width)
    entry.grid(row=row, column=1, sticky="ew", padx=10, pady=8)
    
    return entry


def show_message(parent, title, message, message_type="info"):
    """
    Mostrar mensaje en un dialog simple
    
    Args:
        parent: Widget padre
        title: Título del mensaje
        message: Contenido del mensaje
        message_type: Tipo (info, success, warning, error)
    """
    from tkinter import messagebox
    
    if message_type == "info":
        messagebox.showinfo(title, message)
    elif message_type == "success":
        messagebox.showinfo(title, message)
    elif message_type == "warning":
        messagebox.showwarning(title, message)
    elif message_type == "error":
        messagebox.showerror(title, message)


def validate_entry(entry_widget, is_valid):
    """
    Validar visualmente un entry
    
    Args:
        entry_widget: Widget Entry
        is_valid: True si es válido, False si no
    """
    if is_valid:
        entry_widget.configure(highlightbackground=COLORS["success"])
    else:
        entry_widget.configure(highlightbackground=COLORS["danger"])
