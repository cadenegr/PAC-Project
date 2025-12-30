"""
Suppliers Management View (Refactored)
Now uses BaseCRUDView - reduced from 635 to ~80 lines
"""

from src.views.base_crud_view import BaseCRUDView
from src.database.supplier_db import SupplierDatabase
from src.models.supplier import Supplier


class SuppliersView(BaseCRUDView):
    """Suppliers management view - inherits all CRUD logic from base"""
    
    def __init__(self, container, app_controller):
        super().__init__(container, app_controller)
        self.db = SupplierDatabase()
    
    def get_title(self):
        return "Suppliers Management"
    
    def get_field_definitions(self):
        return [
            {'name': 'sup_number', 'label': 'Supplier Number *:', 'type': 'primary', 'width': 12, 'maxlength': 12},
            {'name': 'sup_name', 'label': 'Name *:', 'type': 'secondary', 'width': 30, 'maxlength': 30},
            {'name': 'sup_address', 'label': 'Address:', 'type': 'text', 'width': 30, 'maxlength': 30},
            {'name': 'sup_phone1', 'label': 'Phone 1:', 'type': 'text', 'width': 12, 'maxlength': 12},
            {'name': 'sup_phone2', 'label': 'Phone 2:', 'type': 'text', 'width': 12, 'maxlength': 12},
            {'name': 'sup_email', 'label': 'Email:', 'type': 'text', 'width': 30, 'maxlength': 30},
            {'name': 'sup_paymethod', 'label': 'Payment Method:', 'type': 'text', 'width': 20, 'maxlength': 20},
            {'name': 'sup_username', 'label': 'Username:', 'type': 'text', 'width': 20, 'maxlength': 20}
        ]
    
    def get_database(self):
        return self.db
    
    def get_model_class(self):
        return Supplier
    
    def get_primary_key_name(self):
        return 'sup_number'
    
    def get_record_by_primary_key(self, key):
        return self.db.get_supplier_by_number(key)
    
    def search_by_secondary_key(self, value):
        return self.db.search_by_name(value)
    
    def get_all_records(self):
        return self.db.get_all_suppliers()
    
    def create_record(self, model):
        return self.db.create_supplier(model)
    
    def update_record(self, model):
        return self.db.update_supplier(model)
    
    def delete_record(self, primary_key):
        return self.db.delete_supplier(primary_key)
    
    def get_list_columns(self):
        return [
            ('sup_number', 'Sup.Number', 100),
            ('sup_name', 'Name', 250),
            ('sup_phone1', 'Phone 1', 120),
            ('sup_email', 'Email', 250)
        ]
