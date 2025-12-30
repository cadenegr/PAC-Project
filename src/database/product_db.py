"""
Product Database Service
Handles all database operations for products
"""

import sqlite3
import os
from src.models.product import Product


class ProductDatabase:
    """Database service for products"""
    
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
        """Create products table if it doesn't exist"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                pro_part TEXT NOT NULL UNIQUE,
                pro_description TEXT NOT NULL,
                pro_unit TEXT NOT NULL,
                pro_price1 REAL DEFAULT 0.0,
                pro_price2 REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_product(self, product):
        """
        Create a new product
        
        Args:
            product (Product): Product instance to create
            
        Returns:
            int: Product ID if successful, None if product already exists
        """
        # Validate product
        is_valid, error_msg = product.validate()
        if not is_valid:
            print(f"Validation error: {error_msg}")
            return None
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO products (pro_part, pro_description, pro_unit, 
                                     pro_price1, pro_price2)
                VALUES (?, ?, ?, ?, ?)
            ''', (product.pro_part, product.pro_description, product.pro_unit,
                  product.pro_price1, product.pro_price2))
            
            conn.commit()
            product_id = cursor.lastrowid
            return product_id
            
        except sqlite3.IntegrityError as e:
            print(f"Product already exists: {e}")
            return None
        finally:
            conn.close()
    
    def get_product_by_part(self, pro_part):
        """
        Get product by Pro.Part
        
        Args:
            pro_part (str): Product part number
            
        Returns:
            Product: Product instance if found, None otherwise
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT product_id, pro_part, pro_description, pro_unit,
                   pro_price1, pro_price2
            FROM products
            WHERE pro_part = ?
        ''', (pro_part,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Product(
                product_id=row[0],
                pro_part=row[1],
                pro_description=row[2],
                pro_unit=row[3],
                pro_price1=row[4],
                pro_price2=row[5]
            )
        return None
    
    def search_by_description(self, description):
        """
        Search products by description (partial match)
        
        Args:
            description (str): Description to search for
            
        Returns:
            list: List of Product instances
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT product_id, pro_part, pro_description, pro_unit,
                   pro_price1, pro_price2
            FROM products
            WHERE pro_description LIKE ?
            ORDER BY pro_description
        ''', (f'%{description}%',))
        
        rows = cursor.fetchall()
        conn.close()
        
        products = []
        for row in rows:
            products.append(Product(
                product_id=row[0],
                pro_part=row[1],
                pro_description=row[2],
                pro_unit=row[3],
                pro_price1=row[4],
                pro_price2=row[5]
            ))
        
        return products
    
    def get_all_products(self):
        """
        Get all products
        
        Returns:
            list: List of all Product instances
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT product_id, pro_part, pro_description, pro_unit,
                   pro_price1, pro_price2
            FROM products
            ORDER BY pro_part
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        products = []
        for row in rows:
            products.append(Product(
                product_id=row[0],
                pro_part=row[1],
                pro_description=row[2],
                pro_unit=row[3],
                pro_price1=row[4],
                pro_price2=row[5]
            ))
        
        return products
    
    def update_product(self, product):
        """
        Update existing product
        
        Args:
            product (Product): Product instance with updated data
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate product
        is_valid, error_msg = product.validate()
        if not is_valid:
            print(f"Validation error: {error_msg}")
            return False
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE products
                SET pro_description = ?, pro_unit = ?,
                    pro_price1 = ?, pro_price2 = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE pro_part = ?
            ''', (product.pro_description, product.pro_unit,
                  product.pro_price1, product.pro_price2,
                  product.pro_part))
            
            conn.commit()
            success = cursor.rowcount > 0
            return success
            
        except sqlite3.Error as e:
            print(f"Update error: {e}")
            return False
        finally:
            conn.close()
    
    def delete_product(self, pro_part):
        """
        Delete product by Pro.Part
        
        Args:
            pro_part (str): Product part number
            
        Returns:
            bool: True if successful, False otherwise
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM products WHERE pro_part = ?', (pro_part,))
            conn.commit()
            success = cursor.rowcount > 0
            return success
            
        except sqlite3.Error as e:
            print(f"Delete error: {e}")
            return False
        finally:
            conn.close()
    
    def get_product_count(self):
        """
        Get total number of products
        
        Returns:
            int: Total product count
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM products')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
