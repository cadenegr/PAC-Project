"""
Supplier Model
Database model for suppliers in ABC_Catalog
"""


class Supplier:
    """Supplier data model"""
    
    def __init__(self, sup_number, sup_name, sup_address="", 
                 sup_phone1="", sup_phone2="", sup_email="", 
                 sup_paymethod="", sup_username="", supplier_id=None):
        """
        Initialize Supplier instance
        
        Args:
            sup_number (str): Supplier number (alphanumeric, max 12 chars) - Primary key
            sup_name (str): Supplier name (alphanumeric, max 30 chars)
            sup_address (str): Supplier address (alphanumeric, max 30 chars)
            sup_phone1 (str): Primary phone (alphanumeric, max 12 chars)
            sup_phone2 (str): Secondary phone (alphanumeric, max 12 chars)
            sup_email (str): Email address (alphanumeric, max 30 chars)
            sup_paymethod (str): Payment method (alphanumeric, max 20 chars)
            sup_username (str): Username (alphanumeric, max 20 chars)
            supplier_id (int): Database ID (auto-generated)
        """
        self.supplier_id = supplier_id
        self.sup_number = sup_number[:12] if sup_number else ""  # Limit to 12 chars
        self.sup_name = sup_name[:30] if sup_name else ""  # Limit to 30 chars
        self.sup_address = sup_address[:30] if sup_address else ""  # Limit to 30 chars
        self.sup_phone1 = sup_phone1[:12] if sup_phone1 else ""  # Limit to 12 chars
        self.sup_phone2 = sup_phone2[:12] if sup_phone2 else ""  # Limit to 12 chars
        self.sup_email = sup_email[:30] if sup_email else ""  # Limit to 30 chars
        self.sup_paymethod = sup_paymethod[:20] if sup_paymethod else ""  # Limit to 20 chars
        self.sup_username = sup_username[:20] if sup_username else ""  # Limit to 20 chars
    
    def __repr__(self):
        return f"Supplier({self.sup_number}, {self.sup_name})"
    
    def to_dict(self):
        """Convert supplier to dictionary"""
        return {
            'supplier_id': self.supplier_id,
            'sup_number': self.sup_number,
            'sup_name': self.sup_name,
            'sup_address': self.sup_address,
            'sup_phone1': self.sup_phone1,
            'sup_phone2': self.sup_phone2,
            'sup_email': self.sup_email,
            'sup_paymethod': self.sup_paymethod,
            'sup_username': self.sup_username
        }
    
    @staticmethod
    def from_dict(data):
        """Create Supplier instance from dictionary"""
        return Supplier(
            sup_number=data.get('sup_number'),
            sup_name=data.get('sup_name'),
            sup_address=data.get('sup_address', ''),
            sup_phone1=data.get('sup_phone1', ''),
            sup_phone2=data.get('sup_phone2', ''),
            sup_email=data.get('sup_email', ''),
            sup_paymethod=data.get('sup_paymethod', ''),
            sup_username=data.get('sup_username', ''),
            supplier_id=data.get('supplier_id')
        )
    
    def validate(self):
        """
        Validate supplier data
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not self.sup_number or len(self.sup_number.strip()) == 0:
            return False, "Sup.Number es requerido"
        
        if len(self.sup_number) > 12:
            return False, "Sup.Number no puede exceder 12 caracteres"
        
        if not self.sup_name or len(self.sup_name.strip()) == 0:
            return False, "Sup.Name es requerido"
        
        if len(self.sup_name) > 30:
            return False, "Sup.Name no puede exceder 30 caracteres"
        
        if len(self.sup_address) > 30:
            return False, "Sup.Address no puede exceder 30 caracteres"
        
        if len(self.sup_phone1) > 12:
            return False, "Sup.Phone1 no puede exceder 12 caracteres"
        
        if len(self.sup_phone2) > 12:
            return False, "Sup.Phone2 no puede exceder 12 caracteres"
        
        if len(self.sup_email) > 30:
            return False, "Sup.Email no puede exceder 30 caracteres"
        
        if len(self.sup_paymethod) > 20:
            return False, "Sup.PayMethod no puede exceder 20 caracteres"
        
        if len(self.sup_username) > 20:
            return False, "Sup.UserName no puede exceder 20 caracteres"
        
        return True, ""
