"""
Form Builder - Dynamic form construction from field definitions
Builds complete forms with validation, search, and formatting
"""

import tkinter as tk
from src.components.ui_components import UIComponents


class FormBuilder:
    """Builds dynamic forms from field configurations"""
    
    def __init__(self, parent):
        self.parent = parent
        self.fields = {}
        self.entries = {}
    
    def build_form(self, field_definitions, primary_search_callback=None, secondary_search_callback=None):
        """
        Build complete form from field definitions
        
        field_definitions: List of dicts with structure:
        {
            'name': 'field_name',           # Internal name (mat_number, prod_code, etc)
            'label': 'Display Label *:',    # Label text shown to user
            'type': 'text',                 # 'text', 'numeric', 'primary', 'secondary'
            'width': 20,                    # Entry width in characters
            'maxlength': 20,                # Max character length
            'decimals': 2,                  # For numeric fields (default 2)
            'search_callback': func         # Optional custom search function
        }
        
        Returns: dict of {field_name: entry_widget}
        """
        fields_frame = tk.Frame(self.parent, bg="#F0F0F0")
        fields_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        for row, field_def in enumerate(field_definitions):
            name = field_def['name']
            label = field_def['label']
            field_type = field_def.get('type', 'text')
            width = field_def.get('width', 20)
            maxlength = field_def.get('maxlength', None)
            decimals = field_def.get('decimals', 2)
            search_callback = field_def.get('search_callback', None)
            
            # Create label
            UIComponents.create_form_label(fields_frame, label, row)
            
            # Create entry based on type
            if field_type == 'primary':
                # Primary key field with search button
                entry_frame = tk.Frame(fields_frame, bg="#F0F0F0")
                entry_frame.grid(row=row, column=1, pady=8, sticky="ew", padx=(0, 10))
                
                entry = tk.Entry(
                    entry_frame,
                    font=("Segoe UI", 10),
                    relief="solid",
                    borderwidth=1,
                    width=width
                )
                entry.pack(side="left", padx=(0, 5))
                
                if maxlength:
                    vcmd = (entry.register(lambda text: len(text) <= maxlength), '%P')
                    entry.config(validate="key", validatecommand=vcmd)
                
                if primary_search_callback:
                    entry.bind("<Return>", lambda e: primary_search_callback())
                    entry.bind("<FocusOut>", lambda e: primary_search_callback())
                
                btn_search = UIComponents.create_search_button(entry_frame, primary_search_callback)
                btn_search.pack(side="left")
                
                self.entries[name] = entry
            
            elif field_type == 'secondary':
                # Secondary search field (like name)
                entry = UIComponents.create_entry(fields_frame, row, width=width, maxlength=maxlength)
                
                if secondary_search_callback:
                    entry.bind("<Return>", lambda e: secondary_search_callback())
                
                self.entries[name] = entry
                
                # Add search button in column 2
                btn_search = UIComponents.create_search_button(fields_frame, secondary_search_callback)
                btn_search.grid(row=row, column=2, pady=8, padx=5)
            
            elif field_type == 'numeric':
                # Numeric field with formatting
                entry = UIComponents.create_numeric_entry(
                    fields_frame, row, 
                    width=width, 
                    maxlength=maxlength, 
                    decimals=decimals
                )
                self.entries[name] = entry
            
            else:
                # Standard text field
                entry = UIComponents.create_entry(fields_frame, row, width=width, maxlength=maxlength)
                self.entries[name] = entry
        
        fields_frame.columnconfigure(1, weight=1)
        
        return self.entries
    
    def get_values(self):
        """Get all form values as dict"""
        values = {}
        for name, entry in self.entries.items():
            value = entry.get().strip()
            # Remove commas from numeric fields
            if ',' in value:
                value = value.replace(',', '')
            values[name] = value
        return values
    
    def set_values(self, values_dict):
        """Set form values from dict"""
        for name, value in values_dict.items():
            if name in self.entries:
                entry = self.entries[name]
                entry.delete(0, tk.END)
                entry.insert(0, str(value) if value else "")
    
    def clear_all(self):
        """Clear all form fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    
    def focus_first(self):
        """Set focus to first entry"""
        if self.entries:
            first_entry = list(self.entries.values())[0]
            first_entry.focus()
