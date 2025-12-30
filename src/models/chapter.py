"""
Chapter Model
Data model for project chapters
"""

from dataclasses import dataclass


@dataclass
class Chapter:
    """Chapter model with validations and automatic truncation"""
    
    # Numeric field
    chap_number: int = 0
    
    # Alphanumeric field
    chap_description: str = ""
    
    def __post_init__(self):
        """Validate and truncate fields"""
        # Ensure chap_number is integer and within range (0-999 for 3 digits)
        try:
            self.chap_number = int(self.chap_number) if self.chap_number else 0
            if self.chap_number < 0 or self.chap_number > 999:
                self.chap_number = min(999, max(0, self.chap_number))
        except (ValueError, TypeError):
            self.chap_number = 0
        
        # Truncate description to max length
        self.chap_description = str(self.chap_description)[:30] if self.chap_description else ""
    
    def validate(self):
        """Validate required fields"""
        if self.chap_number <= 0:
            return False, "Chap.Number es obligatorio y debe ser mayor que 0"
        if not self.chap_description:
            return False, "Chap.Description es obligatorio"
        return True, ""
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'chap_number': self.chap_number,
            'chap_description': self.chap_description
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create instance from dictionary"""
        return cls(**data)
