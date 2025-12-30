"""
Chapter Database Service
CRUD operations for chapters
"""

import sqlite3
from typing import List, Optional
from src.models.chapter import Chapter


class ChapterDatabase:
    """Database service for Chapter operations"""
    
    def __init__(self, db_path: str = 'data/pac.db'):
        self.db_path = db_path
        self._create_table()
    
    def _create_table(self):
        """Create chapters table if not exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chapters (
                chapter_id INTEGER PRIMARY KEY AUTOINCREMENT,
                chap_number INTEGER NOT NULL UNIQUE,
                chap_description TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_chapter(self, chapter: Chapter) -> Optional[int]:
        """
        Create new chapter
        Returns: chapter_id if successful, None if duplicate
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO chapters (chap_number, chap_description)
                VALUES (?, ?)
            ''', (chapter.chap_number, chapter.chap_description))
            
            chapter_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return chapter_id
            
        except sqlite3.IntegrityError:
            return None
    
    def get_chapter_by_number(self, chap_number: int) -> Optional[Chapter]:
        """Get chapter by number (primary key)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT chap_number, chap_description
            FROM chapters
            WHERE chap_number = ?
        ''', (chap_number,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Chapter(
                chap_number=row[0],
                chap_description=row[1]
            )
        return None
    
    def search_by_description(self, description: str) -> List[Chapter]:
        """Search chapters by description (partial match)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT chap_number, chap_description
            FROM chapters
            WHERE chap_description LIKE ?
            ORDER BY chap_number
        ''', (f'%{description}%',))
        
        rows = cursor.fetchall()
        conn.close()
        
        chapters = []
        for row in rows:
            chapters.append(Chapter(
                chap_number=row[0],
                chap_description=row[1]
            ))
        return chapters
    
    def get_all_chapters(self) -> List[Chapter]:
        """Get all chapters ordered by number"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT chap_number, chap_description
            FROM chapters
            ORDER BY chap_number
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        chapters = []
        for row in rows:
            chapters.append(Chapter(
                chap_number=row[0],
                chap_description=row[1]
            ))
        return chapters
    
    def update_chapter(self, chapter: Chapter) -> bool:
        """Update existing chapter"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE chapters
                SET chap_description = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE chap_number = ?
            ''', (chapter.chap_description, chapter.chap_number))
            
            success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return success
            
        except Exception:
            return False
    
    def delete_chapter(self, chap_number: int) -> bool:
        """Delete chapter by number"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM chapters WHERE chap_number = ?', (chap_number,))
            
            success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return success
            
        except Exception:
            return False
