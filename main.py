import logging
import os
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes
from bot import AnimeBot
from database import Database
from admin_utils import AdminUtils
from extended_features import ExtendedFeatures
from database_backup import DatabaseBackup
from config import TOKEN, ADMIN_IDS, MANDATORY_CHANNELS

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class AnimeBotMain:
    def __init__(self):
        self.backup = DatabaseBackup()
        self.backup.auto_backup_on_startup()
        
        self.db = Database()
        self.admin_utils = AdminUtils()
        self.extended = ExtendedFeatures()
        self.anime_bot = AnimeBot()
        self.app = self.anime_bot.app
        self.setup_additional_handlers()
        self.init_mandatory_channels()
    
    def init_mandatory_channels(self):
        existing = self.db.get_mandatory_channels()
        if not existing:
            for channel in MANDATORY_CHANNELS:
                self.db.add_mandatory_channel(
                    channel['channel_id'],
                    channel['link'],
                    channel['name']
                )
    
    def setup_additional_handlers(self):
        self.app.add_handler(CommandHandler("stats", self.stats_command))
        self.app.add_handler(CommandHandler("analytics", self.analytics_command))
        self.app.add_handler(CommandHandler("top", self.top_anime_command))
        self.app.add_handler(CommandHandler("backup", self.backup_command))
        self.app.add_handler(CommandHandler("export", self.export_command))
        self.app.add_handler(CommandHandler("search", self.search_command))
        self.app.add_handler(CommandHandler("groups", self.groups_command))
        self.app.add_handler(CommandHandler("broadcast", self.broadcast_command))
        self.app.add_handler(CommandHandler("test", self.test_command))
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        await self.extended.send_admin_stats(update, context)
    
    async def analytics_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        await self.extended.send_analytics(update, context)
    
    async def top_anime_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        await self.extended.send_top_anime(update, context)
    
    async def backup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        await update.message.reply_text("💾 Backup yaratilmoqda...")
        
        try:
            backup_info = self.backup.create_full_backup()
            
            text = f"""
✅ <b>Backup Tugadi!</b>

📊 Database Backup:
   {backup_info['database']}

📋 JSON Backup:
   {backup_info['json']}

⏰ Vaqt: {backup_info['timestamp']}

💾 Saqlanish holati:
   ✅ Barcha animelari
   ✅ Barcha videolar
   ✅ Barcha izohlar
   ✅ Barcha guruhlar
            """
            
            await update.message.reply_text(text, parse_mode='HTML')
        except Exception as e:
            await update.message.reply_text(f"❌ Xato: {str(e)[:100]}")
    
    async def export_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        await self.extended.export_anime_list(update, context)
    
    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🔍 Anime nomini yuboring:"
        )
    
    async def groups_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        groups = self.db.get_all_groups()
        
        if not groups:
            await update.message.reply_text("📍 Hozircha guruh yo'q!")
            return
        
        text = "📋 <b>Barcha Guruhlar</b>\n\n"
        for idx, group in enumerate(groups, 1):
            text += f"{idx}. <b>{group['name']}</b>\n"
            text += f"   🔗 {group['link']}\n"
            text += f"   ID: <code>{group['group_id']}</code>\n\n"
        
        await update.message.reply_text(text, parse_mode='HTML')
    
    async def broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        await update.message.reply_text(
            "📢 Xabar yuboring (barcha foydalanuvchilarga jo'natiladi):"
        )
    
    async def test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return
        
        stats = self.admin_utils.get_bot_statistics()
        
        test_info = f"""
✅ <b>Bot Tekshiruvi</b>

<b>Ma'lumotlar Bazasi:</b> ✅ Aktiv
<b>Foydalanuvchilar:</b> {stats['total_users']}
<b>Animeler:</b> {stats['total_anime']}
<b>Qismlar:</b> {stats['total_parts']}
<b>Guruhlar:</b> {stats['total_groups']}

<b>Status:</b> ✅ Hamma normal
        """
        
        await update.message.reply_text(test_info, parse_mode='HTML')
    
    def run(self):
        logger.info("Bot ishga tushmoqda...")
        print("[*] Anime Bot ishga tushdi!")
        print("[*] Bot ishga tushdi va polling boshlanmoqda...")
        self.app.run_polling()

if __name__ == '__main__':
    if not TOKEN or TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ XATO: Token sozlanmagan!")
        print("📝 Iltimos .env faylida TOKEN sozlang")
        sys.exit(1)
    
    main = AnimeBotMain()
    main.run()
