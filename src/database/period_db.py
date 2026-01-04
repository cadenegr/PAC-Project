"""
Database service for Period management
"""

import sqlite3
from typing import List, Optional
from datetime import datetime
from src.models.period import Period


class PeriodDB:
    """Database service for Period operations"""
    
    def __init__(self, db_path: str = "data/pac.db"):
        """
        Initialize the Period database service
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._create_table()
    
    def _create_table(self):
        """Create the periods table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS periods (
                per_number INTEGER PRIMARY KEY,
                per_date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_all(self) -> List[Period]:
        """
        Get all periods from the database
        
        Returns:
            List of Period objects
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT per_number, per_date, created_at, updated_at
            FROM periods
            ORDER BY per_number
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Period(
            per_number=row[0],
            per_date=row[1],
            created_at=row[2],
            updated_at=row[3]
        ) for row in rows]
    
    def get_by_number(self, per_number: int) -> Optional[Period]:
        """
        Get a period by its number
        
        Args:
            per_number: Period number
            
        Returns:
            Period object if found, None otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT per_number, per_date, created_at, updated_at
            FROM periods
            WHERE per_number = ?
        """, (per_number,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Period(
                per_number=row[0],
                per_date=row[1],
                created_at=row[2],
                updated_at=row[3]
            )
        return None
    
    def create(self, period: Period) -> bool:
        """
        Create a new period
        
        Args:
            period: Period object to create
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO periods (per_number, per_date)
                VALUES (?, ?)
            """, (period.per_number, period.per_date))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update(self, period: Period) -> bool:
        """
        Update an existing period
        
        Args:
            period: Period object with updated data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE periods
                SET per_date = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE per_number = ?
            """, (period.per_date, period.per_number))
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except sqlite3.Error:
            return False
    
    def delete(self, per_number: int) -> bool:
        """
        Delete a period by its number
        
        Args:
            per_number: Period number to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM periods WHERE per_number = ?", (per_number,))
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except sqlite3.Error:
            return False
    
    def search(self, search_term: str) -> List[Period]:
        """
        Search periods by number or date
        
        Args:
            search_term: Term to search for
            
        Returns:
            List of matching Period objects
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT per_number, per_date, created_at, updated_at
            FROM periods
            WHERE CAST(per_number AS TEXT) LIKE ? OR per_date LIKE ?
            ORDER BY per_number
        """, (f"%{search_term}%", f"%{search_term}%"))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Period(
            per_number=row[0],
            per_date=row[1],
            created_at=row[2],
            updated_at=row[3]
        ) for row in rows]
