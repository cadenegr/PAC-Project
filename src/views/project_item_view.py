"""
Project Item Detail View
"""

import tkinter as tk
from tkinter import messagebox
from src.views.base_view import BaseView
from config.settings import COLORS, FONTS, BUTTON_STYLES, PROJECT_SUBMENU
from src.utils.pdf_handler import PDFHandler


class ProjectItemView(BaseView):
    """Detail view for project submenu items"""
    
    def __init__(self, container, app_controller, item_id):
        """
        Initialize the project item view
        
        Args:
            container: The parent container widget
            app_controller: Reference to the main application controller
            item_id: ID of the project item to display
        """
        super().__init__(container, app_controller)
        self.item_id = item_id
        self.item_data = self._get_item_data()
    
    def _get_item_data(self):
        """Get item data from configuration"""
        for item in PROJECT_SUBMENU:
            if item["id"] == self.item_id:
                return item
        return None
    
    def render(self):
        """Render the project item detail view"""
        self.clear_container()
        
        if not self.item_data:
            self._render_error()
            return
        
        # Title
        screen_title = tk.Label(
            self.container,
            text=self.item_data["title"],
            font=FONTS["subtitle"],
            bg=COLORS["background"],
            fg=COLORS["text_dark"]
        )
        screen_title.pack(pady=30)
        
        # Special rendering for Original_Project
        if self.item_id == "original_project":
            self._render_original_project()
        else:
            # Default content area for other items
            self._render_default_content()
        
        # Back button
        btn_back = tk.Button(
            self.container,
            text="← Back to Project",
            command=self.app_controller.show_project_submenu,
            **BUTTON_STYLES["back"]
        )
        btn_back.pack(pady=20)
    
    def _render_default_content(self):
        """Render default content area"""
        content_frame = tk.Frame(
            self.container,
            bg=COLORS["white"],
            relief="solid",
            borderwidth=1
        )
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        content_label = tk.Label(
            content_frame,
            text=self.item_data["description"],
            font=FONTS["text"],
            bg=COLORS["white"],
            fg=COLORS["text_light"],
            justify="left",
            wraplength=350
        )
        content_label.pack(padx=20, pady=20)
    
    def _render_original_project(self):
        """Render Original_Project with PDF viewer functionality"""
        # Info text
        info_frame = tk.Frame(
            self.container,
            bg=COLORS["white"],
            relief="solid",
            borderwidth=1
        )
        info_frame.pack(padx=20, pady=10, fill="x")
        
        info_label = tk.Label(
            info_frame,
            text="View the original project document and client order.",
            font=FONTS["text"],
            bg=COLORS["white"],
            fg=COLORS["text_light"],
            justify="center"
        )
        info_label.pack(padx=20, pady=15)
        
        # Buttons frame
        buttons_frame = tk.Frame(
            self.container,
            bg=COLORS["background"]
        )
        buttons_frame.pack(pady=20)
        
        # View PDF button
        btn_view_pdf = tk.Button(
            buttons_frame,
            text="📄 View Project PDF",
            command=self._view_project_pdf,
            font=FONTS["button"],
            width=20,
            height=2,
            bg=COLORS["primary"],
            fg=COLORS["white"],
            activebackground=COLORS["primary_hover"],
            border=0,
            cursor="hand2"
        )
        btn_view_pdf.pack(pady=5)
        
        # Select PDF button
        btn_select_pdf = tk.Button(
            buttons_frame,
            text="📁 Select PDF File",
            command=self._select_pdf_file,
            font=FONTS["button"],
            width=20,
            height=2,
            bg=COLORS["secondary"],
            fg=COLORS["white"],
            activebackground=COLORS["secondary_hover"],
            border=0,
            cursor="hand2"
        )
        btn_select_pdf.pack(pady=5)
        
        # Status label
        self.status_label = tk.Label(
            self.container,
            text="",
            font=FONTS["text"],
            bg=COLORS["background"],
            fg=COLORS["text_light"]
        )
        self.status_label.pack(pady=10)
        
        # Check if PDF exists
        self._check_pdf_status()
    
    def _view_project_pdf(self):
        """Open the project PDF file"""
        pdf_path = PDFHandler.get_project_pdf_path("original_project.pdf")
        
        if PDFHandler.open_pdf(pdf_path):
            self.status_label.config(
                text="✓ PDF opened successfully",
                fg=COLORS["primary"]
            )
        else:
            self.status_label.config(
                text="✗ No PDF file found. Please select a PDF first.",
                fg=COLORS["danger"]
            )
    
    def _select_pdf_file(self):
        """Allow user to select a PDF file to use as project document"""
        import shutil
        
        selected_pdf = PDFHandler.select_pdf()
        
        if selected_pdf:
            try:
                # Copy selected PDF to projects folder
                destination = PDFHandler.get_project_pdf_path("original_project.pdf")
                shutil.copy2(selected_pdf, destination)
                
                self.status_label.config(
                    text="✓ PDF file saved successfully",
                    fg=COLORS["primary"]
                )
                messagebox.showinfo(
                    "Success",
                    "Project PDF has been saved!\nYou can now view it anytime."
                )
            except Exception as e:
                self.status_label.config(
                    text=f"✗ Error saving PDF: {str(e)}",
                    fg=COLORS["danger"]
                )
                messagebox.showerror("Error", f"Could not save PDF:\n{str(e)}")
    
    def _check_pdf_status(self):
        """Check if project PDF exists and update status"""
        import os
        pdf_path = PDFHandler.get_project_pdf_path("original_project.pdf")
        
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path) / 1024  # KB
            self.status_label.config(
                text=f"📄 Project PDF ready ({file_size:.1f} KB)",
                fg=COLORS["primary"]
            )
        else:
            self.status_label.config(
                text="No PDF file found. Please select a PDF to upload.",
                fg=COLORS["text_light"]
            )
    
    def _render_error(self):
        """Render error message if item not found"""
        error_label = tk.Label(
            self.container,
            text="Error: Item not found",
            font=FONTS["subtitle"],
            bg=COLORS["background"],
            fg=COLORS["danger"]
        )
        error_label.pack(pady=50)
        
        btn_back = tk.Button(
            self.container,
            text="← Back to Project",
            command=self.app_controller.show_project_submenu,
            **BUTTON_STYLES["back"]
        )
        btn_back.pack(pady=20)
