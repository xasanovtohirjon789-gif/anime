from enum import Enum

class BotState(Enum):
    START = 1
    CHECK_SUBSCRIPTION = 2
    SEARCH_ANIME = 3
    VIEW_PARTS = 4
    SEND_PART = 5
    ADMIN_PANEL = 10
    ADD_ANIME_DESC = 11
    ADD_ANIME_FIRST_PART = 12
    ADD_MORE_PARTS = 13
    ADD_ANIME_CODE = 14
    SELECT_GROUPS = 15
    DELETE_ANIME = 16
    EDIT_ANIME = 17
    EDIT_ANIME_CHOICE = 18
    ADD_NEW_PART = 19
    DELETE_PART = 20
    ADD_GROUP_ID = 21
    ADD_GROUP_LINK = 22
    ADD_GROUP_NAME = 23
    SELECT_DELETE_GROUP = 24
    EDIT_DESCRIPTION = 25

class AnimeStatus(Enum):
    ACTIVE = 'active'
    DELETED = 'deleted'
    ARCHIVED = 'archived'
    PENDING = 'pending'

class UserRole(Enum):
    USER = 1
    MODERATOR = 2
    ADMIN = 3

class SubscriptionStatus(Enum):
    SUBSCRIBED = 'subscribed'
    NOT_SUBSCRIBED = 'not_subscribed'
    BLOCKED = 'blocked'

class NotificationType(Enum):
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    SUCCESS = 'success'

class CommandType(Enum):
    START = '/start'
    HELP = '/help'
    ADMIN = '/admin'
    STATS = '/stats'
    ANALYTICS = '/analytics'
    TOP = '/top'
    BACKUP = '/backup'
    EXPORT = '/export'
    SEARCH = '/search'
    GROUPS = '/groups'
    BROADCAST = '/broadcast'
    TEST = '/test'

class CallbackType(Enum):
    CHECK = 'check'
    VIEW = 'view'
    PART = 'part'
    PAGE = 'page'
    ADD_ANIME = 'add_anime'
    DELETE_ANIME = 'delete_anime'
    EDIT_ANIME = 'edit_anime'
    ADD_GROUP = 'add_group'
    DELETE_GROUP = 'delete_group'

class MediaType(Enum):
    VIDEO = 'video'
    PHOTO = 'photo'
    DOCUMENT = 'document'
    AUDIO = 'audio'
    TEXT = 'text'

class ErrorType(Enum):
    VALIDATION = 'validation'
    DATABASE = 'database'
    AUTHORIZATION = 'authorization'
    NETWORK = 'network'
    UNKNOWN = 'unknown'

class AnimeLimitConstants:
    MIN_CODE = 1
    MAX_CODE = 999999
    MIN_DESCRIPTION_LENGTH = 10
    MAX_DESCRIPTION_LENGTH = 4000
    MAX_PARTS_PER_ANIME = 1000
    PARTS_PER_PAGE = 10
    MIN_PARTS = 1

class TimeConstants:
    SESSION_TIMEOUT_HOURS = 24
    RATE_LIMIT_WINDOW_SECONDS = 60
    CONTEXT_TIMEOUT_MINUTES = 30
    INACTIVITY_TIMEOUT_HOURS = 7
    MESSAGE_DELETE_TIMEOUT_SECONDS = 300

class RateLimitConstants:
    MAX_REQUESTS_PER_MINUTE = 30
    MAX_REQUESTS_PER_HOUR = 300
    MAX_BROADCAST_PER_HOUR = 5
    MIN_DELAY_BETWEEN_MESSAGES = 0.05

class ValidationMessages:
    INVALID_CODE = "❌ Kod faqat raqam bo'lishi kerak!"
    INVALID_GROUP_ID = "❌ Guruh ID noto'g'ri!"
    INVALID_URL = "❌ URL noto'g'ri!"
    EMPTY_INPUT = "❌ Hech narsa yubormadingiz!"
    TOO_LONG = "❌ Matn juda uzun!"
    DUPLICATE_CODE = "❌ Bu kod allaqachon mavjud!"
    ANIME_NOT_FOUND = "❌ Anime topilmadi!"
    NO_PARTS = "❌ Qism yo'q!"

class SuccessMessages:
    OPERATION_COMPLETE = "✅ Operatsiya tugadi!"
    ANIME_ADDED = "✅ Anime qo'shildi!"
    ANIME_DELETED = "✅ Anime o'chirildi!"
    ANIME_UPDATED = "✅ Anime o'zgartirildi!"
    PART_ADDED = "✅ Qism qo'shildi!"
    PART_DELETED = "✅ Qism o'chirildi!"
    GROUP_ADDED = "✅ Guruh qo'shildi!"
    GROUP_DELETED = "✅ Guruh o'chirildi!"
    BROADCAST_SENT = "✅ Xabar yuborildi!"
    SUBSCRIPTION_OK = "✅ Obuna tekshiruvi o'tdi!"

