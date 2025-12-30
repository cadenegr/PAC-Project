"""
Products Management View (Refactored)
Now uses BaseCRUDView - reduced from 721 to ~80 lines
"""

from src.views.base_crud_view import BaseCRUDView
from src.database.product_db import ProductDatabase
from src.models.product import Product


class ProductsView(BaseCRUDView):
    """Products management view - inherits all CRUD logic from base"""
    
    def __init__(self, container, app_controller):
        super().__init__(container, app_controller)
        self.db = ProductDatabase()
    
    def get_title(self):
        return "Products Management"
    
    def get_field_definitions(self):
        return [
            {'name': 'pro_part', 'label': 'Product Part *:', 'type': 'primary', 'width': 12, 'maxlength': 12},
            {'name': 'pro_description', 'label': 'Description *:', 'type': 'secondary', 'width': 30, 'maxlength': 30},
            {'name': 'pro_unit', 'label': 'Unit *:', 'type': 'text', 'width': 4, 'maxlength': 4},
            {'name': 'pro_price1', 'label': 'Price 1:', 'type': 'numeric', 'width': 15, 'maxlength': 12, 'decimals': 2},
            {'name': 'pro_price2', 'label': 'Price 2:', 'type': 'numeric', 'width': 15, 'maxlength': 12, 'decimals': 2}
        ]
    
    def get_database(self):
        return self.db
    
    def get_model_class(self):
        return Product
    
    def get_primary_key_name(self):
        return 'pro_part'
    
    def get_record_by_primary_key(self, key):
        return self.db.get_product_by_part(key)
    
    def search_by_secondary_key(self, value):
        return self.db.search_by_description(value)
    
    def get_all_records(self):
        return self.db.get_all_products()
    
    def create_record(self, model):
        return self.db.create_product(model)
    
    def update_record(self, model):
        return self.db.update_product(model)
    
    def delete_record(self, primary_key):
        return self.db.delete_product(primary_key)
    
    def get_list_columns(self):
        return [
            ('pro_part', 'Pro.Part', 120),
            ('pro_description', 'Description', 300),
            ('pro_unit', 'Unit', 80),
            ('pro_price1', 'Price 1', 120),
            ('pro_price2', 'Price 2', 120)
        ]
