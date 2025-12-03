import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict

class Database:
    def __init__(self, db_path='anime_bot.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anime (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code INTEGER UNIQUE NOT NULL,
                description TEXT,
                photo_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anime_parts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anime_code INTEGER NOT NULL,
                part_number INTEGER NOT NULL,
                file_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (anime_code) REFERENCES anime(code),
                UNIQUE(anime_code, part_number)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER UNIQUE NOT NULL,
                link TEXT,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anime_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anime_code INTEGER NOT NULL,
                group_id INTEGER NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (anime_code) REFERENCES anime(code),
                FOREIGN KEY (group_id) REFERENCES groups(id),
                UNIQUE(anime_code, group_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mandatory_channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT UNIQUE NOT NULL,
                link TEXT,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                anime_code INTEGER,
                part_number INTEGER,
                viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id, username=None, first_name=None, last_name=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name))
            
            cursor.execute('''
                UPDATE users SET last_seen = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (user_id,))
            
            conn.commit()
        except Exception as e:
            print(f"Error adding user: {e}")
        finally:
            conn.close()
    
    def add_anime(self, code: int, description: str = None, photo_id: str = None, 
                  parts: List[Dict] = None, groups: List[int] = None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO anime (code, description, photo_id)
                VALUES (?, ?, ?)
            ''', (code, description, photo_id))
            
            if parts:
                for part in parts:
                    cursor.execute('''
                        INSERT INTO anime_parts (anime_code, part_number, file_id)
                        VALUES (?, ?, ?)
                    ''', (code, part['part_number'], part['file_id']))
            
            if groups:
                for group_id in groups:
                    cursor.execute('''
                        INSERT OR IGNORE INTO anime_groups (anime_code, group_id)
                        VALUES (?, ?)
                    ''', (code, group_id))
            
            conn.commit()
        except Exception as e:
            print(f"Error adding anime: {e}")
        finally:
            conn.close()
    
    def get_anime_by_code(self, code: int) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM anime WHERE code = ?', (code,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
    
    def get_anime_parts(self, anime_code: int) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM anime_parts 
                WHERE anime_code = ? 
                ORDER BY part_number ASC
            ''', (anime_code,))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def get_anime_part(self, anime_code: int, part_number: int) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM anime_parts 
                WHERE anime_code = ? AND part_number = ?
            ''', (anime_code, part_number))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
    
    def add_anime_part(self, anime_code: int, part_number: int, file_id: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO anime_parts (anime_code, part_number, file_id)
                VALUES (?, ?, ?)
            ''', (anime_code, part_number, file_id))
            
            conn.commit()
        except Exception as e:
            print(f"Error adding part: {e}")
        finally:
            conn.close()
    
    def delete_anime_part(self, anime_code: int, part_number: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                DELETE FROM anime_parts 
                WHERE anime_code = ? AND part_number = ?
            ''', (anime_code, part_number))
            
            cursor.execute('''
                UPDATE anime_parts 
                SET part_number = part_number - 1 
                WHERE anime_code = ? AND part_number > ?
            ''', (anime_code, part_number))
            
            conn.commit()
        except Exception as e:
            print(f"Error deleting part: {e}")
        finally:
            conn.close()
    
    def delete_anime(self, code: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM anime_groups WHERE anime_code = ?', (code,))
            cursor.execute('DELETE FROM anime_parts WHERE anime_code = ?', (code,))
            cursor.execute('DELETE FROM anime WHERE code = ?', (code,))
            
            conn.commit()
        except Exception as e:
            print(f"Error deleting anime: {e}")
        finally:
            conn.close()
    
    def update_anime_description(self, code: int, description: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE anime 
                SET description = ?, updated_at = CURRENT_TIMESTAMP
                WHERE code = ?
            ''', (description, code))
            
            conn.commit()
        except Exception as e:
            print(f"Error updating anime: {e}")
        finally:
            conn.close()
    
    def add_group(self, group_id: int, link: str, name: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO groups (group_id, link, name)
                VALUES (?, ?, ?)
            ''', (group_id, link, name))
            
            conn.commit()
        except Exception as e:
            print(f"Error adding group: {e}")
        finally:
            conn.close()
    
    def get_all_groups(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM groups ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def get_group_by_id(self, group_id: int) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM groups WHERE group_id = ?', (group_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
    
    def delete_group(self, group_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM anime_groups WHERE group_id = (SELECT id FROM groups WHERE group_id = ?)', (group_id,))
            cursor.execute('DELETE FROM groups WHERE group_id = ?', (group_id,))
            
            conn.commit()
        except Exception as e:
            print(f"Error deleting group: {e}")
        finally:
            conn.close()
    
    def add_mandatory_channel(self, channel_id: str, link: str, name: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO mandatory_channels (channel_id, link, name)
                VALUES (?, ?, ?)
            ''', (channel_id, link, name))
            
            conn.commit()
        except Exception as e:
            print(f"Error adding channel: {e}")
        finally:
            conn.close()
    
    def get_mandatory_channels(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM mandatory_channels')
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def delete_mandatory_channel(self, channel_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM mandatory_channels WHERE id = ?', (channel_id,))
            conn.commit()
        except Exception as e:
            print(f"Error deleting channel: {e}")
        finally:
            conn.close()
    
    def add_user_history(self, user_id: int, anime_code: int, part_number: int = None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO user_history (user_id, anime_code, part_number)
                VALUES (?, ?, ?)
            ''', (user_id, anime_code, part_number))
            
            conn.commit()
        except Exception as e:
            print(f"Error adding history: {e}")
        finally:
            conn.close()
    
    def get_user_stats(self, user_id: int) -> Dict:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT COUNT(*) as total_views FROM user_history WHERE user_id = ?
            ''', (user_id,))
            result = cursor.fetchone()
            return dict(result) if result else {'total_views': 0}
        finally:
            conn.close()
    
    def search_anime_by_name(self, query: str) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM anime 
                WHERE description LIKE ? 
                ORDER BY created_at DESC 
                LIMIT 20
            ''', (f'%{query}%',))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def get_all_anime(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM anime ORDER BY code DESC')
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def get_total_anime_count(self) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT COUNT(*) FROM anime')
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            conn.close()
    
    def get_total_parts_count(self) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT COUNT(*) FROM anime_parts')
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            conn.close()
    
    def get_anime_groups(self, anime_code: int) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT g.* FROM groups g
                JOIN anime_groups ag ON g.id = ag.group_id
                WHERE ag.anime_code = ?
            ''', (anime_code,))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def get_all_users(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
