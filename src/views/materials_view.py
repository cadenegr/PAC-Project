"""
Materials Management View (Refactored)
Now uses BaseCRUDView - reduced from 908 to ~95 lines
"""

from src.views.base_crud_view import BaseCRUDView
from src.database.material_db import MaterialDatabase
from src.models.material import Material


class MaterialsView(BaseCRUDView):
    """Materials management view - inherits all CRUD logic from base"""
    
    def __init__(self, container, app_controller):
        super().__init__(container, app_controller)
        self.db = MaterialDatabase()
    
    def get_title(self):
        return "Materials Management"
    
    def get_field_definitions(self):
        return [
            {'name': 'raw_part', 'label': 'Part Number  *:', 'type': 'primary', 'width': 12, 'maxlength': 12},
            {'name': 'raw_description', 'label': 'Description *:', 'type': 'secondary', 'width': 30, 'maxlength': 30},
            {'name': 'raw_unit', 'label': 'Unit *:', 'type': 'text', 'width': 10, 'maxlength': 10},
            {'name': 'raw_price1', 'label': 'Actual Price:', 'type': 'numeric', 'width': 15, 'maxlength': 12, 'decimals': 2},
            {'name': 'raw_price2', 'label': 'Previous Price:', 'type': 'numeric', 'width': 15, 'maxlength': 12, 'decimals': 2},
            {'name': 'raw_balance', 'label': 'Balance:', 'type': 'numeric', 'width': 15, 'maxlength': 15, 'decimals': 2}
        ]
    
    def get_database(self):
        return self.db
    
    def get_model_class(self):
        return Material
    
    def get_primary_key_name(self):
        return 'raw_part'
    
    def get_record_by_primary_key(self, key):
        return self.db.get_material_by_part(key)
    
    def search_by_secondary_key(self, value):
        return self.db.search_by_description(value)
    
    def get_all_records(self):
        return self.db.get_all_materials()
    
    def create_record(self, model):
        return self.db.create_material(model)
    
    def update_record(self, model):
        return self.db.update_material(model)
    
    def delete_record(self, primary_key):
        return self.db.delete_material(primary_key)
    
    def get_list_columns(self):
        return [
            ('raw_part', 'Raw.Part', 120),
            ('raw_description', 'Description', 250),
            ('raw_unit', 'Unit', 80),
            ('raw_price1', 'Price 1', 120),
            ('raw_balance', 'Balance', 120)
        ]
