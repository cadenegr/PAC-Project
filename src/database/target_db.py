"""
Target Database Service
CRUD operations for targets
"""

import sqlite3
from typing import List, Optional
from src.models.target import Target


class TargetDatabase:
    """Database service for Target operations"""
    
    def __init__(self, db_path: str = 'data/pac.db'):
        self.db_path = db_path
        self._create_table()
    
    def _create_table(self):
        """Create targets table if not exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if table exists with old schema
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='targets'")
        result = cursor.fetchone()
        
        if result and 'UNIQUE' in result[0]:
            # Backup existing data
            cursor.execute("SELECT * FROM targets")
            backup_data = cursor.fetchall()
            
            # Drop old table
            cursor.execute("DROP TABLE targets")
            
            # Create new table without UNIQUE constraint
            cursor.execute('''
                CREATE TABLE targets (
                    target_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    targ_prochapter TEXT DEFAULT '',
                    targ_pronumber TEXT NOT NULL,
                    targ_prodescription TEXT DEFAULT '',
                    targ_prounit TEXT DEFAULT '',
                    targ_proprice1 REAL DEFAULT 0.0,
                    targ_qtyproject REAL DEFAULT 0.0,
                    targ_qtydone REAL DEFAULT 0.0,
                    targ_qtyprogress REAL DEFAULT 0.0,
                    targ_qtyfinish REAL DEFAULT 0.0,
                    targ_payment REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(targ_prochapter, targ_pronumber)
                )
            ''')
            
            # Restore data if any
            if backup_data:
                for row in backup_data:
                    cursor.execute('''
                        INSERT INTO targets (
                            target_id, targ_prochapter, targ_pronumber, targ_prodescription,
                            targ_prounit, targ_proprice1, targ_qtyproject, targ_qtydone,
                            targ_qtyprogress, targ_qtyfinish, targ_payment, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', row)
        else:
            # Create new table with composite unique constraint
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS targets (
                    target_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    targ_prochapter TEXT DEFAULT '',
                    targ_pronumber TEXT NOT NULL,
                    targ_prodescription TEXT DEFAULT '',
                    targ_prounit TEXT DEFAULT '',
                    targ_proprice1 REAL DEFAULT 0.0,
                    targ_qtyproject REAL DEFAULT 0.0,
                    targ_qtydone REAL DEFAULT 0.0,
                    targ_qtyprogress REAL DEFAULT 0.0,
                    targ_qtyfinish REAL DEFAULT 0.0,
                    targ_payment REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(targ_prochapter, targ_pronumber)
                )
            ''')
        
        conn.commit()
        conn.close()
    
    def create_target(self, target: Target) -> Optional[int]:
        """
        Create new target
        Returns: target_id if successful, None if duplicate
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO targets (
                    targ_prochapter, targ_pronumber, targ_prodescription, targ_prounit,
                    targ_proprice1, targ_qtyproject, targ_qtydone, targ_qtyprogress,
                    targ_qtyfinish, targ_payment
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                target.targ_prochapter,
                target.targ_pronumber,
                target.targ_prodescription,
                target.targ_prounit,
                target.targ_proprice1,
                target.targ_qtyproject,
                target.targ_qtydone,
                target.targ_qtyprogress,
                target.targ_qtyfinish,
                target.targ_payment
            ))
            
            target_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return target_id
            
        except sqlite3.IntegrityError:
            return None
    
    def get_target_by_number(self, targ_pronumber: str) -> Optional[Target]:
        """Get target by ProNumber (primary key)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT targ_prochapter, targ_pronumber, targ_prodescription, targ_prounit,
                   targ_proprice1, targ_qtyproject, targ_qtydone, targ_qtyprogress,
                   targ_qtyfinish, targ_payment
            FROM targets
            WHERE targ_pronumber = ?
        ''', (targ_pronumber,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Target(
                targ_prochapter=row[0],
                targ_pronumber=row[1],
                targ_prodescription=row[2],
                targ_prounit=row[3],
                targ_proprice1=row[4],
                targ_qtyproject=row[5],
                targ_qtydone=row[6],
                targ_qtyprogress=row[7],
                targ_qtyfinish=row[8],
                targ_payment=row[9]
            )
        return None
    
    def search_by_description(self, description: str) -> List[Target]:
        """Search targets by description (partial match)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT targ_prochapter, targ_pronumber, targ_prodescription, targ_prounit,
                   targ_proprice1, targ_qtyproject, targ_qtydone, targ_qtyprogress,
                   targ_qtyfinish, targ_payment
            FROM targets
            WHERE targ_prodescription LIKE ?
            ORDER BY targ_pronumber
        ''', (f'%{description}%',))
        
        rows = cursor.fetchall()
        conn.close()
        
        targets = []
        for row in rows:
            targets.append(Target(
                targ_prochapter=row[0],
                targ_pronumber=row[1],
                targ_prodescription=row[2],
                targ_prounit=row[3],
                targ_proprice1=row[4],
                targ_qtyproject=row[5],
                targ_qtydone=row[6],
                targ_qtyprogress=row[7],
                targ_qtyfinish=row[8],
                targ_payment=row[9]
            ))
        return targets
    
    def get_all_targets(self) -> List[Target]:
        """Get all targets ordered by Chapter (numeric) then ProNumber"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT targ_prochapter, targ_pronumber, targ_prodescription, targ_prounit,
                   targ_proprice1, targ_qtyproject, targ_qtydone, targ_qtyprogress,
                   targ_qtyfinish, targ_payment
            FROM targets
            ORDER BY CAST(targ_prochapter AS INTEGER), targ_pronumber
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        targets = []
        for row in rows:
            targets.append(Target(
                targ_prochapter=row[0],
                targ_pronumber=row[1],
                targ_prodescription=row[2],
                targ_prounit=row[3],
                targ_proprice1=row[4],
                targ_qtyproject=row[5],
                targ_qtydone=row[6],
                targ_qtyprogress=row[7],
                targ_qtyfinish=row[8],
                targ_payment=row[9]
            ))
        return targets
    
    def update_target(self, target: Target) -> bool:
        """Update existing target using composite key (chapter + pronumber)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE targets
                SET targ_prodescription = ?,
                    targ_prounit = ?,
                    targ_proprice1 = ?,
                    targ_qtyproject = ?,
                    targ_qtydone = ?,
                    targ_qtyprogress = ?,
                    targ_qtyfinish = ?,
                    targ_payment = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE targ_prochapter = ? AND targ_pronumber = ?
            ''', (
                target.targ_prodescription,
                target.targ_prounit,
                target.targ_proprice1,
                target.targ_qtyproject,
                target.targ_qtydone,
                target.targ_qtyprogress,
                target.targ_qtyfinish,
                target.targ_payment,
                target.targ_prochapter,
                target.targ_pronumber
            ))
            
            success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return success
            
        except Exception:
            return False
    
    def delete_target(self, targ_prochapter: str, targ_pronumber: str) -> bool:
        """Delete target by composite key (chapter + pronumber)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM targets WHERE targ_prochapter = ? AND targ_pronumber = ?', 
                          (targ_prochapter, targ_pronumber))
            
            success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return success
            
        except Exception:
            return False
