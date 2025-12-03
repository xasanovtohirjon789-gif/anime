import logging
import os
import re
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes
from telegram.error import TelegramError
from database import Database
from config import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

db = Database()

class AnimeBot:
    def __init__(self):
        try:
            self.app = Application.builder().token(TOKEN).build()
        except AttributeError:
            import asyncio
            self.app = Application.builder().token(TOKEN).build()
            asyncio.get_event_loop()
        self.setup_handlers()
        
    def setup_handlers(self):
        start_conv = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                1: [CallbackQueryHandler(self.check_subscription)],
                2: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.search_anime), CallbackQueryHandler(self.check_subscription)],
                3: [CallbackQueryHandler(self.view_anime_parts)],
                4: [CallbackQueryHandler(self.send_part)],
            },
            fallbacks=[CommandHandler("start", self.start)],
            per_message=False
        )
        
        admin_conv = ConversationHandler(
            entry_points=[CommandHandler("admin", self.admin_panel)],
            states={
                10: [CallbackQueryHandler(self.admin_choice)],
                11: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.add_anime_description)],
                12: [MessageHandler(filters.VIDEO | filters.PHOTO, self.add_anime_first_part)],
                13: [CallbackQueryHandler(self.add_more_parts)],
                14: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.add_anime_code)],
                15: [CallbackQueryHandler(self.select_groups_for_anime)],
                16: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.delete_anime_code)],
                17: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.edit_anime_code)],
                18: [CallbackQueryHandler(self.edit_anime_choice)],
                19: [MessageHandler(filters.VIDEO, self.add_new_part)],
                20: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.delete_part_number)],
                21: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.add_group_id)],
                22: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.add_group_link)],
                23: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.add_group_name)],
                24: [CallbackQueryHandler(self.select_group_to_delete)],
                25: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.edit_description_choice)],
                26: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.add_mandatory_channel_id)],
                27: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.add_mandatory_channel_link)],
                28: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.add_mandatory_channel_name)],
                29: [CallbackQueryHandler(self.delete_mandatory_channel_choice)],
            },
            fallbacks=[CommandHandler("admin", self.admin_panel), MessageHandler(filters.COMMAND, self.admin_panel)],
            per_message=False
        )
        
        self.app.add_handler(start_conv)
        self.app.add_handler(admin_conv)
        self.app.add_handler(CallbackQueryHandler(self.handle_verify_callback, pattern="^check_verify$"))
        self.app.add_handler(CallbackQueryHandler(self.handle_view_callback, pattern="^view$"))
        self.app.add_handler(CallbackQueryHandler(self.handle_page_callback, pattern="^page_"))
        self.app.add_handler(CallbackQueryHandler(self.handle_part_callback, pattern="^part_"))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_anime_code))
        self.app.add_handler(CommandHandler("help", self.help_command))
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_id = update.effective_user.id
        db.add_user(user_id)
        
        channels = db.get_mandatory_channels()
        if not channels:
            await update.message.reply_text("Hozircha majburiy obuna kanallari mavjud emas.")
            return ConversationHandler.END
        
        keyboard = [[InlineKeyboardButton(ch['name'], url=ch['link'])] for ch in channels]
        keyboard.append([InlineKeyboardButton("✅ Tekshirish", callback_data="check")])
        
        await update.message.reply_text(
            "👋 Assalomualaikum! Anime izlash botiga xush kelibsiz!\n\n"
            "📺 Quyidagi kanallarga obuna bo'ling:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return 1
    
    async def check_subscription(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        
        channels = db.get_mandatory_channels()
        not_subscribed = []
        
        for channel in channels:
            channel_id = channel['channel_id']
            try:
                channel_id = int(channel_id)
            except (ValueError, TypeError):
                pass
            
            is_member = False
            try:
                member = await context.bot.get_chat_member(channel_id, user_id)
                if member.status in ['member', 'administrator', 'creator']:
                    is_member = True
            except:
                pass
            
            if not is_member:
                not_subscribed.append(channel['name'])
        
        if not_subscribed:
            keyboard = [[InlineKeyboardButton("🔄 Qayta tekshirish", callback_data="check")]]
            await query.edit_message_text(
                f"❌ Siz ushbu kanallarga obuna bo'lmagansiz:\n" + "\n".join(not_subscribed),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return 1
        
        pending_code = context.user_data.get('pending_anime_code')
        if pending_code:
            context.user_data.pop('pending_anime_code', None)
            anime = db.get_anime_by_code(int(pending_code))
            if not anime:
                await query.edit_message_text(f"❌ Kod {pending_code} bo'yicha anime topilmadi!")
                return 2
            
            context.user_data['current_anime_code'] = anime['code']
            context.user_data['current_anime_id'] = anime['id']
            
            text = f"<b>{anime['description']}</b>" if anime['description'] else "Anime izohi"
            
            if anime['photo_id']:
                await query.edit_message_media(
                    media=anime['photo_id'],
                    caption=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🎬 Animeni ko'rish", callback_data="view")
                    ]])
                )
            else:
                await query.edit_message_text(
                    text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🎬 Animeni ko'rish", callback_data="view")
                    ]])
                )
            
            return 3
        
        await query.edit_message_text(
            "✅ Obuna tekshiruvi muvaffaqiyatli o'tdi!\n\n"
            "📝 Anime kodini kiriting:\n"
            "(Masalan: 12, 45, 100)"
        )
        return 2
    
    async def search_anime(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_id = update.effective_user.id
        code = update.message.text.strip()
        
        if not code.isdigit():
            await update.message.reply_text("❌ Kod faqat raqam bo'lishi kerak!")
            return 2
        
        channels = db.get_mandatory_channels()
        not_subscribed = []
        
        for channel in channels:
            channel_id = channel['channel_id']
            try:
                channel_id = int(channel_id)
            except (ValueError, TypeError):
                pass
            
            is_member = False
            try:
                member = await context.bot.get_chat_member(channel_id, user_id)
                if member.status in ['member', 'administrator', 'creator']:
                    is_member = True
            except:
                pass
            
            if not is_member:
                not_subscribed.append(channel)
        
        if not_subscribed:
            keyboard = [[InlineKeyboardButton(ch['name'], url=ch['link'])] for ch in not_subscribed]
            keyboard.append([InlineKeyboardButton("✅ Tekshirish", callback_data="check")])
            
            await update.message.reply_text(
                "❌ Yangi majburiy obuna kanallari qo'shilgan!\n\n"
                "📺 Quyidagi kanallarga obuna bo'ling:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            context.user_data['pending_anime_code'] = code
            return 2
        
        anime = db.get_anime_by_code(int(code))
        if not anime:
            await update.message.reply_text(f"❌ Kod {code} bo'yicha anime topilmadi!")
            return 2
        
        context.user_data['current_anime_code'] = anime['code']
        context.user_data['current_anime_id'] = anime['id']
        
        text = f"<b>{anime['description']}</b>" if anime['description'] else "Anime izohi"
        
        if anime['photo_id']:
            await update.message.reply_photo(
                photo=anime['photo_id'],
                caption=text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🎬 Animeni ko'rish", callback_data="view")
                ]])
            )
        else:
            await update.message.reply_text(
                text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🎬 Animeni ko'rish", callback_data="view")
                ]])
            )
        
        return 3
    
    async def view_anime_parts(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        anime_code = context.user_data.get('current_anime_code')
        if not anime_code:
            await query.edit_message_text("❌ Xato yuz berdi!")
            return 3
        
        context.user_data['current_page'] = 1
        return await self.show_parts_page(query, context, anime_code, 1)
    
    async def show_parts_page(self, query, context, anime_code, page):
        parts = db.get_anime_parts(anime_code)
        total_parts = len(parts)
        
        if total_parts == 0:
            await query.edit_message_text("❌ Bu animeda qism yo'q!")
            return 3
        
        parts_per_page = 10
        total_pages = (total_parts + parts_per_page - 1) // parts_per_page
        
        if page > total_pages:
            page = total_pages
        if page < 1:
            page = 1
        
        context.user_data['current_page'] = page
        
        start_idx = (page - 1) * parts_per_page
        end_idx = min(start_idx + parts_per_page, total_parts)
        page_parts = parts[start_idx:end_idx]
        
        keyboard = []
        for part in page_parts:
            part_num = part['part_number']
            keyboard.append(InlineKeyboardButton(str(part_num), callback_data=f"part_{part_num}"))
        
        keyboard = [keyboard[i:i+5] for i in range(0, len(keyboard), 5)]
        
        nav_buttons = []
        if page > 1:
            nav_buttons.append(InlineKeyboardButton("⬅ Chap", callback_data=f"page_{page-1}"))
        nav_buttons.append(InlineKeyboardButton(f"{page}/{total_pages}", callback_data="page_info"))
        if page < total_pages:
            nav_buttons.append(InlineKeyboardButton("O'ng ➡", callback_data=f"page_{page+1}"))
        keyboard.append(nav_buttons)
        
        text = f"📺 Qismlar ({start_idx+1}-{end_idx}/{total_parts}):\n\n" \
               f"Sahifa {page}/{total_pages}"
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return 4
    
    async def send_part(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        anime_code = context.user_data.get('current_anime_code')
        callback_data = query.data
        
        if callback_data.startswith("part_"):
            part_num = int(callback_data.split("_")[1])
            part = db.get_anime_part(anime_code, part_num)
            
            if part:
                await query.message.reply_video(part['file_id'])
            else:
                await query.answer("❌ Qism topilmadi!", show_alert=True)
            
            return 4
        
        elif callback_data.startswith("page_"):
            new_page = int(callback_data.split("_")[1])
            return await self.show_parts_page(query, context, anime_code, new_page)
        
        elif callback_data == "page_info":
            await query.answer()
            return 4
        
        return 4
    
    async def admin_panel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_id = update.effective_user.id
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("❌ Siz admin emassiz!")
            return ConversationHandler.END
        
        keyboard = [
            [InlineKeyboardButton("➕ Anime qo'shish", callback_data="add_anime")],
            [InlineKeyboardButton("❌ Anime o'chirish", callback_data="delete_anime")],
            [InlineKeyboardButton("✏️ Anime tahrirlash", callback_data="edit_anime")],
            [InlineKeyboardButton("➕ Guruh qo'shish", callback_data="add_group")],
            [InlineKeyboardButton("📋 Guruhlar ro'yxati", callback_data="groups_list")],
            [InlineKeyboardButton("❌ Guruh o'chirish", callback_data="delete_group")],
            [InlineKeyboardButton("📌 Obuna kanali qo'shish", callback_data="add_mandatory_channel")],
            [InlineKeyboardButton("❌ Obuna kanalini o'chirish", callback_data="delete_mandatory_channel")],
            [InlineKeyboardButton("🔙 Orqaga qaytish", callback_data="back")],
        ]
        
        await update.message.reply_text(
            "⚙️ Admin Paneli\n\nKerakli amalni tanlang:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return 10
    
    async def admin_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        choice = query.data
        logger.info(f"Admin choice: {choice}")
        
        if choice == "add_anime":
            await query.edit_message_text("📝 Anime izohini yuboring:\n(Rasm bilan yubora olasiz)")
            return 11
        elif choice == "delete_anime":
            await query.edit_message_text("🔍 O'chirish uchun anime kodini yuboring:")
            return 16
        elif choice == "edit_anime":
            await query.edit_message_text("🔍 Tahrirlash uchun anime kodini yuboring:")
            return 17
        elif choice == "add_group":
            await query.edit_message_text("📌 Guruh ID sini yuboring:\n(Masalan: -1001234567890)")
            return 21
        elif choice == "groups_list":
            return await self.show_groups_list(query)
        elif choice == "delete_group":
            return await self.show_delete_group(query)
        elif choice == "add_mandatory_channel":
            await query.edit_message_text("📌 Guruh/Kanal ID sini yuboring:\n(Masalan: -1001234567890)")
            return 26
        elif choice == "delete_mandatory_channel":
            return await self.show_delete_mandatory_channel(query)
        elif choice == "back":
            await query.delete_message()
            return ConversationHandler.END
        return 10
    
    async def add_anime_description(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        text = update.message.text if update.message.text else ""
        photo_id = None
        
        if update.message.photo:
            photo_id = update.message.photo[-1].file_id
        
        context.user_data['anime_description'] = text
        context.user_data['anime_photo_id'] = photo_id
        context.user_data['anime_parts'] = []
        
        await update.message.reply_text(
            "🎬 1-qismning videosini yuboring:"
        )
        return 12
    
    async def add_anime_first_part(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if update.message.video:
            file_id = update.message.video.file_id
        elif update.message.document:
            file_id = update.message.document.file_id
        else:
            await update.message.reply_text("❌ Video turini qabul qilaman!")
            return 12
        
        context.user_data['anime_parts'].append({
            'part_number': 1,
            'file_id': file_id
        })
        
        keyboard = [
            [InlineKeyboardButton("✅ Ha", callback_data="add_more_yes")],
            [InlineKeyboardButton("❌ Yo'q", callback_data="add_more_no")]
        ]
        
        await update.message.reply_text(
            "❓ Yana qism qo'shasizmi?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return 13
    
    async def add_more_parts(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        if query.data == "add_more_yes":
            part_num = len(context.user_data['anime_parts']) + 1
            await query.edit_message_text(
                f"🎬 {part_num}-qismning videosini yuboring:"
            )
            return 12
        
        else:
            await query.edit_message_text(
                "📝 Anime kodingizni kiriting:\n"
                "(Faqat raqam, masalan: 12)"
            )
            return 14
    
    async def add_anime_code(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        code = update.message.text.strip()
        
        if not code.isdigit():
            await update.message.reply_text(
                "❌ Kod faqat raqam bo'lishi kerak!\n"
                "Qayta yuboring:"
            )
            return 14
        
        code = int(code)
        
        if db.get_anime_by_code(code):
            await update.message.reply_text(
                f"❌ Kod {code} allaqachon mavjud!\n"
                "Boshqa kod kiriting:"
            )
            return 14
        
        context.user_data['anime_code'] = code
        
        groups = db.get_all_groups()
        if not groups:
            db.add_anime(
                code=code,
                description=context.user_data['anime_description'],
                photo_id=context.user_data['anime_photo_id'],
                parts=context.user_data['anime_parts']
            )
            
            await update.message.reply_text(
                f"✅ Anime muvaffaqiyatli qo'shildi!\n"
                f"Kod: {code}"
            )
            return ConversationHandler.END
        
        keyboard = [[InlineKeyboardButton(g['name'], callback_data=f"group_{g['id']}")] for g in groups]
        keyboard.append([InlineKeyboardButton("✅ Tugatish", callback_data="groups_done")])
        
        await update.message.reply_text(
            "📍 Bu animeni qaysi guruhlarga tashlayman?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return 15
    
    async def select_groups_for_anime(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        if query.data == "groups_done":
            code = context.user_data['anime_code']
            description = context.user_data['anime_description']
            photo_id = context.user_data['anime_photo_id']
            parts = context.user_data['anime_parts']
            groups = context.user_data.get('selected_groups', [])
            
            db.add_anime(
                code=code,
                description=description,
                photo_id=photo_id,
                parts=parts,
                groups=groups
            )
            
            await query.edit_message_text(
                f"✅ Anime muvaffaqiyatli qo'shildi!\n"
                f"Kod: {code}\n"
                f"Qismlar: {len(parts)}\n"
                f"Guruhlar: {len(groups)}"
            )
            return ConversationHandler.END
        
        group_id = int(query.data.split("_")[1])
        
        if 'selected_groups' not in context.user_data:
            context.user_data['selected_groups'] = []
        
        if group_id not in context.user_data['selected_groups']:
            context.user_data['selected_groups'].append(group_id)
        
        return 15
    
    async def delete_anime_code(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        code = update.message.text.strip()
        
        if not code.isdigit():
            await update.message.reply_text("❌ Kod faqat raqam bo'lishi kerak!")
            return 16
        
        code = int(code)
        anime = db.get_anime_by_code(code)
        
        if not anime:
            await update.message.reply_text(f"❌ Kod {code} topilmadi!")
            return 16
        
        db.delete_anime(code)
        await update.message.reply_text(
            f"✅ Anime muvaffaqiyatli o'chirildi!\n"
            f"Kod: {code}"
        )
        return ConversationHandler.END
    
    async def edit_anime_code(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        code = update.message.text.strip()
        
        if not code.isdigit():
            await update.message.reply_text("❌ Kod faqat raqam bo'lishi kerak!")
            return 17
        
        code = int(code)
        anime = db.get_anime_by_code(code)
        
        if not anime:
            await update.message.reply_text(f"❌ Kod {code} topilmadi!")
            return 17
        
        context.user_data['edit_anime_code'] = code
        
        keyboard = [
            [InlineKeyboardButton("➕ Qism qo'shish", callback_data="edit_add_part")],
            [InlineKeyboardButton("❌ Qism o'chirish", callback_data="edit_delete_part")],
            [InlineKeyboardButton("🗑️ Animeni o'chirish", callback_data="edit_delete_anime")],
            [InlineKeyboardButton("✏️ Izohni o'zgartirish", callback_data="edit_description")],
        ]
        
        await update.message.reply_text(
            f"📝 Anime: {anime['description'][:50]}...\n\n"
            "Kerakli amalni tanlang:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return 18
    
    async def edit_anime_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        code = context.user_data['edit_anime_code']
        
        if query.data == "edit_add_part":
            await query.edit_message_text("🎬 Yangi video yuboring:")
            return 19
        
        elif query.data == "edit_delete_part":
            parts = db.get_anime_parts(code)
            if not parts:
                await query.answer("❌ Qismlar yo'q!", show_alert=True)
                return 18
            
            await query.edit_message_text(
                f"🔍 O'chirish uchun qism raqamini yuboring:\n"
                f"(1-{len(parts)})"
            )
            return 20
        
        elif query.data == "edit_delete_anime":
            db.delete_anime(code)
            await query.edit_message_text("✅ Anime muvaffaqiyatli o'chirildi!")
            return ConversationHandler.END
        
        elif query.data == "edit_description":
            anime = db.get_anime_by_code(code)
            await query.edit_message_text(
                f"📝 Eski izoh:\n{anime['description']}\n\n"
                "Yangi izohni yuboring:"
            )
            return 25
        
        return 18
    
    async def add_new_part(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        code = context.user_data['edit_anime_code']
        parts = db.get_anime_parts(code)
        next_part_num = len(parts) + 1
        
        if update.message.video:
            file_id = update.message.video.file_id
        elif update.message.document:
            file_id = update.message.document.file_id
        else:
            await update.message.reply_text("❌ Video turini qabul qilaman!")
            return 19
        
        db.add_anime_part(code, next_part_num, file_id)
        
        keyboard = [
            [InlineKeyboardButton("✅ Ha", callback_data="edit_desc_yes")],
            [InlineKeyboardButton("❌ Yo'q", callback_data="edit_desc_no")]
        ]
        
        await update.message.reply_text(
            f"✅ {next_part_num}-qism qo'shildi!\n\n"
            "❓ Izohni o'zgartirasizmi?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return 25
    
    async def delete_part_number(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        code = context.user_data['edit_anime_code']
        
        try:
            part_num = int(update.message.text.strip())
        except:
            await update.message.reply_text("❌ Faqat raqam yuboring!")
            return 20
        
        parts = db.get_anime_parts(code)
        if part_num < 1 or part_num > len(parts):
            await update.message.reply_text(f"❌ Qism 1-{len(parts)} orasida bo'lishi kerak!")
            return 20
        
        db.delete_anime_part(code, part_num)
        
        await update.message.reply_text(
            f"✅ {part_num}-qism o'chirildi!"
        )
        return ConversationHandler.END
    
    async def add_group_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        group_id = update.message.text.strip()
        
        if not group_id.lstrip('-').isdigit():
            await update.message.reply_text("❌ Faqat raqam yuboring!")
            return 21
        
        context.user_data['group_id'] = int(group_id)
        
        await update.message.reply_text(
            "🔗 Guruh linkini yuboring:\n"
            "(Masalan: https://t.me/animeler)"
        )
        return 22
    
    async def add_group_link(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        link = update.message.text.strip()
        
        context.user_data['group_link'] = link
        
        await update.message.reply_text(
            "📝 Guruh nomini yuboring:\n"
            "(Masalan: Anime Dunyosi)"
        )
        return 23
    
    async def add_group_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        name = update.message.text.strip()
        
        group_id = context.user_data['group_id']
        link = context.user_data['group_link']
        
        db.add_group(group_id, link, name)
        
        await update.message.reply_text(
            f"✅ Guruh qo'shildi!\n"
            f"ID: {group_id}\n"
            f"Nomi: {name}"
        )
        return ConversationHandler.END
    
    async def show_groups_list(self, query) -> int:
        groups = db.get_all_groups()
        
        if not groups:
            await query.edit_message_text("📋 Hozircha guruh yo'q!")
            return 10
        
        text = "📋 Guruhlar ro'yxati:\n\n"
        for group in groups:
            text += f"• {group['name']}\n"
            text += f"  🔗 {group['link']}\n"
            text += f"  ID: {group['group_id']}\n\n"
        
        await query.edit_message_text(text)
        return 10
    
    async def show_delete_group(self, query) -> int:
        groups = db.get_all_groups()
        
        if not groups:
            await query.answer("❌ Guruh yo'q!", show_alert=True)
            return 10
        
        keyboard = [[InlineKeyboardButton(g['name'], callback_data=f"del_group_{g['id']}")] for g in groups]
        keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back")])
        
        await query.edit_message_text(
            "❌ O'chirish uchun guruhni tanlang:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return 24
    
    async def select_group_to_delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        if query.data == "back":
            await query.delete_message()
            return ConversationHandler.END
        
        group_id = int(query.data.split("_")[2])
        db.delete_group(group_id)
        
        await query.answer("✅ Guruh o'chirildi!")
        return 24
    
    async def edit_description_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        code = context.user_data['edit_anime_code']
        new_description = update.message.text.strip()
        
        db.update_anime_description(code, new_description)
        
        await update.message.reply_text(
            "✅ Izoh o'zgartirildi!"
        )
        return ConversationHandler.END
    
    async def add_mandatory_channel_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        channel_id = update.message.text.strip()
        
        try:
            int(channel_id)
        except ValueError:
            await update.message.reply_text(
                "❌ Noto'g'ri ID! Raqamlardan iborat ID yuboring.\n"
                "Qayta urinib ko'ring:"
            )
            return 26
        
        context.user_data['mandatory_channel_id'] = channel_id
        
        await update.message.reply_text(
            "🔗 Guruh/Kanal silkasini yuboring:\n"
            "(Masalan: https://t.me/+yWlBa7lZF9tlN2M6)"
        )
        return 27
    
    async def add_mandatory_channel_link(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        link = update.message.text.strip()
        
        context.user_data['mandatory_channel_link'] = link
        
        await update.message.reply_text(
            "📝 Guruh/Kanal nomini yuboring:\n"
            "(Masalan: ANITOX CHANEL)"
        )
        return 28
    
    async def add_mandatory_channel_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        name = update.message.text.strip()
        
        channel_id = context.user_data['mandatory_channel_id']
        link = context.user_data['mandatory_channel_link']
        
        db.add_mandatory_channel(channel_id, link, name)
        
        await update.message.reply_text(
            f"✅ Obuna kanali qo'shildi!\n"
            f"ID: {channel_id}\n"
            f"Silka: {link}\n"
            f"Nomi: {name}\n\n"
            f"📌 Barcha foydalanuvchilar ushbu kanalga obuna bo'lishi kerak!"
        )
        return ConversationHandler.END
    
    async def show_delete_mandatory_channel(self, query) -> int:
        channels = db.get_mandatory_channels()
        
        if not channels:
            await query.edit_message_text("📌 Majburiy obuna kanallari yo'q!")
            return 10
        
        keyboard = [[InlineKeyboardButton(ch['name'], callback_data=f"del_mand_ch_{ch['id']}")] for ch in channels]
        keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back")])
        
        await query.edit_message_text(
            "❌ Qaysi kanalni o'chirmoqchisiz:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return 29
    
    async def delete_mandatory_channel_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        if query.data == "back":
            await query.delete_message()
            return ConversationHandler.END
        
        channel_id = int(query.data.split("_")[3])
        db.delete_mandatory_channel(channel_id)
        
        await query.answer("✅ Kanal o'chirildi!")
        return 29
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        help_text = """
🎬 Anime Bot - Komandalari:

/start - Botni ishga tushirish
/help - Yordam

👤 Foydalanuvchi uchun:
1. Majburiy kanallarga obuna bo'ling
2. Tekshirish tugmasini bosing
3. Anime kodini kiriting
4. Qismlarni o'rtasidan tanlang

⚙️ Admin uchun:
/admin - Admin panelini ochish

Admin panelida:
✔ Anime qo'shish/o'chirish/tahrirlash
✔ Guruh boshqaruvi
        """
        await update.message.reply_text(help_text)
    
    async def handle_anime_code(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_id = update.effective_user.id
        code = update.message.text.strip()
        
        if not code.isdigit():
            return
        
        db.add_user(user_id)
        
        channels = db.get_mandatory_channels()
        not_subscribed = []
        
        for channel in channels:
            channel_id = channel['channel_id']
            try:
                channel_id = int(channel_id)
            except (ValueError, TypeError):
                pass
            
            is_member = False
            try:
                member = await context.bot.get_chat_member(channel_id, user_id)
                if member.status in ['member', 'administrator', 'creator']:
                    is_member = True
            except:
                pass
            
            if not is_member:
                not_subscribed.append(channel)
        
        if not_subscribed:
            keyboard = [[InlineKeyboardButton(ch['name'], url=ch['link'])] for ch in not_subscribed]
            keyboard.append([InlineKeyboardButton("✅ Tekshirish", callback_data="check_verify")])
            
            await update.message.reply_text(
                "❌ Majburiy obuna kanallari topilmadi!\n\n"
                "📺 Quyidagi kanallarga obuna bo'ling:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            context.user_data['pending_anime_code'] = code
            return
        
        anime = db.get_anime_by_code(int(code))
        if not anime:
            await update.message.reply_text(f"❌ Kod {code} bo'yicha anime topilmadi!")
            return
        
        context.user_data['current_anime_code'] = anime['code']
        context.user_data['current_anime_id'] = anime['id']
        
        text = f"<b>{anime['description']}</b>" if anime['description'] else "Anime izohi"
        
        if anime['photo_id']:
            await update.message.reply_photo(
                photo=anime['photo_id'],
                caption=text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🎬 Animeni ko'rish", callback_data="view")
                ]])
            )
        else:
            await update.message.reply_text(
                text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🎬 Animeni ko'rish", callback_data="view")
                ]])
            )
    
    async def handle_verify_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        
        channels = db.get_mandatory_channels()
        not_subscribed = []
        
        for channel in channels:
            channel_id = channel['channel_id']
            try:
                channel_id = int(channel_id)
            except (ValueError, TypeError):
                pass
            
            is_member = False
            try:
                member = await context.bot.get_chat_member(channel_id, user_id)
                if member.status in ['member', 'administrator', 'creator']:
                    is_member = True
            except:
                pass
            
            if not is_member:
                not_subscribed.append(channel['name'])
        
        if not_subscribed:
            keyboard = [[InlineKeyboardButton("🔄 Qayta tekshirish", callback_data="check_verify")]]
            await query.edit_message_text(
                f"❌ Siz ushbu kanallarga obuna bo'lmagansiz:\n" + "\n".join(not_subscribed),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return
        
        pending_code = context.user_data.get('pending_anime_code')
        if pending_code:
            context.user_data.pop('pending_anime_code', None)
            anime = db.get_anime_by_code(int(pending_code))
            if not anime:
                await query.edit_message_text(f"❌ Kod {pending_code} bo'yicha anime topilmadi!")
                return
            
            context.user_data['current_anime_code'] = anime['code']
            context.user_data['current_anime_id'] = anime['id']
            
            text = f"<b>{anime['description']}</b>" if anime['description'] else "Anime izohi"
            
            if anime['photo_id']:
                await query.edit_message_media(
                    media=anime['photo_id'],
                    caption=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🎬 Animeni ko'rish", callback_data="view")
                    ]])
                )
            else:
                await query.edit_message_text(
                    text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🎬 Animeni ko'rish", callback_data="view")
                    ]])
                )
        else:
            await query.edit_message_text(
                "✅ Obuna tekshiruvi muvaffaqiyatli o'tdi!\n\n"
                "📝 Anime kodini kiriting:\n"
                "(Masalan: 12, 45, 100)"
            )
    
    async def handle_view_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        
        anime_code = context.user_data.get('current_anime_code')
        if not anime_code:
            await query.answer("❌ Xato yuz berdi!", show_alert=True)
            return
        
        context.user_data['current_page'] = 1
        await self.show_parts_page(query, context, anime_code, 1)
    
    async def handle_page_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        
        anime_code = context.user_data.get('current_anime_code')
        if not anime_code:
            await query.answer("❌ Xato yuz berdi!", show_alert=True)
            return
        
        callback_data = query.data
        if callback_data == "page_info":
            await query.answer("Sahifa ma'lumoti", show_alert=False)
            return
        
        page = int(callback_data.split("_")[1])
        await self.show_parts_page(query, context, anime_code, page)
    
    async def handle_part_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        
        anime_code = context.user_data.get('current_anime_code')
        callback_data = query.data
        
        if callback_data.startswith("part_"):
            part_num = int(callback_data.split("_")[1])
            part = db.get_anime_part(anime_code, part_num)
            
            if part:
                await query.message.reply_video(part['file_id'])
            else:
                await query.answer("❌ Qism topilmadi!", show_alert=True)
    
    def run(self):
        self.app.run_polling()

if __name__ == '__main__':
    bot = AnimeBot()
    bot.run()
