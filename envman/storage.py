"""
SQLite storage for environment variables
"""
import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class Storage:
    """Handle database operations for environment variables"""
    
    def __init__(self, db_path: Path):
        """Initialize database connection"""
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_db()
    
    def _init_db(self):
        """Create database tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Environments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS environments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Variables table (encrypted)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS variables (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                environment_id INTEGER NOT NULL,
                key TEXT NOT NULL,
                encrypted_value TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (environment_id) REFERENCES environments(id) ON DELETE CASCADE,
                UNIQUE(environment_id, key)
            )
        """)
        
        # Backups table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                environment_id INTEGER NOT NULL,
                backup_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (environment_id) REFERENCES environments(id) ON DELETE CASCADE
            )
        """)
        
        # Config table for settings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        
        self.conn.commit()
    
    def create_environment(self, name: str, description: str = "") -> int:
        """Create a new environment"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO environments (name, description) VALUES (?, ?)",
            (name, description)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_environment(self, name: str) -> Optional[Dict]:
        """Get environment by name"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM environments WHERE name = ?", (name,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def list_environments(self) -> List[Dict]:
        """List all environments"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM environments ORDER BY name")
        return [dict(row) for row in cursor.fetchall()]
    
    def delete_environment(self, name: str):
        """Delete an environment and all its variables"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM environments WHERE name = ?", (name,))
        self.conn.commit()
    
    def set_variable(self, environment_id: int, key: str, encrypted_value: str):
        """Set an encrypted variable for an environment"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO variables (environment_id, key, encrypted_value, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(environment_id, key) 
            DO UPDATE SET encrypted_value = ?, updated_at = CURRENT_TIMESTAMP
        """, (environment_id, key, encrypted_value, encrypted_value))
        self.conn.commit()
    
    def get_variables(self, environment_id: int) -> Dict[str, str]:
        """Get all encrypted variables for an environment"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT key, encrypted_value FROM variables WHERE environment_id = ?",
            (environment_id,)
        )
        return {row['key']: row['encrypted_value'] for row in cursor.fetchall()}
    
    def create_backup(self, environment_id: int, data: Dict):
        """Create a backup of an environment"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO backups (environment_id, backup_data) VALUES (?, ?)",
            (environment_id, json.dumps(data))
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_backups(self, environment_id: int) -> List[Dict]:
        """Get all backups for an environment"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM backups WHERE environment_id = ? ORDER BY created_at DESC",
            (environment_id,)
        )
        backups = []
        for row in cursor.fetchall():
            backup = dict(row)
            backup['backup_data'] = json.loads(backup['backup_data'])
            backups.append(backup)
        return backups
    
    def set_config(self, key: str, value: str):
        """Set a configuration value"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)",
            (key, value)
        )
        self.conn.commit()
    
    def get_config(self, key: str) -> Optional[str]:
        """Get a configuration value"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM config WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row['value'] if row else None
    
    def close(self):
        """Close database connection"""
        self.conn.close()
