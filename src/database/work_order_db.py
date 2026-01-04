"""
Database service for Work Orders management
"""

import sqlite3
from typing import List, Optional
from src.models.work_order import WorkOrder


class WorkOrderDB:
    """Database service for Work Order operations"""
    
    def __init__(self, db_path: str = "data/pac.db"):
        """
        Initialize the Work Order database service
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._create_table()
    
    def _create_table(self):
        """Create the work_orders table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS work_orders (
                wo_number TEXT(4) PRIMARY KEY,
                wo_date TEXT NOT NULL,
                wo_time TEXT NOT NULL,
                wo_teamnumber TEXT(4),
                wo_chapter TEXT(4),
                wo_target TEXT(4),
                wo_qty REAL,
                wo_price REAL,
                wo_done REAL,
                wo_payticket TEXT(20),
                wo_status INTEGER(1),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_all(self) -> List[WorkOrder]:
        """
        Get all work orders from the database
        
        Returns:
            List of WorkOrder objects
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT wo_number, wo_date, wo_time, wo_teamnumber, wo_chapter, wo_target,
                   wo_qty, wo_price, wo_done, wo_payticket, wo_status,
                   created_at, updated_at
            FROM work_orders
            ORDER BY wo_number
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [WorkOrder(
            wo_number=row[0],
            wo_date=row[1],
            wo_time=row[2],
            wo_teamnumber=row[3],
            wo_chapter=row[4],
            wo_target=row[5],
            wo_qty=row[6],
            wo_price=row[7],
            wo_done=row[8],
            wo_payticket=row[9],
            wo_status=row[10],
            created_at=row[11],
            updated_at=row[12]
        ) for row in rows]
    
    def get_by_number(self, wo_number: str) -> Optional[WorkOrder]:
        """
        Get a work order by its number
        
        Args:
            wo_number: Work order number
            
        Returns:
            WorkOrder object if found, None otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT wo_number, wo_date, wo_time, wo_teamnumber, wo_chapter, wo_target,
                   wo_qty, wo_price, wo_done, wo_payticket, wo_status,
                   created_at, updated_at
            FROM work_orders
            WHERE wo_number = ?
        """, (wo_number,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return WorkOrder(
                wo_number=row[0],
                wo_date=row[1],
                wo_time=row[2],
                wo_teamnumber=row[3],
                wo_chapter=row[4],
                wo_target=row[5],
                wo_qty=row[6],
                wo_price=row[7],
                wo_done=row[8],
                wo_payticket=row[9],
                wo_status=row[10],
                created_at=row[11],
                updated_at=row[12]
            )
        return None
    
    def create(self, work_order: WorkOrder) -> bool:
        """
        Create a new work order
        
        Args:
            work_order: WorkOrder object to create
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO work_orders (
                    wo_number, wo_date, wo_time, wo_teamnumber, wo_chapter, wo_target,
                    wo_qty, wo_price, wo_done, wo_payticket, wo_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                work_order.wo_number,
                work_order.wo_date,
                work_order.wo_time,
                work_order.wo_teamnumber,
                work_order.wo_chapter,
                work_order.wo_target,
                work_order.wo_qty,
                work_order.wo_price,
                work_order.wo_done,
                work_order.wo_payticket,
                work_order.wo_status
            ))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update(self, work_order: WorkOrder) -> bool:
        """
        Update an existing work order
        
        Args:
            work_order: WorkOrder object with updated data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE work_orders
                SET wo_date = ?,
                    wo_time = ?,
                    wo_teamnumber = ?,
                    wo_chapter = ?,
                    wo_target = ?,
                    wo_qty = ?,
                    wo_price = ?,
                    wo_done = ?,
                    wo_payticket = ?,
                    wo_status = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE wo_number = ?
            """, (
                work_order.wo_date,
                work_order.wo_time,
                work_order.wo_teamnumber,
                work_order.wo_chapter,
                work_order.wo_target,
                work_order.wo_qty,
                work_order.wo_price,
                work_order.wo_done,
                work_order.wo_payticket,
                work_order.wo_status,
                work_order.wo_number
            ))
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except sqlite3.Error:
            return False
    
    def delete(self, wo_number: str) -> bool:
        """
        Delete a work order by its number
        
        Args:
            wo_number: Work order number to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM work_orders WHERE wo_number = ?", (wo_number,))
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except sqlite3.Error:
            return False
    
    def search(self, search_term: str) -> List[WorkOrder]:
        """
        Search work orders by number, team, or target
        
        Args:
            search_term: Term to search for
            
        Returns:
            List of matching WorkOrder objects
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT wo_number, wo_date, wo_time, wo_teamnumber, wo_chapter, wo_target,
                   wo_qty, wo_price, wo_done, wo_payticket, wo_status,
                   created_at, updated_at
            FROM work_orders
            WHERE wo_number LIKE ? 
               OR wo_teamnumber LIKE ? 
               OR wo_chapter LIKE ?
               OR wo_target LIKE ?
               OR wo_payticket LIKE ?
            ORDER BY wo_number
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [WorkOrder(
            wo_number=row[0],
            wo_date=row[1],
            wo_time=row[2],
            wo_teamnumber=row[3],
            wo_chapter=row[4],
            wo_target=row[5],
            wo_qty=row[6],
            wo_price=row[7],
            wo_done=row[8],
            wo_payticket=row[9],
            wo_status=row[10],
            created_at=row[11],
            updated_at=row[12]
        ) for row in rows]
