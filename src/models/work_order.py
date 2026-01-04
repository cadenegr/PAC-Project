"""
Work Order data model
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class WorkOrder:
    """Work Order data model"""
    wo_number: str  # TEXT(4)
    wo_date: str
    wo_time: str
    wo_teamnumber: Optional[str] = None  # TEXT(4)
    wo_chapter: Optional[str] = None  # TEXT(4)
    wo_target: Optional[str] = None  # TEXT(4)
    wo_qty: Optional[float] = None  # NUMERIC(9)
    wo_price: Optional[float] = None  # NUMERIC(9)
    wo_done: Optional[float] = None  # NUMERIC(9)
    wo_payticket: Optional[str] = None  # TEXT(20)
    wo_status: Optional[int] = None  # NUMERIC(1)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def __post_init__(self):
        """Validate work order data after initialization"""
        # Validate wo_number length
        if self.wo_number and len(self.wo_number) > 4:
            raise ValueError("wo_number must be 4 characters or less")
        # Validate wo_teamnumber length
        if self.wo_teamnumber and len(self.wo_teamnumber) > 4:
            raise ValueError("wo_teamnumber must be 4 characters or less")
        
        # Validate wo_chapter length
        if self.wo_chapter and len(self.wo_chapter) > 4:
            raise ValueError("wo_chapter must be 4 characters or less")
        
        # Validate wo_target length
        if self.wo_target and len(self.wo_target) > 4:
            raise ValueError("wo_target must be 4 characters or less")
            raise ValueError("wo_target must be 4 characters or less")
        
        # Validate wo_payticket length
        if self.wo_payticket and len(self.wo_payticket) > 20:
            raise ValueError("wo_payticket must be 20 characters or less")
        
        # Validate wo_status is 0 or 1
        if self.wo_status is not None and self.wo_status not in [0, 1]:
            raise ValueError("wo_status must be 0 or 1")
        
        # Convert numeric fields to float if they're not None
        if self.wo_qty is not None and not isinstance(self.wo_qty, (int, float)):
            try:
                self.wo_qty = float(self.wo_qty)
            except (ValueError, TypeError):
                raise ValueError("wo_qty must be numeric")
        
        if self.wo_price is not None and not isinstance(self.wo_price, (int, float)):
            try:
                self.wo_price = float(self.wo_price)
            except (ValueError, TypeError):
                raise ValueError("wo_price must be numeric")
        
        if self.wo_done is not None and not isinstance(self.wo_done, (int, float)):
            try:
                self.wo_done = float(self.wo_done)
            except (ValueError, TypeError):
                raise ValueError("wo_done must be numeric")
