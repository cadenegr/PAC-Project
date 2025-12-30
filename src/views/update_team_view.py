"""
Update Team View - List and edit existing teams
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.views.base_view import BaseView
from src.models.database import Database, Team
from config.settings import COLORS, FONTS, BUTTON_STYLES


class UpdateTeamView(BaseView):
    """View for updating existing teams"""
    
    def __init__(self, container, app_controller):
        """Initialize the update team view"""
        super().__init__(container, app_controller)
        self.db = Database()
        self.team_model = Team(self.db)
        self.selected_team = None
        self.entries = {}
    
    def render(self):
        """Render the update team view"""
        self.clear_container()
        
        # Title
        title = tk.Label(
            self.container,
            text="Update Team",
            font=FONTS["subtitle"],
            bg=COLORS["background"],
            fg=COLORS["text_dark"]
        )
        title.pack(pady=20)
        
        # Create main frame with two sections
        main_frame = tk.Frame(self.container, bg=COLORS["background"])
        main_frame.pack(fill="both", expand=True, padx=20)
        
        # Left section - Team list
        left_frame = tk.Frame(main_frame, bg=COLORS["background"])
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Search frame
        search_frame = tk.Frame(left_frame, bg=COLORS["background"])
        search_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            search_frame,
            text="Search:",
            font=FONTS["text"],
            bg=COLORS["background"],
            fg=COLORS["text_dark"]
        ).pack(side="left", padx=(0, 5))
        
        self.search_entry = tk.Entry(
            search_frame,
            font=FONTS["text"],
            bg=COLORS["white"]
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_teams())
        
        # Team listbox
        list_label = tk.Label(
            left_frame,
            text="Select a team:",
            font=FONTS["text"],
            bg=COLORS["background"],
            fg=COLORS["text_dark"],
            anchor="w"
        )
        list_label.pack(fill="x", pady=(0, 5))
        
        list_frame = tk.Frame(left_frame, bg=COLORS["white"], relief="solid", borderwidth=1)
        list_frame.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.team_listbox = tk.Listbox(
            list_frame,
            font=FONTS["text"],
            bg=COLORS["white"],
            fg=COLORS["text_dark"],
            yscrollcommand=scrollbar.set,
            activestyle='none',
            selectmode=tk.SINGLE
        )
        self.team_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.team_listbox.yview)
        
        self.team_listbox.bind('<<ListboxSelect>>', self.on_team_select)
        
        # Right section - Edit form
        right_frame = tk.Frame(main_frame, bg=COLORS["background"])
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Form title
        form_title = tk.Label(
            right_frame,
            text="Team Details:",
            font=FONTS["text"],
            bg=COLORS["background"],
            fg=COLORS["text_dark"],
            anchor="w"
        )
        form_title.pack(fill="x", pady=(0, 10))
        
        # Form fields
        fields = [
            ("Team Number", "team_number", True, True),  # readonly
            ("Team Name *", "team_name", True, False),
            ("Phone 1", "team_phone_1", False, False),
            ("Phone 2", "team_phone_2", False, False),
            ("Email", "team_email", False, False),
            ("WhatsApp", "team_wassup", False, False),
            ("Address", "team_address", False, False),
            ("Payment Method", "team_pay_method", False, False),
            ("Username", "team_username", False, False)
        ]
        
        for label_text, field_name, required, readonly in fields:
            # Label
            label = tk.Label(
                right_frame,
                text=label_text,
                font=("Arial", 10),
                bg=COLORS["background"],
                fg=COLORS["text_dark"],
                anchor="w"
            )
            label.pack(fill="x", pady=(5, 2))
            
            # Entry
            entry = tk.Entry(
                right_frame,
                font=("Arial", 10),
                bg=COLORS["white"] if not readonly else "#e0e0e0",
                fg=COLORS["text_dark"],
                relief="solid",
                borderwidth=1,
                state="readonly" if readonly else "normal"
            )
            entry.pack(fill="x", pady=(0, 2))
            self.entries[field_name] = entry
        
        # Buttons
        button_frame = tk.Frame(self.container, bg=COLORS["background"])
        button_frame.pack(pady=15)
        
        # Update button
        btn_update = tk.Button(
            button_frame,
            text="Update",
            command=self.update_team,
            font=FONTS["button_small"],
            width=12,
            height=2,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            activebackground=COLORS["primary_hover"],
            border=0,
            cursor="hand2"
        )
        btn_update.pack(side="left", padx=5)
        
        # Delete button
        btn_delete = tk.Button(
            button_frame,
            text="Delete",
            command=self.delete_team,
            font=FONTS["button_small"],
            width=12,
            height=2,
            bg=COLORS["danger"],
            fg=COLORS["white"],
            activebackground=COLORS["danger_hover"],
            border=0,
            cursor="hand2"
        )
        btn_delete.pack(side="left", padx=5)
        
        # Back button
        btn_back = tk.Button(
            self.container,
            text="← Back to Teams_Work",
            command=self.app_controller.show_teams_work_submenu,
            **BUTTON_STYLES["back"]
        )
        btn_back.pack(pady=5)
        
        # Load teams
        self.load_teams()
    
    def load_teams(self):
        """Load teams into listbox"""
        self.team_listbox.delete(0, tk.END)
        
        search_term = self.search_entry.get().strip()
        
        if search_term:
            teams = self.team_model.search(search_term)
        else:
            teams = self.team_model.get_all()
        
        for team in teams:
            display_text = f"#{team['team_number']} - {team['team_name']}"
            self.team_listbox.insert(tk.END, display_text)
            self.team_listbox.itemconfig(tk.END, {'team_data': team})
    
    def on_team_select(self, event):
        """Handle team selection from listbox"""
        selection = self.team_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        
        # Get all teams again (matching current search)
        search_term = self.search_entry.get().strip()
        if search_term:
            teams = self.team_model.search(search_term)
        else:
            teams = self.team_model.get_all()
        
        if index < len(teams):
            self.selected_team = teams[index]
            self.populate_form()
    
    def populate_form(self):
        """Populate form with selected team data"""
        if not self.selected_team:
            return
        
        for field_name, entry in self.entries.items():
            # Enable entry temporarily if readonly
            if entry['state'] == 'readonly':
                entry.config(state='normal')
            
            # Clear and set value
            entry.delete(0, tk.END)
            value = self.selected_team.get(field_name, '')
            if value:
                entry.insert(0, str(value))
            
            # Restore readonly state for team_number
            if field_name == 'team_number':
                entry.config(state='readonly')
    
    def update_team(self):
        """Update the selected team"""
        if not self.selected_team:
            messagebox.showwarning(
                "Warning",
                "Please select a team to update"
            )
            return
        
        # Get values from entries
        team_data = {}
        for field_name, entry in self.entries.items():
            if field_name != 'team_number':  # Skip readonly field
                team_data[field_name] = entry.get().strip()
        
        # Validate required field
        if not team_data.get('team_name'):
            messagebox.showerror(
                "Error",
                "Team Name is required!"
            )
            return
        
        # Update in database
        success = self.team_model.update(
            self.selected_team['team_number'],
            team_data
        )
        
        if success:
            messagebox.showinfo(
                "Success",
                "Team updated successfully!"
            )
            self.load_teams()
        else:
            messagebox.showerror(
                "Error",
                "Failed to update team. Please try again."
            )
    
    def delete_team(self):
        """Delete the selected team"""
        if not self.selected_team:
            messagebox.showwarning(
                "Warning",
                "Please select a team to delete"
            )
            return
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete team:\n{self.selected_team['team_name']}?\n\nThis action cannot be undone."
        )
        
        if not confirm:
            return
        
        # Delete from database
        success = self.team_model.delete(self.selected_team['team_number'])
        
        if success:
            messagebox.showinfo(
                "Success",
                "Team deleted successfully!"
            )
            self.selected_team = None
            self.load_teams()
            
            # Clear form
            for entry in self.entries.values():
                if entry['state'] != 'readonly':
                    entry.delete(0, tk.END)
                else:
                    entry.config(state='normal')
                    entry.delete(0, tk.END)
                    entry.config(state='readonly')
        else:
            messagebox.showerror(
                "Error",
                "Failed to delete team. Please try again."
            )
    
    def __del__(self):
        """Cleanup database connection"""
        if hasattr(self, 'db'):
            self.db.close()
