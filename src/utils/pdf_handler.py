"""
PDF Utilities
Functions for handling PDF files
"""

import os
import subprocess
import platform
from tkinter import filedialog, messagebox


class PDFHandler:
    """Handle PDF operations"""
    
    @staticmethod
    def open_pdf(pdf_path):
        """
        Open a PDF file with the system's default PDF viewer
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", f"PDF file not found:\n{pdf_path}")
            return False
        
        try:
            system = platform.system()
            
            if system == "Linux":
                subprocess.Popen(["xdg-open", pdf_path])
            elif system == "Darwin":  # macOS
                subprocess.Popen(["open", pdf_path])
            elif system == "Windows":
                os.startfile(pdf_path)
            else:
                messagebox.showerror("Error", "Unsupported operating system")
                return False
            
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open PDF:\n{str(e)}")
            return False
    
    @staticmethod
    def select_pdf():
        """
        Open file dialog to select a PDF file
        
        Returns:
            str: Path to selected PDF or None if cancelled
        """
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        return file_path if file_path else None
    
    @staticmethod
    def get_project_pdf_path(project_name="original_project.pdf"):
        """
        Get the path for a project PDF file
        
        Args:
            project_name: Name of the PDF file
            
        Returns:
            str: Full path to the PDF file
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        pdf_dir = os.path.join(base_dir, "data", "projects")
        
        # Create directory if it doesn't exist
        os.makedirs(pdf_dir, exist_ok=True)
        
        return os.path.join(pdf_dir, project_name)
