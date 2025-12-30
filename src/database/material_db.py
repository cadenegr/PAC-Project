"""
Material Database Service
Handles all database operations for materials
"""

import sqlite3
import os
from src.models.material import Material


class MaterialDatabase:
    """Database service for materials"""
    
    def __init__(self, db_path='data/pac.db'):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        # Create data directory if it doesn't exist
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        self.db_path = db_path
        self._create_table()
    
    def _get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def _create_table(self):
        """Create materials table if it doesn't exist"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materials (
                material_id INTEGER PRIMARY KEY AUTOINCREMENT,
                raw_part TEXT NOT NULL UNIQUE,
                raw_description TEXT NOT NULL,
                raw_unit TEXT NOT NULL,
                raw_price1 REAL DEFAULT 0.0,
                raw_price2 REAL DEFAULT 0.0,
                raw_balance REAL DEFAULT 0.0,
                raw_in INTEGER DEFAULT 0,
                raw_out INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for faster searches
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_raw_part 
            ON materials(raw_part)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_raw_description 
            ON materials(raw_description)
        ''')
        
        conn.commit()
        conn.close()
    
    def create_material(self, material):
        """
        Create a new material
        
        Args:
            material: Material object
            
        Returns:
            int: ID of created material or None if error
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO materials (
                    raw_part, raw_description, raw_unit,
                    raw_price1, raw_price2, raw_balance,
                    raw_in, raw_out
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                material.raw_part,
                material.raw_description,
                material.raw_unit,
                material.raw_price1,
                material.raw_price2,
                material.raw_balance,
                material.raw_in,
                material.raw_out
            ))
            
            material_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return material_id
        except sqlite3.IntegrityError:
            # Raw_part already exists
            return None
        except Exception as e:
            print(f"Error creating material: {e}")
            return None
    
    def get_material_by_part(self, raw_part):
        """
        Get material by part number
        
        Args:
            raw_part: Material part number
            
        Returns:
            Material object or None
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT material_id, raw_part, raw_description, raw_unit,
                   raw_price1, raw_price2, raw_balance, raw_in, raw_out
            FROM materials
            WHERE raw_part = ?
        ''', (raw_part,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Material(
                material_id=row[0],
                raw_part=row[1],
                raw_description=row[2],
                raw_unit=row[3],
                raw_price1=row[4],
                raw_price2=row[5],
                raw_balance=row[6],
                raw_in=row[7],
                raw_out=row[8]
            )
        return None
    
    def search_by_description(self, description):
        """
        Search materials by description
        
        Args:
            description: Search term for description
            
        Returns:
            List of Material objects
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT material_id, raw_part, raw_description, raw_unit,
                   raw_price1, raw_price2, raw_balance, raw_in, raw_out
            FROM materials
            WHERE raw_description LIKE ?
            ORDER BY raw_description
        ''', (f'%{description}%',))
        
        rows = cursor.fetchall()
        conn.close()
        
        materials = []
        for row in rows:
            materials.append(Material(
                material_id=row[0],
                raw_part=row[1],
                raw_description=row[2],
                raw_unit=row[3],
                raw_price1=row[4],
                raw_price2=row[5],
                raw_balance=row[6],
                raw_in=row[7],
                raw_out=row[8]
            ))
        
        return materials
    
    def get_all_materials(self):
        """
        Get all materials
        
        Returns:
            List of Material objects
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT material_id, raw_part, raw_description, raw_unit,
                   raw_price1, raw_price2, raw_balance, raw_in, raw_out
            FROM materials
            ORDER BY raw_part
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        materials = []
        for row in rows:
            materials.append(Material(
                material_id=row[0],
                raw_part=row[1],
                raw_description=row[2],
                raw_unit=row[3],
                raw_price1=row[4],
                raw_price2=row[5],
                raw_balance=row[6],
                raw_in=row[7],
                raw_out=row[8]
            ))
        
        return materials
    
    def update_material(self, material):
        """
        Update an existing material
        
        Args:
            material: Material object with updated data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE materials
                SET raw_description = ?,
                    raw_unit = ?,
                    raw_price1 = ?,
                    raw_price2 = ?,
                    raw_balance = ?,
                    raw_in = ?,
                    raw_out = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE raw_part = ?
            ''', (
                material.raw_description,
                material.raw_unit,
                material.raw_price1,
                material.raw_price2,
                material.raw_balance,
                material.raw_in,
                material.raw_out,
                material.raw_part
            ))
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            
            return success
        except Exception as e:
            print(f"Error updating material: {e}")
            return False
    
    def delete_material(self, raw_part):
        """
        Delete a material
        
        Args:
            raw_part: Material part number
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM materials WHERE raw_part = ?', (raw_part,))
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            
            return success
        except Exception as e:
            print(f"Error deleting material: {e}")
            return False
