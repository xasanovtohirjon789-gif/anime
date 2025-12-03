from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import Database
from admin_utils import AdminUtils
from config import ADMIN_IDS
import asyncio

class ExtendedFeatures:
    def __init__(self):
        self.db = Database()
        self.admin_utils = AdminUtils()
    
    async def broadcast_message(self, context: ContextTypes.DEFAULT_TYPE, 
                               message_type: str, content: dict, 
                               target_groups: list = None, target_users: list = None):
        
        if message_type == 'anime':
            code = content.get('code')
            description = content.get('description')
            photo_id = content.get('photo_id')
            
            users = target_users or self.db.get_all_users()
            
            failed = 0
            sent = 0
            
            for user in users:
                try:
                    if photo_id:
                        await context.bot.send_photo(
                            chat_id=user['user_id'],
                            photo=photo_id,
                            caption=f"<b>📺 Yangi Anime!</b>\n\n{description}",
                            parse_mode='HTML'
                        )
                    else:
                        await context.bot.send_message(
                            chat_id=user['user_id'],
                            text=f"<b>📺 Yangi Anime!</b>\n\n{description}",
                            parse_mode='HTML'
                        )
                    sent += 1
                    await asyncio.sleep(0.1)
                except Exception as e:
                    failed += 1
                    print(f"Failed to send to {user['user_id']}: {e}")
            
            if target_groups:
                for group_id in target_groups:
                    try:
                        if photo_id:
                            await context.bot.send_photo(
                                chat_id=group_id,
                                photo=photo_id,
                                caption=f"<b>📺 Yangi Anime!</b>\n\n{description}",
                                parse_mode='HTML'
                            )
                        else:
                            await context.bot.send_message(
                                chat_id=group_id,
                                text=f"<b>📺 Yangi Anime!</b>\n\n{description}",
                                parse_mode='HTML'
                            )
                    except Exception as e:
                        print(f"Failed to send to group {group_id}: {e}")
            
            return {'sent': sent, 'failed': failed}
    
    async def send_admin_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        stats = self.admin_utils.get_bot_statistics()
        
        text = f"""
⚙️ <b>Bot Statistikasi</b>

👥 Foydalanuvchilar: {stats['total_users']}
📺 Animeler: {stats['total_anime']}
🎬 Qismlar: {stats['total_parts']}
📍 Guruhlar: {stats['total_groups']}

🕐 O'zgartirilgan vaqt: {stats['timestamp']}
        """
        
        await update.message.reply_text(text, parse_mode='HTML')
    
    async def send_analytics(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        report = self.admin_utils.get_user_activity_report(days=30)
        
        text = f"""
📊 <b>Faoliyat Hisoboti (30 kun)</b>

👥 Faol Foydalanuvchilar: {report['active_users']}

<b>Kunlik Ko'rishlar:</b>
"""
        
        for day in report['daily_activity'][:10]:
            text += f"\n📅 {day['date']}: {day['views']} ko'rish"
        
        await update.message.reply_text(text, parse_mode='HTML')
    
    async def send_top_anime(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        top_anime = self.admin_utils.get_most_viewed_anime(limit=15)
        
        text = "<b>🔥 Eng Ko'p Ko'rilgan Animeler</b>\n\n"
        
        for idx, anime in enumerate(top_anime, 1):
            text += f"{idx}. {anime['description'][:50]}... - {anime['view_count']} ko'rish\n"
        
        await update.message.reply_text(text, parse_mode='HTML')
    
    async def backup_database(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        import shutil
        from datetime import datetime
        
        backup_name = f"anime_bot_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        
        try:
            shutil.copy(self.db.db_path, backup_name)
            
            with open(backup_name, 'rb') as f:
                await context.bot.send_document(
                    chat_id=user_id,
                    document=f,
                    filename=backup_name
                )
            
            await update.message.reply_text("✅ Ma'lumotlar bazasi zaxiralandi!")
        except Exception as e:
            await update.message.reply_text(f"❌ Xato: {e}")
    
    async def export_anime_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        try:
            export_file = self.admin_utils.export_anime_list()
            
            with open(export_file, 'rb') as f:
                await context.bot.send_document(
                    chat_id=user_id,
                    document=f,
                    filename=export_file
                )
            
            await update.message.reply_text("✅ Animeler ro'yxati eksport qilindi!")
        except Exception as e:
            await update.message.reply_text(f"❌ Xato: {e}")
    
    async def search_anime_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        await update.message.reply_text(
            "🔍 Qidirish uchun anime nomini yuboring:"
        )
    
    def get_all_users(self) -> list:
        conn = __import__('sqlite3').connect(self.db.db_path)
        conn.row_factory = __import__('sqlite3').Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM users')
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
