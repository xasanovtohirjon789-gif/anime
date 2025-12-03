import os
import sys
import sqlite3
from pathlib import Path

def create_directories():
    directories = [
        'logs',
        'uploads',
        'backups',
        'exports'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Papka yaratildi: {directory}")

def init_database():
    try:
        from database import Database
        db = Database()
        print("✅ Ma'lumotlar bazasi ishga tushirildi")
        return True
    except Exception as e:
        print(f"❌ Ma'lumotlar bazasi xatosi: {e}")
        return False

def check_env_file():
    env_file = '.env'
    
    if not os.path.exists(env_file):
        print("⚠️ .env fayli topilmadi!")
        print("📝 .env.example faylidan nusxa oling va TOKEN qo'shing:")
        print("   cp .env.example .env")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
        
        if 'YOUR_BOT_TOKEN_HERE' in content or 'TOKEN=' not in content:
            print("❌ TOKEN sozlanmagan!")
            return False
    
    print("✅ .env fayli tekshirildi")
    return True

def check_dependencies():
    try:
        import telegram
        print("✅ python-telegram-bot o'rnatilgan")
    except:
        print("❌ python-telegram-bot o'rnatilmagan")
        print("   pip install python-telegram-bot")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv o'rnatilgan")
    except:
        print("❌ python-dotenv o'rnatilmagan")
        print("   pip install python-dotenv")
        return False
    
    return True

def setup_admin_ids():
    from config import ADMIN_IDS
    
    if not ADMIN_IDS or ADMIN_IDS == [123456789, 987654321]:
        print("⚠️ ADMIN_IDS sozlanmagan!")
        print("📝 config.py faylida ADMIN_IDS qo'shing")
        return False
    
    print(f"✅ Admin ID'lar sozlandi: {ADMIN_IDS}")
    return True

def test_bot_connection():
    try:
        from config import TOKEN
        import asyncio
        from telegram import Bot
        
        async def test():
            bot = Bot(token=TOKEN)
            me = await bot.get_me()
            print(f"✅ Bot ulanishi muvaffaqiyatli!")
            print(f"   Bot nomi: @{me.username}")
            return True
        
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(test())
        return result
    except Exception as e:
        print(f"❌ Bot ulanishida xato: {e}")
        return False

def create_admin_script():
    script_content = '''#!/usr/bin/env python3

import asyncio
from telegram import Bot
from config import TOKEN, ADMIN_IDS
from database import Database

async def init_admin():
    db = Database()
    
    print("\\n=== Admin Paneli Sozlash ===\\n")
    
    print(f"Admin ID'lar: {ADMIN_IDS}")
    
    channels_count = len(db.get_mandatory_channels())
    print(f"Majburiy kanallar: {channels_count}")
    
    groups_count = len(db.get_all_groups())
    print(f"Guruhlar: {groups_count}")
    
    print("\\n✅ Sozlash tugadi!\\n")

if __name__ == "__main__":
    asyncio.run(init_admin())
'''
    
    with open('admin_init.py', 'w') as f:
        f.write(script_content)
    
    print("✅ admin_init.py yaratildi")

def main():
    print("""
╔════════════════════════════════════════╗
║      🤖 Anime Bot Sozlanishi        ║
╚════════════════════════════════════════╝
""")
    
    print("1️⃣ Papkalar tekshirilmoqda...")
    create_directories()
    
    print("\\n2️⃣ .env fayli tekshirilmoqda...")
    if not check_env_file():
        print("\\n⚠️ Iltimos .env faylini sozlang va qayta ishlating")
        return False
    
    print("\\n3️⃣ Kutubxonalar tekshirilmoqda...")
    if not check_dependencies():
        print("\\n❌ Quyidagi buyruqni ishlating:")
        print("pip install -r requirements.txt")
        return False
    
    print("\\n4️⃣ Ma'lumotlar bazasi ishga tushirilmoqda...")
    if not init_database():
        return False
    
    print("\\n5️⃣ Admin ID'lari tekshirilmoqda...")
    if not setup_admin_ids():
        return False
    
    print("\\n6️⃣ Bot ulanishi sinovdan o'tmoqda...")
    if not test_bot_connection():
        return False
    
    print("\\n7️⃣ Admin skripti yaratilmoqda...")
    create_admin_script()
    
    print("""
╔════════════════════════════════════════╗
║     ✅ Sozlash Muvaffaqiyatli!       ║
╚════════════════════════════════════════╝

Botni ishga tushirish uchun:
  python main.py

O'rinli yo'l:
  python main.py &

Admin panelini tekshirish:
  /admin koandini yuboring
""")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
