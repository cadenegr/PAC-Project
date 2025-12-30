"""
Teams Work Form View - Formulario mejorado para gestionar equipos de trabajo
"""

import tkinter as tk
from src.views.base_view import BaseView
from src.utils.ui_components import (
    ModernEntry, ModernLabel, ModernFrame, 
    ScrollableFrame, create_form_field, show_message, validate_entry
)
from config.settings import COLORS, FONTS, BUTTON_STYLES


class TeamsWorkFormView(BaseView):
    """Vista de formulario para crear/actualizar equipos de trabajo"""
    
    def __init__(self, container, app_controller, mode="new", team_data=None):
        """
        Initialize the teams work form view
        
        Args:
            container: The parent container widget
            app_controller: Reference to the main application controller
            mode: "new" para nuevo equipo, "update" para actualizar
            team_data: Datos del equipo (si es modo update)
        """
        super().__init__(container, app_controller)
        self.mode = mode
        self.team_data = team_data or {}
        self.entries = {}
    
    def render(self):
        """Render the teams work form"""
        self.clear_container()
        
        # Header
        header_frame = tk.Frame(self.container, bg=COLORS["header_bg"], height=60)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_text = "Nuevo Equipo de Trabajo" if self.mode == "new" else "Actualizar Equipo de Trabajo"
        header_label = tk.Label(
            header_frame,
            text=title_text,
            font=FONTS["subtitle"],
            bg=COLORS["header_bg"],
            fg=COLORS["header_text"]
        )
        header_label.pack(expand=True)
        
        # Scrollable form area
        scroll_frame = ScrollableFrame(self.container)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Form card
        form_card = ModernFrame(scroll_frame.scrollable_frame)
        form_card.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configure grid
        form_card.columnconfigure(1, weight=1)
        
        # Form title
        form_title = ModernLabel(
            form_card,
            text="Información del Equipo",
            is_header=True
        )
        form_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 10))
        
        # Form fields
        self.entries["team_number"] = create_form_field(
            form_card, "Número de Equipo *", 1, 
            placeholder="Ej: 001"
        )
        
        self.entries["team_name"] = create_form_field(
            form_card, "Nombre del Equipo *", 2,
            placeholder="Ej: Equipo Alpha"
        )
        
        # Separator
        separator1 = tk.Frame(form_card, height=1, bg=COLORS["input_border"])
        separator1.grid(row=3, column=0, columnspan=2, sticky="ew", padx=15, pady=15)
        
        # Contact section
        contact_title = ModernLabel(
            form_card,
            text="Información de Contacto",
            is_header=True
        )
        contact_title.grid(row=4, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 10))
        
        self.entries["phone_1"] = create_form_field(
            form_card, "Teléfono 1 *", 5,
            placeholder="Ej: +1 234 567 8900"
        )
        
        self.entries["phone_2"] = create_form_field(
            form_card, "Teléfono 2", 6,
            placeholder="Ej: +1 234 567 8901"
        )
        
        self.entries["email"] = create_form_field(
            form_card, "Email *", 7,
            placeholder="Ej: equipo@empresa.com"
        )
        
        self.entries["whatsapp"] = create_form_field(
            form_card, "WhatsApp", 8,
            placeholder="Ej: +1 234 567 8900"
        )
        
        # Separator
        separator2 = tk.Frame(form_card, height=1, bg=COLORS["input_border"])
        separator2.grid(row=9, column=0, columnspan=2, sticky="ew", padx=15, pady=15)
        
        # Additional info section
        info_title = ModernLabel(
            form_card,
            text="Información Adicional",
            is_header=True
        )
        info_title.grid(row=10, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 10))
        
        self.entries["address"] = create_form_field(
            form_card, "Dirección", 11,
            placeholder="Ej: Calle Principal #123"
        )
        
        # Payment method dropdown
        payment_label = ModernLabel(form_card, text="Método de Pago *")
        payment_label.grid(row=12, column=0, sticky="w", padx=10, pady=8)
        
        payment_methods = ["Efectivo", "Transferencia", "Cheque", "Depósito", "Otro"]
        self.entries["pay_method"] = tk.StringVar(value=payment_methods[0])
        payment_dropdown = tk.OptionMenu(
            form_card,
            self.entries["pay_method"],
            *payment_methods
        )
        payment_dropdown.configure(
            font=FONTS["text"],
            bg=COLORS["input_bg"],
            fg=COLORS["text_dark"],
            relief="solid",
            borderwidth=1,
            highlightthickness=0,
            activebackground=COLORS["secondary"],
            width=27
        )
        payment_dropdown.grid(row=12, column=1, sticky="ew", padx=10, pady=8)
        
        self.entries["username"] = create_form_field(
            form_card, "Usuario", 13,
            placeholder="Ej: usuario123"
        )
        
        # Required fields note
        note_label = tk.Label(
            form_card,
            text="* Campos obligatorios",
            font=("Segoe UI", 8, "italic"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_light"]
        )
        note_label.grid(row=14, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 15))
        
        # Load existing data if in update mode
        if self.mode == "update" and self.team_data:
            self._load_team_data()
        
        # Buttons frame
        buttons_frame = tk.Frame(self.container, bg=COLORS["background"])
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        # Save button
        save_text = "Guardar" if self.mode == "new" else "Actualizar"
        btn_save = tk.Button(
            buttons_frame,
            text=save_text,
            command=self._save_team,
            **BUTTON_STYLES["save"]
        )
        btn_save.pack(side="left", padx=5)
        
        # Cancel button
        btn_cancel = tk.Button(
            buttons_frame,
            text="Cancelar",
            command=self._go_back,
            **BUTTON_STYLES["cancel"]
        )
        btn_cancel.pack(side="left", padx=5)
        
        # Back button
        btn_back = tk.Button(
            buttons_frame,
            text="← Volver",
            command=self._go_back,
            **BUTTON_STYLES["back"]
        )
        btn_back.pack(side="right", padx=5)
    
    def _load_team_data(self):
        """Cargar datos del equipo en el formulario"""
        if "team_number" in self.team_data:
            self.entries["team_number"].delete(0, tk.END)
            self.entries["team_number"].insert(0, self.team_data["team_number"])
        
        # Cargar otros campos...
        # (implementar según la estructura de datos)
    
    def _validate_form(self):
        """Validar el formulario"""
        is_valid = True
        
        # Validar número de equipo
        team_number = self.entries["team_number"].get_value()
        if not team_number:
            validate_entry(self.entries["team_number"], False)
            is_valid = False
        else:
            validate_entry(self.entries["team_number"], True)
        
        # Validar nombre
        team_name = self.entries["team_name"].get_value()
        if not team_name:
            validate_entry(self.entries["team_name"], False)
            is_valid = False
        else:
            validate_entry(self.entries["team_name"], True)
        
        # Validar teléfono 1
        phone_1 = self.entries["phone_1"].get_value()
        if not phone_1:
            validate_entry(self.entries["phone_1"], False)
            is_valid = False
        else:
            validate_entry(self.entries["phone_1"], True)
        
        # Validar email
        email = self.entries["email"].get_value()
        if not email or "@" not in email:
            validate_entry(self.entries["email"], False)
            is_valid = False
        else:
            validate_entry(self.entries["email"], True)
        
        return is_valid
    
    def _save_team(self):
        """Guardar equipo de trabajo"""
        if not self._validate_form():
            show_message(
                self.container,
                "Validación",
                "Por favor completa todos los campos obligatorios correctamente.",
                "warning"
            )
            return
        
        # Recopilar datos del formulario
        team_data = {
            "team_number": self.entries["team_number"].get_value(),
            "team_name": self.entries["team_name"].get_value(),
            "phone_1": self.entries["phone_1"].get_value(),
            "phone_2": self.entries["phone_2"].get_value(),
            "email": self.entries["email"].get_value(),
            "whatsapp": self.entries["whatsapp"].get_value(),
            "address": self.entries["address"].get_value(),
            "pay_method": self.entries["pay_method"].get(),
            "username": self.entries["username"].get_value()
        }
        
        # TODO: Guardar en base de datos
        # Por ahora solo mostramos mensaje de éxito
        
        action = "creado" if self.mode == "new" else "actualizado"
        show_message(
            self.container,
            "Éxito",
            f"Equipo {action} correctamente.\n\nNúmero: {team_data['team_number']}\nNombre: {team_data['team_name']}",
            "success"
        )
        
        # Volver al submenú
        self._go_back()
    
    def _go_back(self):
        """Volver al submenú de Teams_Work"""
        self.app_controller.show_teams_work_submenu()
