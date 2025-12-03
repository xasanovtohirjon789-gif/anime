from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from database import Database
from config import ADMIN_IDS
from utils import ValidationUtils, ErrorMessages, LoggerUtils, PaginationUtils
from middleware import session_middleware, rate_limit_middleware, error_handler_middleware

class GeneralHandlers:
    def __init__(self):
        self.db = Database()
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        error_msg = str(context.error)
        
        if update and update.effective_user:
            user_id = update.effective_user.id
            error_handler_middleware.log_error(user_id, "Handler Error", error_msg)
        
        LoggerUtils.log_error("HANDLER", error_msg)
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.text:
            return
        
        user_id = update.effective_user.id
        
        if rate_limit_middleware.is_rate_limited(user_id):
            await update.message.reply_text(
                "⏱️ Juda ko'p xabar yuborayotganingiz!\n"
                "Bir oz kutib ko'ring."
            )
            return
        
        await session_middleware.track_user(update, context)
        
        text = update.message.text.strip()
        
        if not text or len(text) > 1000:
            await update.message.reply_text(ErrorMessages.DATABASE_ERROR)
            return

class SearchHandlers:
    def __init__(self):
        self.db = Database()
    
    async def handle_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_id = update.effective_user.id
        
        query = update.message.text.strip()
        
        if len(query) < 2:
            await update.message.reply_text(
                "🔍 Kamida 2 belgi yuboring!"
            )
            return
        
        results = self.db.search_anime_by_name(query)
        
        if not results:
            await update.message.reply_text(
                f"❌ '{query}' bo'yicha anime topilmadi!"
            )
            return
        
        context.user_data['search_results'] = results
        context.user_data['search_page'] = 0
        
        keyboard = []
        for idx, anime in enumerate(results[:5]):
            keyboard.append([
                InlineKeyboardButton(
                    anime['description'][:50] if anime['description'] else f"Kod: {anime['code']}",
                    callback_data=f"search_select_{idx}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("📄 Ko'proq", callback_data="search_next")])
        
        await update.message.reply_text(
            f"🔍 Natijalar ({len(results)} ta):",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

class NotificationHandlers:
    def __init__(self):
        self.db = Database()
    
    async def send_notification(self, context: ContextTypes.DEFAULT_TYPE, 
                               user_id: int, message: str, is_alert: bool = False):
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='HTML'
            )
        except Exception as e:
            LoggerUtils.log_error("NOTIFICATION", str(e), f"User: {user_id}")

class AnalyticsHandlers:
    def __init__(self):
        self.db = Database()
    
    async def track_view(self, user_id: int, anime_code: int, part_number: int = None):
        self.db.add_user_history(user_id, anime_code, part_number)
    
    async def get_user_stats(self, user_id: int) -> dict:
        return self.db.get_user_stats(user_id)

class CallbackHandlers:
    def __init__(self):
        self.db = Database()
    
    async def handle_inline_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        user_id = query.from_user.id
        
        if rate_limit_middleware.is_rate_limited(user_id):
            await query.answer(
                "⏱️ Juda ko'p amallar!"
            )
            return
        
        await query.answer()

class MediaHandlers:
    def __init__(self):
        self.db = Database()
    
    async def handle_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.video:
            file_id = update.message.video.file_id
            file_size = update.message.video.file_size
            
            if file_size > 2000000000:
                await update.message.reply_text(
                    "❌ Video hajmi 2GB dan ortiq!"
                )
                return
            
            return file_id
        
        return None
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.photo:
            return update.message.photo[-1].file_id
        
        return None
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.document:
            return update.message.document.file_id
        
        return None

class TextInputHandlers:
    @staticmethod
    def sanitize_input(text: str, max_length: int = 500) -> str:
        text = text.strip()
        
        if len(text) > max_length:
            text = text[:max_length]
        
        text = text.replace('<', '&lt;').replace('>', '&gt;')
        
        return text
    
    @staticmethod
    def validate_anime_code(code_str: str) -> int:
        if not ValidationUtils.is_valid_code(code_str):
            return None
        
        code = int(code_str)
        
        if code < 0 or code > 999999:
            return None
        
        return code
    
    @staticmethod
    def validate_group_id(group_id_str: str) -> int:
        if not ValidationUtils.is_valid_group_id(group_id_str):
            return None
        
        group_id = int(group_id_str)
        
        return group_id

class PaginationHandlers:
    def __init__(self):
        self.db = Database()
    
    async def create_paginated_buttons(self, total_items: int, page: int, 
                                       items_per_page: int = 10) -> dict:
        pagination = PaginationUtils.calculate_pagination(
            total_items, page, items_per_page
        )
        
        return pagination

class StateManagementHandlers:
    def __init__(self):
        self.user_states = {}
    
    def set_user_state(self, user_id: int, state: str, data: dict = None):
        self.user_states[user_id] = {
            'state': state,
            'data': data or {},
            'timestamp': __import__('datetime').datetime.now()
        }
    
    def get_user_state(self, user_id: int) -> str:
        if user_id in self.user_states:
            return self.user_states[user_id]['state']
        
        return None
    
    def get_user_data(self, user_id: int) -> dict:
        if user_id in self.user_states:
            return self.user_states[user_id]['data']
        
        return {}
    
    def clear_user_state(self, user_id: int):
        if user_id in self.user_states:
            del self.user_states[user_id]

class ValidationHandlers:
    @staticmethod
    async def validate_subscription(context: ContextTypes.DEFAULT_TYPE, 
                                   user_id: int, channels: list) -> bool:
        for channel in channels:
            try:
                member = await context.bot.get_chat_member(
                    channel['channel_id'], 
                    user_id
                )
                
                if member.status not in ['member', 'administrator', 'creator']:
                    return False
            except:
                return False
        
        return True
    
    @staticmethod
    async def validate_admin_access(update: Update) -> bool:
        user_id = update.effective_user.id
        return user_id in ADMIN_IDS
