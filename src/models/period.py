"""
Period data model
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Period:
    """Period data model"""
    per_number: int
    per_date: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def __post_init__(self):
        """Validate period data after initialization"""
        if self.per_number is not None and not isinstance(self.per_number, int):
            try:
                self.per_number = int(self.per_number)
            except (ValueError, TypeError):
                raise ValueError("per_number must be an integer")
