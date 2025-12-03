import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

if sys.platform == 'win32':
    import os
    os.system('chcp 65001 >nul 2>&1')

class DatabaseBackup:
    def __init__(self, db_path='anime_bot.db'):
        self.db_path = db_path
        self.backup_dir = Path('backups')
        self.backup_dir.mkdir(exist_ok=True)
    
    def export_all_to_json(self, output_file=None):
        """Export barcha data JSON formatda"""
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'backups/anime_backup_{timestamp}.json'
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            backup_data = {
                'backup_timestamp': datetime.now().isoformat(),
                'anime': [],
                'groups': [],
                'users': []
            }
            
            cursor.execute('SELECT * FROM anime')
            for row in cursor.fetchall():
                anime_data = dict(row)
                anime_code = anime_data['code']
                
                cursor.execute('SELECT * FROM anime_parts WHERE anime_code = ? ORDER BY part_number', (anime_code,))
                parts = [dict(p) for p in cursor.fetchall()]
                
                anime_data['parts'] = parts
                backup_data['anime'].append(anime_data)
            
            cursor.execute('SELECT * FROM groups')
            backup_data['groups'] = [dict(row) for row in cursor.fetchall()]
            
            cursor.execute('SELECT * FROM users')
            backup_data['users'] = [dict(row) for row in cursor.fetchall()]
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2, default=str)
            
            print(f"[OK] JSON backup yaratildi: {output_file}")
            return output_file
        
        finally:
            conn.close()
    
    def import_from_json(self, input_file):
        """JSON fayldan data import qilish"""
        with open(input_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for anime in backup_data.get('anime', []):
                parts = anime.pop('parts', [])
                
                try:
                    cursor.execute('''
                        INSERT OR REPLACE INTO anime (code, description, photo_id, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        anime['code'],
                        anime.get('description'),
                        anime.get('photo_id'),
                        anime.get('created_at'),
                        anime.get('updated_at')
                    ))
                    
                    for part in parts:
                        cursor.execute('''
                            INSERT OR REPLACE INTO anime_parts (anime_code, part_number, file_id, created_at)
                            VALUES (?, ?, ?, ?)
                        ''', (
                            part['anime_code'],
                            part['part_number'],
                            part['file_id'],
                            part.get('created_at')
                        ))
                except Exception as e:
                    print(f"[WARN] Anime {anime['code']} import: {e}")
            
            for group in backup_data.get('groups', []):
                try:
                    cursor.execute('''
                        INSERT OR REPLACE INTO groups (id, group_id, link, name, created_at)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        group['id'],
                        group['group_id'],
                        group.get('link'),
                        group.get('name'),
                        group.get('created_at')
                    ))
                except Exception as e:
                    print(f"[WARN] Guruh import: {e}")
            
            conn.commit()
            print(f"[OK] Import qilindi: {input_file}")
            return True
        
        finally:
            conn.close()
    
    def create_full_backup(self):
        """Database va JSON backup"""
        import shutil
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        db_backup = f'backups/anime_bot_{timestamp}.db'
        shutil.copy(self.db_path, db_backup)
        print(f"[OK] Database backup: {db_backup}")
        
        json_backup = self.export_all_to_json()
        
        return {
            'database': db_backup,
            'json': json_backup,
            'timestamp': timestamp
        }
    
    def get_backup_info(self, backup_file):
        """Backup faylning ma'lumotlarini ko'rish"""
        if backup_file.endswith('.json'):
            with open(backup_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return {
                'type': 'JSON',
                'anime_count': len(data.get('anime', [])),
                'groups_count': len(data.get('groups', [])),
                'users_count': len(data.get('users', [])),
                'timestamp': data.get('backup_timestamp')
            }
        
        elif backup_file.endswith('.db'):
            conn = sqlite3.connect(backup_file)
            cursor = conn.cursor()
            
            try:
                cursor.execute('SELECT COUNT(*) FROM anime')
                anime_count = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM groups')
                groups_count = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM users')
                users_count = cursor.fetchone()[0]
                
                return {
                    'type': 'SQLite',
                    'anime_count': anime_count,
                    'groups_count': groups_count,
                    'users_count': users_count
                }
            finally:
                conn.close()
        
        return None
    
    def list_backups(self):
        """Barcha backuplarni ko'rish"""
        backups = []
        
        for backup_file in self.backup_dir.glob('*'):
            if backup_file.is_file():
                info = self.get_backup_info(str(backup_file))
                backups.append({
                    'file': str(backup_file),
                    'size': backup_file.stat().st_size,
                    'info': info
                })
        
        return backups
    
    def auto_backup_on_startup(self):
        """Bot ishga tushganda avtomatik backup"""
        print("[*] Avtomatik backup yaratilmoqda...")
        try:
            backup_info = self.create_full_backup()
            print(f"[OK] Startup backup tugadi!")
            print(f"   Database: {backup_info['database']}")
            print(f"   JSON: {backup_info['json']}")
            return True
        except Exception as e:
            print(f"[ERROR] Backup xatosi: {e}")
            return False

if __name__ == '__main__':
    backup = DatabaseBackup()
    
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'export':
            backup.export_all_to_json()
        
        elif command == 'import' and len(sys.argv) > 2:
            backup.import_from_json(sys.argv[2])
        
        elif command == 'full':
            backup.create_full_backup()
        
        elif command == 'list':
            for b in backup.list_backups():
                print(f"\n📦 {b['file']}")
                print(f"   Size: {b['size'] / 1024:.1f} KB")
                if b['info']:
                    print(f"   Animeler: {b['info'].get('anime_count', 0)}")
                    print(f"   Guruhlar: {b['info'].get('groups_count', 0)}")
    else:
        print("✅ Doimiy backup tizimi tayyor!")
        print("Komandalar:")
        print("  python database_backup.py export    - JSON export")
        print("  python database_backup.py full      - Lengthening backup")
        print("  python database_backup.py list      - Backuplar ro'yxati")
        print("  python database_backup.py import <file>")
