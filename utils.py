import re
from typing import Optional, Tuple
from datetime import datetime

class ValidationUtils:
    @staticmethod
    def is_valid_code(code: str) -> bool:
        return code.isdigit()
    
    @staticmethod
    def is_valid_group_id(group_id: str) -> bool:
        return group_id.lstrip('-').isdigit()
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return re.match(url_pattern, url) is not None
    
    @staticmethod
    def is_valid_telegram_url(url: str) -> bool:
        return url.startswith('https://t.me/') or url.startswith('t.me/')
    
    @staticmethod
    def clean_text(text: str, max_length: int = 4096) -> str:
        text = text.strip()
        if len(text) > max_length:
            text = text[:max_length-3] + "..."
        return text
    
    @staticmethod
    def format_timestamp(timestamp: str) -> str:
        try:
            dt = datetime.fromisoformat(timestamp)
            return dt.strftime("%d.%m.%Y %H:%M")
        except:
            return timestamp

class TextFormatting:
    @staticmethod
    def format_anime_description(description: str, max_parts: int = 1000) -> str:
        text = f"📺 <b>Anime Izohi</b>\n\n{description[:500]}"
        if len(description) > 500:
            text += "...\n\n<i>To'liq izohni ko'rish uchun qismlarni tanlang</i>"
        return text
    
    @staticmethod
    def format_parts_grid(total_parts: int, current_page: int, parts_per_page: int = 10) -> Tuple[list, int]:
        total_pages = (total_parts + parts_per_page - 1) // parts_per_page
        
        if current_page > total_pages:
            current_page = total_pages
        if current_page < 1:
            current_page = 1
        
        start = (current_page - 1) * parts_per_page + 1
        end = min(start + parts_per_page - 1, total_parts)
        
        parts_range = list(range(start, end + 1))
        grid = [parts_range[i:i+5] for i in range(0, len(parts_range), 5)]
        
        return grid, total_pages
    
    @staticmethod
    def format_admin_menu_text() -> str:
        return """
⚙️ <b>Admin Panel</b>

Kerakli amalni tanlang:

✏️ <b>Anime Boshqaruvi:</b>
• Anime qo'shish
• Anime o'chirish
• Anime tahrirlash

📍 <b>Guruh Boshqaruvi:</b>
• Guruh qo'shish
• Guruhlar ro'yxati
• Guruh o'chirish

📊 <b>Statistika:</b>
• /stats - Bot statistikasi
• /analytics - Faoliyat hisoboti
• /top - Eng ko'p ko'rilgan
"""
    
    @staticmethod
    def format_anime_card(anime_data: dict) -> str:
        text = f"""
📺 <b>{anime_data.get('description', 'Anime')[:100]}</b>

📝 Kod: <code>{anime_data['code']}</code>
🎬 Qismlar: {anime_data.get('total_parts', 0)}
👥 Ko'rishlar: {anime_data.get('views', 0)}
📅 Yaratilgan: {TextFormatting.format_timestamp(anime_data['created_at'])}
"""
        return text

class ErrorMessages:
    INVALID_CODE = "❌ Kod faqat raqam bo'lishi kerak!"
    CODE_NOT_FOUND = "❌ Bu kodli anime topilmadi!"
    NOT_ADMIN = "❌ Siz admin emassiz!"
    NOT_SUBSCRIBED = "❌ Siz majburiy kanallarga obuna bo'lmagansiz!"
    DATABASE_ERROR = "❌ Ma'lumotlar bazasi xatosi!"
    UPLOAD_ERROR = "❌ Fayl yuklashda xato!"
    INVALID_GROUP_ID = "❌ Guruh ID noto'g'ri!"
    ANIME_EXISTS = "❌ Bu kod allaqachon mavjud!"
    NO_PARTS = "❌ Bu animeda qism yo'q!"

class SuccessMessages:
    ANIME_ADDED = "✅ Anime muvaffaqiyatli qo'shildi!"
    ANIME_DELETED = "✅ Anime muvaffaqiyatli o'chirildi!"
    ANIME_UPDATED = "✅ Anime muvaffaqiyatli o'zgartirildi!"
    PART_ADDED = "✅ Qism qo'shildi!"
    PART_DELETED = "✅ Qism o'chirildi!"
    GROUP_ADDED = "✅ Guruh qo'shildi!"
    GROUP_DELETED = "✅ Guruh o'chirildi!"
    SUBSCRIPTION_OK = "✅ Obuna tekshiruvi muvaffaqiyatli!"

class ButtonLabels:
    CHECK = "✅ Tekshirish"
    VIEW = "🎬 Animeni ko'rish"
    ADD_ANIME = "➕ Anime qo'shish"
    DELETE_ANIME = "❌ Anime o'chirish"
    EDIT_ANIME = "✏️ Anime tahrirlash"
    ADD_GROUP = "➕ Guruh qo'shish"
    GROUPS_LIST = "📋 Guruhlar ro'yxati"
    DELETE_GROUP = "❌ Guruh o'chirish"
    BACK = "🔙 Orqaga qaytish"
    YES = "✅ Ha"
    NO = "❌ Yo'q"
    NEXT = "O'ng ➡"
    PREV = "⬅ Chap"
    FINISH = "✅ Tugatish"

class LoggerUtils:
    @staticmethod
    def log_user_action(user_id: int, action: str, details: str = ""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] User {user_id}: {action}"
        if details:
            log_message += f" | {details}"
        print(log_message)
    
    @staticmethod
    def log_error(error_type: str, error_message: str, context: str = ""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] ERROR [{error_type}]: {error_message}"
        if context:
            log_message += f" | {context}"
        print(f"❌ {log_message}")
    
    @staticmethod
    def log_admin_action(admin_id: int, action: str, details: str = ""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] ADMIN {admin_id}: {action}"
        if details:
            log_message += f" | {details}"
        print(f"⚙️ {log_message}")

class PaginationUtils:
    @staticmethod
    def calculate_pagination(total_items: int, page: int, items_per_page: int = 10) -> dict:
        total_pages = (total_items + items_per_page - 1) // items_per_page
        
        if page > total_pages:
            page = total_pages
        if page < 1:
            page = 1
        
        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_items)
        
        return {
            'page': page,
            'total_pages': total_pages,
            'start_idx': start_idx,
            'end_idx': end_idx,
            'total_items': total_items,
            'has_prev': page > 1,
            'has_next': page < total_pages,
            'items_on_page': end_idx - start_idx
        }
    
    @staticmethod
    def create_page_buttons(page: int, total_pages: int) -> list:
        buttons = []
        
        if page > 1:
            buttons.append(("⬅ Chap", f"page_{page-1}"))
        
        buttons.append((f"{page}/{total_pages}", "page_info"))
        
        if page < total_pages:
            buttons.append(("O'ng ➡", f"page_{page+1}"))
        
        return buttons

class SecurityUtils:
    @staticmethod
    def sanitize_code(code: str) -> Optional[int]:
        try:
            code = code.strip()
            if code.isdigit():
                return int(code)
            return None
        except:
            return None
    
    @staticmethod
    def sanitize_group_id(group_id: str) -> Optional[int]:
        try:
            group_id = group_id.strip()
            if group_id.lstrip('-').isdigit():
                return int(group_id)
            return None
        except:
            return None
    
    @staticmethod
    def is_safe_string(text: str, max_length: int = 1000) -> bool:
        if len(text) > max_length:
            return False
        
        dangerous_chars = ['<script', 'javascript:', 'onclick', 'onerror']
        text_lower = text.lower()
        
        for char in dangerous_chars:
            if char in text_lower:
                return False
        
        return True
