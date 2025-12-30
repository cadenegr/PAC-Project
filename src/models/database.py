"""
Database models for PAC Application
"""

import sqlite3
import os
from datetime import datetime


class Database:
    """Database handler for PAC Application"""
    
    def __init__(self, db_path="data/pac.db"):
        """
        Initialize database connection
        
        Args:
            db_path: Path to the database file
        """
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Establish database connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    def _create_tables(self):
        """Create all database tables"""
        self._create_teams_table()
    
    def _create_teams_table(self):
        """Create teams work table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams_work (
                team_number INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT NOT NULL,
                team_phone_1 TEXT,
                team_phone_2 TEXT,
                team_email TEXT,
                team_wassup TEXT,
                team_address TEXT,
                team_pay_method TEXT,
                team_username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()


class Team:
    """Team model for database operations"""
    
    def __init__(self, db):
        """
        Initialize Team model
        
        Args:
            db: Database instance
        """
        self.db = db
    
    def create(self, team_data):
        """
        Create a new team
        
        Args:
            team_data: Dictionary with team information
            
        Returns:
            team_number of created team or None if error
        """
        try:
            query = '''
                INSERT INTO teams_work (
                    team_name, team_phone_1, team_phone_2, team_email,
                    team_wassup, team_address, team_pay_method, team_username
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            self.db.cursor.execute(query, (
                team_data.get('team_name'),
                team_data.get('team_phone_1', ''),
                team_data.get('team_phone_2', ''),
                team_data.get('team_email', ''),
                team_data.get('team_wassup', ''),
                team_data.get('team_address', ''),
                team_data.get('team_pay_method', ''),
                team_data.get('team_username', '')
            ))
            
            self.db.connection.commit()
            return self.db.cursor.lastrowid
        except Exception as e:
            print(f"Error creating team: {e}")
            return None
    
    def get_all(self):
        """
        Get all teams
        
        Returns:
            List of teams as dictionaries
        """
        try:
            self.db.cursor.execute('SELECT * FROM teams_work ORDER BY team_number')
            rows = self.db.cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error getting teams: {e}")
            return []
    
    def get_by_number(self, team_number):
        """
        Get team by number
        
        Args:
            team_number: Team number to search
            
        Returns:
            Team dictionary or None
        """
        try:
            self.db.cursor.execute(
                'SELECT * FROM teams_work WHERE team_number = ?',
                (team_number,)
            )
            row = self.db.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error getting team: {e}")
            return None
    
    def update(self, team_number, team_data):
        """
        Update a team
        
        Args:
            team_number: Team number to update
            team_data: Dictionary with updated team information
            
        Returns:
            True if successful, False otherwise
        """
        try:
            query = '''
                UPDATE teams_work SET
                    team_name = ?,
                    team_phone_1 = ?,
                    team_phone_2 = ?,
                    team_email = ?,
                    team_wassup = ?,
                    team_address = ?,
                    team_pay_method = ?,
                    team_username = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE team_number = ?
            '''
            
            self.db.cursor.execute(query, (
                team_data.get('team_name'),
                team_data.get('team_phone_1', ''),
                team_data.get('team_phone_2', ''),
                team_data.get('team_email', ''),
                team_data.get('team_wassup', ''),
                team_data.get('team_address', ''),
                team_data.get('team_pay_method', ''),
                team_data.get('team_username', ''),
                team_number
            ))
            
            self.db.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating team: {e}")
            return False
    
    def delete(self, team_number):
        """
        Delete a team
        
        Args:
            team_number: Team number to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.db.cursor.execute(
                'DELETE FROM teams_work WHERE team_number = ?',
                (team_number,)
            )
            self.db.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting team: {e}")
            return False
    
    def search(self, search_term):
        """
        Search teams by name or username
        
        Args:
            search_term: Term to search
            
        Returns:
            List of matching teams
        """
        try:
            query = '''
                SELECT * FROM teams_work 
                WHERE team_name LIKE ? OR team_username LIKE ?
                ORDER BY team_number
            '''
            self.db.cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
            rows = self.db.cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error searching teams: {e}")
            return []
