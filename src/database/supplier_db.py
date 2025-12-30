"""
Supplier Database Service
Handles all database operations for suppliers
"""

import sqlite3
import os
from src.models.supplier import Supplier


class SupplierDatabase:
    """Database service for suppliers"""
    
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
        """Create suppliers table if it doesn't exist"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sup_number TEXT NOT NULL UNIQUE,
                sup_name TEXT NOT NULL,
                sup_address TEXT DEFAULT '',
                sup_phone1 TEXT DEFAULT '',
                sup_phone2 TEXT DEFAULT '',
                sup_email TEXT DEFAULT '',
                sup_paymethod TEXT DEFAULT '',
                sup_username TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_supplier(self, supplier):
        """
        Create a new supplier
        
        Args:
            supplier (Supplier): Supplier instance to create
            
        Returns:
            int: Supplier ID if successful, None if supplier already exists
        """
        # Validate supplier
        is_valid, error_msg = supplier.validate()
        if not is_valid:
            print(f"Validation error: {error_msg}")
            return None
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO suppliers (sup_number, sup_name, sup_address, 
                                      sup_phone1, sup_phone2, sup_email,
                                      sup_paymethod, sup_username)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (supplier.sup_number, supplier.sup_name, supplier.sup_address,
                  supplier.sup_phone1, supplier.sup_phone2, supplier.sup_email,
                  supplier.sup_paymethod, supplier.sup_username))
            
            conn.commit()
            supplier_id = cursor.lastrowid
            return supplier_id
            
        except sqlite3.IntegrityError as e:
            print(f"Supplier already exists: {e}")
            return None
        finally:
            conn.close()
    
    def get_supplier_by_number(self, sup_number):
        """
        Get supplier by Sup.Number
        
        Args:
            sup_number (str): Supplier number
            
        Returns:
            Supplier: Supplier instance if found, None otherwise
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT supplier_id, sup_number, sup_name, sup_address,
                   sup_phone1, sup_phone2, sup_email, sup_paymethod, sup_username
            FROM suppliers
            WHERE sup_number = ?
        ''', (sup_number,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Supplier(
                supplier_id=row[0],
                sup_number=row[1],
                sup_name=row[2],
                sup_address=row[3],
                sup_phone1=row[4],
                sup_phone2=row[5],
                sup_email=row[6],
                sup_paymethod=row[7],
                sup_username=row[8]
            )
        return None
    
    def search_by_name(self, name):
        """
        Search suppliers by name (partial match)
        
        Args:
            name (str): Name to search for
            
        Returns:
            list: List of Supplier instances
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT supplier_id, sup_number, sup_name, sup_address,
                   sup_phone1, sup_phone2, sup_email, sup_paymethod, sup_username
            FROM suppliers
            WHERE sup_name LIKE ?
            ORDER BY sup_name
        ''', (f'%{name}%',))
        
        rows = cursor.fetchall()
        conn.close()
        
        suppliers = []
        for row in rows:
            suppliers.append(Supplier(
                supplier_id=row[0],
                sup_number=row[1],
                sup_name=row[2],
                sup_address=row[3],
                sup_phone1=row[4],
                sup_phone2=row[5],
                sup_email=row[6],
                sup_paymethod=row[7],
                sup_username=row[8]
            ))
        
        return suppliers
    
    def get_all_suppliers(self):
        """
        Get all suppliers
        
        Returns:
            list: List of all Supplier instances
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT supplier_id, sup_number, sup_name, sup_address,
                   sup_phone1, sup_phone2, sup_email, sup_paymethod, sup_username
            FROM suppliers
            ORDER BY sup_number
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        suppliers = []
        for row in rows:
            suppliers.append(Supplier(
                supplier_id=row[0],
                sup_number=row[1],
                sup_name=row[2],
                sup_address=row[3],
                sup_phone1=row[4],
                sup_phone2=row[5],
                sup_email=row[6],
                sup_paymethod=row[7],
                sup_username=row[8]
            ))
        
        return suppliers
    
    def update_supplier(self, supplier):
        """
        Update existing supplier
        
        Args:
            supplier (Supplier): Supplier instance with updated data
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate supplier
        is_valid, error_msg = supplier.validate()
        if not is_valid:
            print(f"Validation error: {error_msg}")
            return False
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE suppliers
                SET sup_name = ?, sup_address = ?, sup_phone1 = ?,
                    sup_phone2 = ?, sup_email = ?, sup_paymethod = ?,
                    sup_username = ?, updated_at = CURRENT_TIMESTAMP
                WHERE sup_number = ?
            ''', (supplier.sup_name, supplier.sup_address, supplier.sup_phone1,
                  supplier.sup_phone2, supplier.sup_email, supplier.sup_paymethod,
                  supplier.sup_username, supplier.sup_number))
            
            conn.commit()
            success = cursor.rowcount > 0
            return success
            
        except sqlite3.Error as e:
            print(f"Update error: {e}")
            return False
        finally:
            conn.close()
    
    def delete_supplier(self, sup_number):
        """
        Delete supplier by Sup.Number
        
        Args:
            sup_number (str): Supplier number
            
        Returns:
            bool: True if successful, False otherwise
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM suppliers WHERE sup_number = ?', (sup_number,))
            conn.commit()
            success = cursor.rowcount > 0
            return success
            
        except sqlite3.Error as e:
            print(f"Delete error: {e}")
            return False
        finally:
            conn.close()
    
    def get_supplier_count(self):
        """
        Get total number of suppliers
        
        Returns:
            int: Total supplier count
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM suppliers')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
