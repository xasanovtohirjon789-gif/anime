import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
from database import Database
from config import ADMIN_IDS
from utils import LoggerUtils, ValidationUtils, ErrorMessages

class AdvancedAdminPanel:
    def __init__(self):
        self.db = Database()
        self.broadcast_data = {}
    
    async def handle_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text(ErrorMessages.NOT_ADMIN)
            return ConversationHandler.END
        
        keyboard = [
            [InlineKeyboardButton("👥 Barcha foydalanuvchilarga", callback_data="broadcast_all_users")],
            [InlineKeyboardButton("📍 Barcha guruhlarga", callback_data="broadcast_all_groups")],
            [InlineKeyboardButton("📍 Tanlangan guruhga", callback_data="broadcast_select_group")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="broadcast_cancel")]
        ]
        
        await update.message.reply_text(
            "📢 Xabar yuborish turini tanlang:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return 100
    
    async def broadcast_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        if query.data == "broadcast_all_users":
            context.user_data['broadcast_target'] = 'all_users'
            await query.edit_message_text("📝 Xabarni yuboring (matn yoki media):")
            return 101
        
        elif query.data == "broadcast_all_groups":
            context.user_data['broadcast_target'] = 'all_groups'
            await query.edit_message_text("📝 Xabarni yuboring (matn yoki media):")
            return 101
        
        elif query.data == "broadcast_select_group":
            groups = self.db.get_all_groups()
            if not groups:
                await query.answer("❌ Guruh yo'q!", show_alert=True)
                return 100
            
            keyboard = [[InlineKeyboardButton(g['name'], callback_data=f"br_group_{g['id']}")] for g in groups]
            keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="broadcast_cancel")])
            
            await query.edit_message_text(
                "📍 Guruhni tanlang:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return 102
        
        elif query.data == "broadcast_cancel":
            await query.delete_message()
            return ConversationHandler.END
        
        return 100
    
    async def select_broadcast_group(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        if query.data == "broadcast_cancel":
            await query.delete_message()
            return ConversationHandler.END
        
        group_id = int(query.data.split("_")[2])
        context.user_data['broadcast_target'] = 'group'
        context.user_data['broadcast_group_id'] = group_id
        
        group = self.db.get_group_by_id(group_id)
        
        await query.edit_message_text(
            f"📝 Guruhga xabar yuboring:\n\n📍 {group['name']}"
        )
        return 101
    
    async def receive_broadcast_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        target = context.user_data.get('broadcast_target')
        
        if update.message.text:
            message_data = {
                'type': 'text',
                'content': update.message.text
            }
        elif update.message.photo:
            message_data = {
                'type': 'photo',
                'content': update.message.photo[-1].file_id,
                'caption': update.message.caption
            }
        elif update.message.video:
            message_data = {
                'type': 'video',
                'content': update.message.video.file_id,
                'caption': update.message.caption
            }
        else:
            await update.message.reply_text("❌ Bu format qo'llab-quvvatlanmaydi!")
            return 101
        
        keyboard = [
            [InlineKeyboardButton("✅ Jo'natish", callback_data="confirm_broadcast")],
            [InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel_broadcast")]
        ]
        
        preview_text = message_data['content'] if isinstance(message_data['content'], str) else "[Video/Rasm]"
        
        await update.message.reply_text(
            f"📋 Xabar ko'rinishi:\n\n{preview_text[:100]}...\n\n"
            f"📍 Manzil: {target}\n\n"
            "Tasdiqlang:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        context.user_data['broadcast_message'] = message_data
        
        return 103
    
    async def confirm_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        if query.data == "cancel_broadcast":
            await query.edit_message_text("❌ Bekor qilindi!")
            return ConversationHandler.END
        
        target = context.user_data.get('broadcast_target')
        message_data = context.user_data.get('broadcast_message')
        
        await query.edit_message_text("📤 Xabar yuborilmoqda...")
        
        sent_count = 0
        failed_count = 0
        
        try:
            if target == 'all_users':
                users = self.get_all_users()
                sent_count, failed_count = await self.send_to_users(
                    context, users, message_data
                )
            
            elif target == 'all_groups':
                groups = self.db.get_all_groups()
                sent_count, failed_count = await self.send_to_groups(
                    context, groups, message_data
                )
            
            elif target == 'group':
                group_id = context.user_data.get('broadcast_group_id')
                group = self.db.get_group_by_id(group_id)
                sent_count, failed_count = await self.send_to_groups(
                    context, [group], message_data
                )
            
            await query.edit_message_text(
                f"✅ Xabar yuborildi!\n\n"
                f"✅ Muvaffaqiyatli: {sent_count}\n"
                f"❌ Xatoli: {failed_count}"
            )
            
            LoggerUtils.log_admin_action(
                query.from_user.id,
                "Broadcast",
                f"Target: {target}, Sent: {sent_count}, Failed: {failed_count}"
            )
        
        except Exception as e:
            LoggerUtils.log_error("BROADCAST", str(e))
            await query.edit_message_text(f"❌ Xato: {str(e)[:100]}")
        
        return ConversationHandler.END
    
    async def send_to_users(self, context: ContextTypes.DEFAULT_TYPE, users: list, message_data: dict) -> tuple:
        sent = 0
        failed = 0
        
        for user in users:
            try:
                await self.send_message(context, user['user_id'], message_data)
                sent += 1
                await asyncio.sleep(0.05)
            except Exception as e:
                failed += 1
                print(f"Failed to send to {user['user_id']}: {e}")
        
        return sent, failed
    
    async def send_to_groups(self, context: ContextTypes.DEFAULT_TYPE, groups: list, message_data: dict) -> tuple:
        sent = 0
        failed = 0
        
        for group in groups:
            try:
                await self.send_message(context, group['group_id'], message_data)
                sent += 1
                await asyncio.sleep(0.05)
            except Exception as e:
                failed += 1
                print(f"Failed to send to group {group['group_id']}: {e}")
        
        return sent, failed
    
    async def send_message(self, context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_data: dict):
        if message_data['type'] == 'text':
            await context.bot.send_message(
                chat_id=chat_id,
                text=message_data['content'],
                parse_mode='HTML'
            )
        elif message_data['type'] == 'photo':
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=message_data['content'],
                caption=message_data.get('caption'),
                parse_mode='HTML'
            )
        elif message_data['type'] == 'video':
            await context.bot.send_video(
                chat_id=chat_id,
                video=message_data['content'],
                caption=message_data.get('caption'),
                parse_mode='HTML'
            )
    
    async def user_management(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text(ErrorMessages.NOT_ADMIN)
            return ConversationHandler.END
        
        users = self.get_all_users()
        
        text = f"""
👥 <b>Foydalanuvchi Boshqaruvi</b>

Jami foydalanuvchilar: {len(users)}
"""
        
        await update.message.reply_text(text, parse_mode='HTML')
        
        return ConversationHandler.END
    
    async def channel_management(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text(ErrorMessages.NOT_ADMIN)
            return ConversationHandler.END
        
        channels = self.db.get_mandatory_channels()
        
        keyboard = []
        for channel in channels:
            keyboard.append([
                InlineKeyboardButton(
                    f"❌ {channel['name']}", 
                    callback_data=f"remove_channel_{channel['id']}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("➕ Kanal qo'shish", callback_data="add_channel")])
        
        await update.message.reply_text(
            "📺 <b>Majburiy Kanallar</b>\n\n"
            "Kanalni tanlang:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )
        
        return ConversationHandler.END
    
    def get_all_users(self) -> list:
        conn = __import__('sqlite3').connect(self.db.db_path)
        conn.row_factory = __import__('sqlite3').Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

class UserManagementPanel:
    def __init__(self):
        self.db = Database()
    
    async def block_user(self, user_id: int):
        conn = __import__('sqlite3').connect(self.db.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET blocked = 1 WHERE user_id = ?
            ''', (user_id,))
            conn.commit()
        finally:
            conn.close()
    
    async def unblock_user(self, user_id: int):
        conn = __import__('sqlite3').connect(self.db.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET blocked = 0 WHERE user_id = ?
            ''', (user_id,))
            conn.commit()
        finally:
            conn.close()
    
    async def get_user_details(self, user_id: int) -> dict:
        return self.db.admin_utils.get_user_info(user_id) if hasattr(self.db, 'admin_utils') else None

class ModeratorPanel:
    def __init__(self):
        self.db = Database()
    
    async def report_anime(self, anime_code: int, reason: str, reported_by: int):
        conn = __import__('sqlite3').connect(self.db.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS anime_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    anime_code INTEGER NOT NULL,
                    reason TEXT,
                    reported_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'pending'
                )
            ''')
            
            cursor.execute('''
                INSERT INTO anime_reports (anime_code, reason, reported_by)
                VALUES (?, ?, ?)
            ''', (anime_code, reason, reported_by))
            
            conn.commit()
        finally:
            conn.close()
    
    async def get_pending_reports(self) -> list:
        conn = __import__('sqlite3').connect(self.db.db_path)
        conn.row_factory = __import__('sqlite3').Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM anime_reports WHERE status = 'pending'
            ''')
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
