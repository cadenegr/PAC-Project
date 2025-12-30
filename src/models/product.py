"""
Product Model
Database model for products in ABC_Catalog
"""


class Product:
    """Product data model"""
    
    def __init__(self, pro_part, pro_description, pro_unit, 
                 pro_price1=0.0, pro_price2=0.0, product_id=None):
        """
        Initialize Product instance
        
        Args:
            pro_part (str): Product part number (alphanumeric, max 12 chars) - Primary key
            pro_description (str): Product description (alphanumeric, max 30 chars)
            pro_unit (str): Unit of measure (alphanumeric, max 4 chars)
            pro_price1 (float): First price (numeric, max 12 digits)
            pro_price2 (float): Second price (numeric, max 12 digits)
            product_id (int): Database ID (auto-generated)
        """
        self.product_id = product_id
        self.pro_part = pro_part[:12] if pro_part else ""  # Limit to 12 chars
        self.pro_description = pro_description[:30] if pro_description else ""  # Limit to 30 chars
        self.pro_unit = pro_unit[:4] if pro_unit else ""  # Limit to 4 chars
        self.pro_price1 = float(pro_price1) if pro_price1 else 0.0
        self.pro_price2 = float(pro_price2) if pro_price2 else 0.0
    
    def __repr__(self):
        return f"Product({self.pro_part}, {self.pro_description}, {self.pro_unit})"
    
    def to_dict(self):
        """Convert product to dictionary"""
        return {
            'product_id': self.product_id,
            'pro_part': self.pro_part,
            'pro_description': self.pro_description,
            'pro_unit': self.pro_unit,
            'pro_price1': self.pro_price1,
            'pro_price2': self.pro_price2
        }
    
    @staticmethod
    def from_dict(data):
        """Create Product instance from dictionary"""
        return Product(
            pro_part=data.get('pro_part'),
            pro_description=data.get('pro_description'),
            pro_unit=data.get('pro_unit'),
            pro_price1=data.get('pro_price1', 0.0),
            pro_price2=data.get('pro_price2', 0.0),
            product_id=data.get('product_id')
        )
    
    def validate(self):
        """
        Validate product data
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not self.pro_part or len(self.pro_part.strip()) == 0:
            return False, "Pro.Part es requerido"
        
        if len(self.pro_part) > 12:
            return False, "Pro.Part no puede exceder 12 caracteres"
        
        if not self.pro_description or len(self.pro_description.strip()) == 0:
            return False, "Pro.Description es requerido"
        
        if len(self.pro_description) > 30:
            return False, "Pro.Description no puede exceder 30 caracteres"
        
        if not self.pro_unit or len(self.pro_unit.strip()) == 0:
            return False, "Pro.Unit es requerido"
        
        if len(self.pro_unit) > 4:
            return False, "Pro.Unit no puede exceder 4 caracteres"
        
        if self.pro_price1 < 0:
            return False, "Pro.Price1 no puede ser negativo"
        
        if self.pro_price2 < 0:
            return False, "Pro.Price2 no puede ser negativo"
        
        return True, ""
