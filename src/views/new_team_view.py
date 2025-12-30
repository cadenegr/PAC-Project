"""
New Team View - Form to create new teams
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.views.base_view import BaseView
from src.models.database import Database, Team
from config.settings import COLORS, FONTS, BUTTON_STYLES


class NewTeamView(BaseView):
    """View for creating new teams"""
    
    def __init__(self, container, app_controller):
        """Initialize the new team view"""
        super().__init__(container, app_controller)
        self.db = Database()
        self.team_model = Team(self.db)
        self.entries = {}
    
    def render(self):
        """Render the new team form"""
        self.clear_container()
        
        # Title
        title = tk.Label(
            self.container,
            text="New Team",
            font=FONTS["subtitle"],
            bg=COLORS["background"],
            fg=COLORS["text_dark"]
        )
        title.pack(pady=20)
        
        # Form container with scrollbar
        form_frame = tk.Frame(self.container, bg=COLORS["background"])
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Canvas for scrolling
        canvas = tk.Canvas(form_frame, bg=COLORS["background"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["background"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        fields = [
            ("Team Name *", "team_name", True),
            ("Phone 1", "team_phone_1", False),
            ("Phone 2", "team_phone_2", False),
            ("Email", "team_email", False),
            ("WhatsApp", "team_wassup", False),
            ("Address", "team_address", False),
            ("Payment Method", "team_pay_method", False),
            ("Username", "team_username", False)
        ]
        
        for label_text, field_name, required in fields:
            # Label
            label = tk.Label(
                scrollable_frame,
                text=label_text,
                font=FONTS["text"],
                bg=COLORS["background"],
                fg=COLORS["text_dark"],
                anchor="w"
            )
            label.pack(fill="x", padx=10, pady=(10, 2))
            
            # Entry
            entry = tk.Entry(
                scrollable_frame,
                font=FONTS["text"],
                bg=COLORS["white"],
                fg=COLORS["text_dark"],
                relief="solid",
                borderwidth=1
            )
            entry.pack(fill="x", padx=10, pady=(0, 5))
            self.entries[field_name] = entry
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons container
        button_frame = tk.Frame(self.container, bg=COLORS["background"])
        button_frame.pack(pady=20)
        
        # Save button
        btn_save = tk.Button(
            button_frame,
            text="Save Team",
            command=self.save_team,
            font=FONTS["button"],
            width=15,
            height=2,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            activebackground=COLORS["primary_hover"],
            border=0,
            cursor="hand2"
        )
        btn_save.pack(side="left", padx=5)
        
        # Clear button
        btn_clear = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_form,
            font=FONTS["button"],
            width=15,
            height=2,
            bg=COLORS["text_light"],
            fg=COLORS["white"],
            activebackground="#555555",
            border=0,
            cursor="hand2"
        )
        btn_clear.pack(side="left", padx=5)
        
        # Back button
        btn_back = tk.Button(
            self.container,
            text="← Back to Teams_Work",
            command=self.app_controller.show_teams_work_submenu,
            **BUTTON_STYLES["back"]
        )
        btn_back.pack(pady=10)
    
    def save_team(self):
        """Save the new team to database"""
        # Get values from entries
        team_data = {}
        for field_name, entry in self.entries.items():
            team_data[field_name] = entry.get().strip()
        
        # Validate required field
        if not team_data.get('team_name'):
            messagebox.showerror(
                "Error",
                "Team Name is required!"
            )
            return
        
        # Save to database
        team_number = self.team_model.create(team_data)
        
        if team_number:
            messagebox.showinfo(
                "Success",
                f"Team created successfully!\nTeam Number: {team_number}"
            )
            self.clear_form()
        else:
            messagebox.showerror(
                "Error",
                "Failed to create team. Please try again."
            )
    
    def clear_form(self):
        """Clear all form fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        
        # Focus on first field
        if 'team_name' in self.entries:
            self.entries['team_name'].focus()
    
    def __del__(self):
        """Cleanup database connection"""
        if hasattr(self, 'db'):
            self.db.close()
