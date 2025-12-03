from database import Database
from datetime import datetime, timedelta
from typing import Dict, List
import json

class AdminUtils:
    def __init__(self):
        self.db = Database()
    
    def get_bot_statistics(self) -> Dict:
        total_users = self.get_total_users()
        total_anime = self.db.get_total_anime_count()
        total_parts = self.db.get_total_parts_count()
        total_groups = len(self.db.get_all_groups())
        
        return {
            'total_users': total_users,
            'total_anime': total_anime,
            'total_parts': total_parts,
            'total_groups': total_groups,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_total_users(self) -> int:
        conn = __import__('sqlite3').connect(self.db.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT COUNT(*) FROM users')
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            conn.close()
    
    def get_active_users(self, days: int = 7) -> int:
        conn = __import__('sqlite3').connect(self.db.db_path)
        cursor = conn.cursor()
        
        try:
            since_date = (datetime.now() - timedelta(days=days)).isoformat()
            cursor.execute(
                'SELECT COUNT(*) FROM users WHERE last_seen > ?',
                (since_date,)
            )
            result = cursor.fetchone()
            return result[0] if result else 0
        finally:
            conn.close()
    
    def get_most_viewed_anime(self, limit: int = 10) -> List[Dict]:
        conn = __import__('sqlite3').connect(self.db.db_path)
        conn.row_factory = __import__('sqlite3').Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT a.code, a.description, COUNT(uh.id) as view_count
                FROM anime a
                LEFT JOIN user_history uh ON a.code = uh.anime_code
                GROUP BY a.code
                ORDER BY view_count DESC
                LIMIT ?
            ''', (limit,))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def get_anime_details(self, code: int) -> Dict:
        anime = self.db.get_anime_by_code(code)
        if not anime:
            return None
        
        parts = self.db.get_anime_parts(code)
        groups = self.db.get_anime_groups(code)
        
        conn = __import__('sqlite3').connect(self.db.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'SELECT COUNT(*) FROM user_history WHERE anime_code = ?',
                (code,)
            )
            view_count = cursor.fetchone()[0]
        finally:
            conn.close()
        
        return {
            'code': anime['code'],
            'description': anime['description'],
            'photo_id': anime['photo_id'],
            'total_parts': len(parts),
            'groups': len(groups),
            'views': view_count,
            'created_at': anime['created_at'],
            'updated_at': anime['updated_at']
        }
    
    def export_anime_list(self, output_file: str = 'anime_list.json'):
        all_anime = self.db.get_all_anime()
        
        anime_list = []
        for anime in all_anime:
            parts = self.db.get_anime_parts(anime['code'])
            groups = self.db.get_anime_groups(anime['code'])
            
            anime_list.append({
                'code': anime['code'],
                'description': anime['description'],
                'parts_count': len(parts),
                'groups': [g['name'] for g in groups],
                'created_at': anime['created_at']
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(anime_list, f, ensure_ascii=False, indent=2)
        
        return output_file
    
    def import_anime_from_json(self, input_file: str):
        with open(input_file, 'r', encoding='utf-8') as f:
            anime_list = json.load(f)
        
        count = 0
        for anime_data in anime_list:
            try:
                code = anime_data.get('code')
                if not code:
                    continue
                
                if self.db.get_anime_by_code(code):
                    continue
                
                description = anime_data.get('description', '')
                
                self.db.add_anime(
                    code=code,
                    description=description,
                    photo_id=None,
                    parts=[]
                )
                count += 1
            except Exception as e:
                print(f"Error importing anime {anime_data}: {e}")
        
        return count
    
    def get_user_activity_report(self, days: int = 30) -> Dict:
        conn = __import__('sqlite3').connect(self.db.db_path)
        conn.row_factory = __import__('sqlite3').Row
        cursor = conn.cursor()
        
        try:
            since_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            cursor.execute('''
                SELECT DATE(viewed_at) as date, COUNT(*) as views
                FROM user_history
                WHERE viewed_at > ?
                GROUP BY DATE(viewed_at)
                ORDER BY date DESC
            ''', (since_date,))
            
            activity = [dict(row) for row in cursor.fetchall()]
            
            cursor.execute('''
                SELECT COUNT(DISTINCT user_id) as active_users
                FROM user_history
                WHERE viewed_at > ?
            ''', (since_date,))
            
            active_users = cursor.fetchone()['active_users']
            
            return {
                'period_days': days,
                'active_users': active_users,
                'daily_activity': activity
            }
        finally:
            conn.close()
    
    def cleanup_old_data(self, days: int = 90):
        conn = __import__('sqlite3').connect(self.db.db_path)
        cursor = conn.cursor()
        
        try:
            old_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            cursor.execute(
                'DELETE FROM user_history WHERE viewed_at < ?',
                (old_date,)
            )
            
            deleted_rows = cursor.rowcount
            conn.commit()
            
            return deleted_rows
        finally:
            conn.close()
    
    def get_group_statistics(self) -> List[Dict]:
        groups = self.db.get_all_groups()
        
        stats = []
        for group in groups:
            conn = __import__('sqlite3').connect(self.db.db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute(
                    'SELECT COUNT(*) FROM anime_groups WHERE group_id = ?',
                    (group['id'],)
                )
                anime_count = cursor.fetchone()[0]
            finally:
                conn.close()
            
            stats.append({
                'name': group['name'],
                'link': group['link'],
                'anime_count': anime_count,
                'created_at': group['created_at']
            })
        
        return stats
    
    def add_manga_channel(self, channel_id: str, link: str, name: str):
        self.db.add_mandatory_channel(channel_id, link, name)
    
    def remove_manga_channel(self, channel_id: str):
        conn = __import__('sqlite3').connect(self.db.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'DELETE FROM mandatory_channels WHERE channel_id = ?',
                (channel_id,)
            )
            conn.commit()
        finally:
            conn.close()
    
    def get_user_info(self, user_id: int) -> Dict:
        conn = __import__('sqlite3').connect(self.db.db_path)
        conn.row_factory = __import__('sqlite3').Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()
            
            if not user:
                return None
            
            cursor.execute(
                'SELECT COUNT(*) FROM user_history WHERE user_id = ?',
                (user_id,)
            )
            view_count = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT DISTINCT anime_code FROM user_history WHERE user_id = ?
            ''', (user_id,))
            watched_anime = cursor.fetchall()
            
            return {
                'user_id': user['user_id'],
                'username': user['username'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'created_at': user['created_at'],
                'last_seen': user['last_seen'],
                'total_views': view_count,
                'watched_anime_count': len(watched_anime)
            }
        finally:
            conn.close()