class ButtonEmojis:
    BACK = "🔙"
    NEXT = "➡️"
    PREV = "⬅️"
    ADD = "➕"
    DELETE = "❌"
    EDIT = "✏️"
    CONFIRM = "✅"
    CANCEL = "🚫"
    SEARCH = "🔍"
    PLAY = "▶️"
    STOP = "⏹️"
    SETTINGS = "⚙️"
    INFO = "ℹ️"
    LIST = "📋"
    GROUP = "👥"
    CHART = "📊"
    SEND = "📤"
    DOWNLOAD = "📥"
    SAVE = "💾"

class DatabaseQueries:
    INSERT_USER = "INSERT INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)"
    INSERT_ANIME = "INSERT INTO anime (code, description, photo_id) VALUES (?, ?, ?)"
    INSERT_PART = "INSERT INTO anime_parts (anime_code, part_number, file_id) VALUES (?, ?, ?)"
    INSERT_GROUP = "INSERT INTO groups (group_id, link, name) VALUES (?, ?, ?)"
    
    SELECT_ANIME = "SELECT * FROM anime WHERE code = ?"
    SELECT_PARTS = "SELECT * FROM anime_parts WHERE anime_code = ? ORDER BY part_number ASC"
    SELECT_GROUPS = "SELECT * FROM groups ORDER BY created_at DESC"
    
    UPDATE_ANIME = "UPDATE anime SET description = ?, updated_at = CURRENT_TIMESTAMP WHERE code = ?"
    UPDATE_USER = "UPDATE users SET last_seen = CURRENT_TIMESTAMP WHERE user_id = ?"
    
    DELETE_ANIME = "DELETE FROM anime WHERE code = ?"
    DELETE_PART = "DELETE FROM anime_parts WHERE anime_code = ? AND part_number = ?"
    DELETE_GROUP = "DELETE FROM groups WHERE group_id = ?"

class AdminPanelOptions:
    ADD_ANIME = "add_anime"
    DELETE_ANIME = "delete_anime"
    EDIT_ANIME = "edit_anime"
    ADD_GROUP = "add_group"
    DELETE_GROUP = "delete_group"
    VIEW_GROUPS = "view_groups"
    STATS = "stats"
    BROADCAST = "broadcast"

class PaginationDefaults:
    ITEMS_PER_PAGE = 10
    MAX_INLINE_BUTTONS = 5
    MIN_PAGE = 1

class FileSize:
    MAX_VIDEO_SIZE = 2000000000
    MAX_PHOTO_SIZE = 5242880
    MAX_DOCUMENT_SIZE = 50000000

class ResponseMessages:
    WELCOME = "👋 Assalomualaikum! Anime izlash botiga xush kelibsiz!"
    SUBSCRIBE_REQUIRED = "🔒 Iltimos, quyidagi kanallarga obuna bo'ling:"
    ENTER_CODE = "📝 Anime kodini kiriting:"
    INVALID_CODE = "❌ Kod faqat raqam bo'lishi kerak!"
    NO_RESULTS = "❌ Qidirish natijasi topilmadi!"
    SELECT_PART = "🎬 Qism raqamini tanlang:"
    ADMIN_PANEL = "⚙️ Admin Panel"
    BROADCAST_CONFIRM = "📋 Xabarni tasdiqlang:"

class LogMessages:
    USER_JOINED = "Foydalanuvchi qo'shildi"
    USER_SEARCHED = "Qidirish bajarildi"
    ANIME_VIEWED = "Anime ko'rildi"
    PART_DOWNLOADED = "Qism ko'rildi"
    ADMIN_ACTION = "Admin amali bajarildi"
    BROADCAST_SENT = "Xabar yuborildi"
    ERROR_OCCURRED = "Xato yuz berdi"
    DATABASE_ERROR = "Ma'lumotlar bazasi xatosi"

ADMIN_ONLY = "⛔ Bu amalni faqat adminlar bajarishi mumkin!"
NOT_FOUND = "🔍 Axtarish natijasi topilmadi!"
RATE_LIMIT_ERROR = "⏱️ Juda ko'p so'rov yuborayotganingiz. Bir oz kutin!"
DATABASE_ERROR = "💔 Ma'lumotlar bazasida xato!"
