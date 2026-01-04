"""
Chapter Database Service
"""

import sqlite3
from typing import List, Optional
from src.models.chapter import Chapter


class ChapterDB:
    """Database service for Chapter operations"""
    
    def __init__(self, db_path: str = 'data/pac.db'):
        self.db_path = db_path
        self._create_table()
    
    def _create_table(self):
        """Create chapters table if not exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chapters (
                chap_number TEXT(4) PRIMARY KEY,
                chap_description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_all(self) -> List[Chapter]:
        """Get all chapters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT chap_number, chap_description, created_at, updated_at
            FROM chapters
            ORDER BY chap_number
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Chapter(
            chap_number=row[0],
            chap_description=row[1],
            created_at=row[2],
            updated_at=row[3]
        ) for row in rows]
    
    def get_by_number(self, chap_number: str) -> Optional[Chapter]:
        """Get chapter by number"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT chap_number, chap_description, created_at, updated_at
            FROM chapters
            WHERE chap_number = ?
        """, (chap_number,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Chapter(
                chap_number=row[0],
                chap_description=row[1],
                created_at=row[2],
                updated_at=row[3]
            )
        return None
    
    def create(self, chapter: Chapter) -> bool:
        """Create a new chapter"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO chapters (chap_number, chap_description)
                VALUES (?, ?)
            """, (chapter.chap_number, chapter.chap_description))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update(self, chapter: Chapter) -> bool:
        """Update existing chapter"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE chapters
                SET chap_description = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE chap_number = ?
            """, (chapter.chap_description, chapter.chap_number))
            
            success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return success
        except sqlite3.Error:
            return False
    
    def delete(self, chap_number: str) -> bool:
        """Delete chapter by number"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM chapters WHERE chap_number = ?", (chap_number,))
            
            success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return success
        except sqlite3.Error:
            return False
    
    def search(self, search_term: str) -> List[Chapter]:
        """Search chapters by number or description"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT chap_number, chap_description, created_at, updated_at
            FROM chapters
            WHERE chap_number LIKE ? OR chap_description LIKE ?
            ORDER BY chap_number
        """, (f"%{search_term}%", f"%{search_term}%"))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [Chapter(
            chap_number=row[0],
            chap_description=row[1],
            created_at=row[2],
            updated_at=row[3]
        ) for row in rows]
