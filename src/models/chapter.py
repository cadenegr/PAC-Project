"""
Chapter Model
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Chapter:
    """Chapter data model"""
    chap_number: str  # TEXT(4)
    chap_description: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def __post_init__(self):
        """Validate and normalize fields"""
        # Normalize chap_number to 4 characters
        self.chap_number = str(self.chap_number).strip()
        
        if len(self.chap_number) > 4:
            # Truncate to first 4 characters
            self.chap_number = self.chap_number[:4]
        elif len(self.chap_number) < 4 and self.chap_number.isdigit():
            # Pad with zeros if numeric
            self.chap_number = self.chap_number.zfill(4)
        
        # Ensure description is string
        self.chap_description = str(self.chap_description).strip()
