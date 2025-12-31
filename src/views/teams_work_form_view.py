"""
Teams Work Form View - Formulario mejorado para gestionar equipos de trabajo
"""

import tkinter as tk
from tkinter import messagebox
from src.views.base_view import BaseView
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
        from src.components.ui_components import UIComponents
        title_text = "Nuevo Equipo de Trabajo" if self.mode == "new" else "Actualizar Equipo de Trabajo"
        UIComponents.create_header(self.container, title_text)
        
        # Main frame with scrollbar
        main_frame = tk.Frame(self.container, bg=COLORS["background"])
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Canvas and scrollbar for scrolling
        canvas = tk.Canvas(main_frame, bg=COLORS["background"], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["card_bg"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Form container
        form_card = tk.Frame(scrollable_frame, bg=COLORS["card_bg"], relief="solid", borderwidth=1)
        form_card.pack(fill="both", expand=True, padx=5, pady=5)
        form_card.columnconfigure(1, weight=1)
        
        # Form title
        form_title = tk.Label(
            form_card,
            text="Team Information",
            font=FONTS["subtitle"],
            bg=COLORS["card_bg"],
            fg=COLORS["text_dark"]
        )
        form_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 10))
        
        # Team Number
        tk.Label(form_card, text="Team Number *", font=FONTS["text"], 
                bg=COLORS["card_bg"], fg=COLORS["text_dark"]).grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self.entries["team_number"] = tk.Entry(form_card, font=FONTS["text"], relief="solid", borderwidth=1)
        self.entries["team_number"].grid(row=1, column=1, sticky="ew", padx=10, pady=8)
        
        # Team Name
        tk.Label(form_card, text="Team Name *", font=FONTS["text"], 
                bg=COLORS["card_bg"], fg=COLORS["text_dark"]).grid(row=2, column=0, sticky="w", padx=10, pady=8)
        self.entries["team_name"] = tk.Entry(form_card, font=FONTS["text"], relief="solid", borderwidth=1)
        self.entries["team_name"].grid(row=2, column=1, sticky="ew", padx=10, pady=8)
        
        # Separator
        tk.Frame(form_card, height=1, bg=COLORS["input_border"]).grid(row=3, column=0, columnspan=2, sticky="ew", padx=15, pady=15)
        
        # Contact section header
        tk.Label(
            form_card,
            text="Contact Information",
            font=FONTS["subtitle"],
            bg=COLORS["card_bg"],
            fg=COLORS["text_dark"]
        ).grid(row=4, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 10))
        
        # Address
        tk.Label(form_card, text="Address", font=FONTS["text"], 
                bg=COLORS["card_bg"], fg=COLORS["text_dark"]).grid(row=9, column=0, sticky="w", padx=10, pady=8)
        self.entries["address"] = tk.Entry(form_card, font=FONTS["text"], relief="solid", borderwidth=1)
        self.entries["address"].grid(row=9, column=1, sticky="ew", padx=10, pady=8)
        
        # Phone 1
        tk.Label(form_card, text="Phone 1 *", font=FONTS["text"], 
                bg=COLORS["card_bg"], fg=COLORS["text_dark"]).grid(row=5, column=0, sticky="w", padx=10, pady=8)
        self.entries["phone_1"] = tk.Entry(form_card, font=FONTS["text"], relief="solid", borderwidth=1)
        self.entries["phone_1"].grid(row=5, column=1, sticky="ew", padx=10, pady=8)
        
        # Phone 2
        tk.Label(form_card, text="Phone 2", font=FONTS["text"], 
                bg=COLORS["card_bg"], fg=COLORS["text_dark"]).grid(row=6, column=0, sticky="w", padx=10, pady=8)
        self.entries["phone_2"] = tk.Entry(form_card, font=FONTS["text"], relief="solid", borderwidth=1)
        self.entries["phone_2"].grid(row=6, column=1, sticky="ew", padx=10, pady=8)
        
        # Email
        tk.Label(form_card, text="Email *", font=FONTS["text"], 
                bg=COLORS["card_bg"], fg=COLORS["text_dark"]).grid(row=7, column=0, sticky="w", padx=10, pady=8)
        self.entries["email"] = tk.Entry(form_card, font=FONTS["text"], relief="solid", borderwidth=1)
        self.entries["email"].grid(row=7, column=1, sticky="ew", padx=10, pady=8)
        
        # WhatsApp
        tk.Label(form_card, text="WhatsApp", font=FONTS["text"], 
                bg=COLORS["card_bg"], fg=COLORS["text_dark"]).grid(row=8, column=0, sticky="w", padx=10, pady=8)
        self.entries["whatsapp"] = tk.Entry(form_card, font=FONTS["text"], relief="solid", borderwidth=1)
        self.entries["whatsapp"].grid(row=8, column=1, sticky="ew", padx=10, pady=8)
        
        # Separator
        tk.Frame(form_card, height=1, bg=COLORS["input_border"]).grid(row=10, column=0, columnspan=2, sticky="ew", padx=15, pady=15)
        
        # Additional info section header
        tk.Label(
            form_card,
            text="Bank Information",
            font=FONTS["subtitle"],
            bg=COLORS["card_bg"],
            fg=COLORS["text_dark"]
        ).grid(row=11, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 10))
        
        # Payment method dropdown
        tk.Label(form_card, text="Payment Method *", font=FONTS["text"], 
                bg=COLORS["card_bg"], fg=COLORS["text_dark"]).grid(row=12, column=0, sticky="w", padx=10, pady=8)
        self.entries["payment_method"] = tk.Entry(form_card, font=FONTS["text"], relief="solid", borderwidth=1)
        self.entries["payment_method"].grid(row=12, column=1, sticky="ew", padx=10, pady=8)
        # payment_methods = ["Efectivo", "Transferencia", "Cheque", "Depósito", "Otro"]
        # self.entries["pay_method"] = tk.StringVar(value=payment_methods[0])
        # payment_dropdown = tk.OptionMenu(form_card, self.entries["pay_method"], *payment_methods)
        # payment_dropdown.configure(font=FONTS["text"], bg=COLORS["input_bg"], fg=COLORS["text_dark"], 
        #                           relief="solid", borderwidth=1, highlightthickness=0, width=27)
        # payment_dropdown.grid(row=12, column=1, sticky="ew", padx=10, pady=8)
        
        # Username
        tk.Label(form_card, text="Username", font=FONTS["text"], 
                bg=COLORS["card_bg"], fg=COLORS["text_dark"]).grid(row=13, column=0, sticky="w", padx=10, pady=8)
        self.entries["username"] = tk.Entry(form_card, font=FONTS["text"], relief="solid", borderwidth=1)
        self.entries["username"].grid(row=13, column=1, sticky="ew", padx=10, pady=8)
        
        # Required fields note
        tk.Label(
            form_card,
            text="* Fields required",
            font=("Segoe UI", 8, "italic"),
            bg=COLORS["card_bg"],
            fg=COLORS["text_light"]
        ).grid(row=14, column=0, columnspan=2, sticky="w", padx=15, pady=(10, 15))
        
        # Load existing data if in update mode
        if self.mode == "update" and self.team_data:
            self._load_team_data()
        
        # Buttons frame
        buttons_frame = tk.Frame(self.container, bg=COLORS["background"])
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        # Save button
        save_text = "💾 Save" if self.mode == "new" else "✏️ Update"
        btn_save = tk.Button(buttons_frame, text=save_text, command=self._save_team, **BUTTON_STYLES["save"])
        btn_save.pack(side="left", padx=5)
        
        # Cancel button
        btn_cancel = tk.Button(buttons_frame, text="❌ Cancel", command=self._go_back, **BUTTON_STYLES["cancel"])
        btn_cancel.pack(side="left", padx=5)
        
        # Back button
        btn_back = tk.Button(buttons_frame, text="← Back", command=self._go_back, **BUTTON_STYLES["back"])
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
        errors = []
        
        # Validar número de equipo
        team_number = self.entries["team_number"].get().strip()
        if not team_number:
            errors.append("Número de equipo es requerido")
            is_valid = False
        
        # Validar nombre
        team_name = self.entries["team_name"].get().strip()
        if not team_name:
            errors.append("Nombre del equipo es requerido")
            is_valid = False
        
        # Validar teléfono 1
        phone_1 = self.entries["phone_1"].get().strip()
        if not phone_1:
            errors.append("Teléfono 1 es requerido")
            is_valid = False
        
        # Validar email
        email = self.entries["email"].get().strip()
        if not email or "@" not in email:
            errors.append("Email válido es requerido")
            is_valid = False
        
        if not is_valid:
            messagebox.showwarning("Validación", "\n".join(errors))
        
        return is_valid
    
    def _save_team(self):
        """Guardar equipo de trabajo"""
        if not self._validate_form():
            return
        
        # Recopilar datos del formulario
        team_data = {
            "team_number": self.entries["team_number"].get().strip(),
            "team_name": self.entries["team_name"].get().strip(),
            "phone_1": self.entries["phone_1"].get().strip(),
            "phone_2": self.entries["phone_2"].get().strip(),
            "email": self.entries["email"].get().strip(),
            "address": self.entries["address"].get().strip(),
            "whatsapp": self.entries["whatsapp"].get().strip(),
            "pay_method": self.entries["pay_method"].get(),
            "username": self.entries["username"].get().strip()
        }
        
        # TODO: Guardar en base de datos
        # Por ahora solo mostramos mensaje de éxito
        
        action = "creado" if self.mode == "new" else "actualizado"
        messagebox.showinfo(
            "Éxito",
            f"Equipo {action} correctamente.\n\nNúmero: {team_data['team_number']}\nNombre: {team_data['team_name']}"
        )
        
        # Volver al submenú
        self._go_back()
    
    def _go_back(self):
        """Volver al submenú de Teams_Work"""
        self.app_controller.show_teams_work_submenu()
