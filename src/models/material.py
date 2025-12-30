"""
Material Model
Database model for raw materials in ABC_Catalog
"""


class Material:
    """Material data model"""
    
    def __init__(self, raw_part, raw_description, raw_unit, 
                 raw_price1=0.0, raw_price2=0.0, raw_balance=0.0,
                 raw_in=0, raw_out=0, material_id=None):
        """
        Initialize Material instance
        
        Args:
            raw_part (str): Material part number (alphanumeric) - Primary key
            raw_description (str): Material description (alphanumeric) - Also searchable
            raw_unit (str): Unit of measure (e.g., gal, kilo, pieza)
            raw_price1 (float): First price
            raw_price2 (float): Second price
            raw_balance (float): Current balance/stock value
            raw_in (int): Incoming units
            raw_out (int): Outgoing units
            material_id (int): Database ID (auto-generated)
        """
        self.material_id = material_id
        self.raw_part = raw_part
        self.raw_description = raw_description
        self.raw_unit = raw_unit
        self.raw_price1 = raw_price1
        self.raw_price2 = raw_price2
        self.raw_balance = raw_balance
        self.raw_in = raw_in
        self.raw_out = raw_out
    
    def to_dict(self):
        """Convert material to dictionary"""
        return {
            'material_id': self.material_id,
            'raw_part': self.raw_part,
            'raw_description': self.raw_description,
            'raw_unit': self.raw_unit,
            'raw_price1': self.raw_price1,
            'raw_price2': self.raw_price2,
            'raw_balance': self.raw_balance,
            'raw_in': self.raw_in,
            'raw_out': self.raw_out
        }
    
    @staticmethod
    def from_dict(data):
        """Create Material instance from dictionary"""
        return Material(
            material_id=data.get('material_id'),
            raw_part=data.get('raw_part'),
            raw_description=data.get('raw_description'),
            raw_unit=data.get('raw_unit'),
            raw_price1=data.get('raw_price1', 0.0),
            raw_price2=data.get('raw_price2', 0.0),
            raw_balance=data.get('raw_balance', 0.0),
            raw_in=data.get('raw_in', 0),
            raw_out=data.get('raw_out', 0)
        )
    
    def __repr__(self):
        return f"Material(raw_part='{self.raw_part}', description='{self.raw_description}')"
