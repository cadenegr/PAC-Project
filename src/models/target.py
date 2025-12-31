"""
Target Model
Data model for project targets/objectives
"""

from dataclasses import dataclass


@dataclass
class Target:
    """Target model with validations and automatic truncation"""
    
    # Primary key
    target_id: int = None
    
    # Alphanumeric fields
    targ_prochapter: str = ""
    targ_pronumber: str = ""
    targ_prodescription: str = ""
    targ_prounit: str = ""
    
    # Numeric fields (stored as float)
    targ_proprice1: float = 0.0
    targ_qtyproject: float = 0.0
    targ_qtydone: float = 0.0
    targ_qtyprogress: float = 0.0
    targ_qtyfinish: float = 0.0
    targ_payment: float = 0.0
    
    def __post_init__(self):
        """Truncate alphanumeric fields to max length"""
        self.targ_prochapter = str(self.targ_prochapter)[:3] if self.targ_prochapter else ""
        self.targ_pronumber = str(self.targ_pronumber)[:12] if self.targ_pronumber else ""
        self.targ_prodescription = str(self.targ_prodescription)[:30] if self.targ_prodescription else ""
        self.targ_prounit = str(self.targ_prounit)[:4] if self.targ_prounit else ""
        
        # Ensure numeric fields are float
        self.targ_proprice1 = float(self.targ_proprice1) if self.targ_proprice1 else 0.0
        self.targ_qtyproject = float(self.targ_qtyproject) if self.targ_qtyproject else 0.0
        self.targ_qtydone = float(self.targ_qtydone) if self.targ_qtydone else 0.0
        self.targ_qtyprogress = float(self.targ_qtyprogress) if self.targ_qtyprogress else 0.0
        self.targ_qtyfinish = float(self.targ_qtyfinish) if self.targ_qtyfinish else 0.0
        self.targ_payment = float(self.targ_payment) if self.targ_payment else 0.0
    
    def validate(self):
        """Validate required fields"""
        if not self.targ_pronumber:
            return False, "Targ.ProNumber es obligatorio"
        if not self.targ_prodescription:
            return False, "Targ.ProDescription es obligatorio"
        return True, ""
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'targ_prochapter': self.targ_prochapter,
            'targ_pronumber': self.targ_pronumber,
            'targ_prodescription': self.targ_prodescription,
            'targ_prounit': self.targ_prounit,
            'targ_proprice1': self.targ_proprice1,
            'targ_qtyproject': self.targ_qtyproject,
            'targ_qtydone': self.targ_qtydone,
            'targ_qtyprogress': self.targ_qtyprogress,
            'targ_qtyfinish': self.targ_qtyfinish,
            'targ_payment': self.targ_payment
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create instance from dictionary"""
        return cls(**data)
