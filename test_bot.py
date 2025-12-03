import asyncio
import sys
from pathlib import Path

def test_imports():
    print("🔍 Testing imports...")
    try:
        from telegram import Update, Bot
        print("  ✅ python-telegram-bot")
    except ImportError as e:
        print(f"  ❌ python-telegram-bot: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("  ✅ python-dotenv")
    except ImportError as e:
        print(f"  ❌ python-dotenv: {e}")
        return False
    
    try:
        from database import Database
        print("  ✅ database module")
    except ImportError as e:
        print(f"  ❌ database module: {e}")
        return False
    
    try:
        from bot import AnimeBot
        print("  ✅ bot module")
    except ImportError as e:
        print(f"  ❌ bot module: {e}")
        return False
    
    return True

def test_config():
    print("\n🔍 Testing configuration...")
    try:
        from config import TOKEN, ADMIN_IDS
        
        if TOKEN == 'YOUR_BOT_TOKEN_HERE' or not TOKEN:
            print("  ❌ TOKEN not configured!")
            return False
        
        print(f"  ✅ TOKEN: {TOKEN[:10]}...")
        
        if not ADMIN_IDS:
            print("  ⚠️  Warning: No admin IDs configured")
        else:
            print(f"  ✅ ADMIN_IDS: {len(ADMIN_IDS)} admin(s)")
        
        return True
    except ImportError as e:
        print(f"  ❌ Config error: {e}")
        return False

def test_database():
    print("\n🔍 Testing database...")
    try:
        from database import Database
        
        db = Database()
        print("  ✅ Database connection")
        
        anime_count = db.get_total_anime_count()
        print(f"  ✅ Anime count: {anime_count}")
        
        groups = db.get_all_groups()
        print(f"  ✅ Groups: {len(groups)}")
        
        return True
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        return False

async def test_bot_connection():
    print("\n🔍 Testing bot connection...")
    try:
        from config import TOKEN
        from telegram import Bot
        
        bot = Bot(token=TOKEN)
        me = await bot.get_me()
        
        print(f"  ✅ Bot connected: @{me.username}")
        print(f"  ✅ Bot ID: {me.id}")
        print(f"  ✅ Bot name: {me.first_name}")
        
        return True
    except Exception as e:
        print(f"  ❌ Connection failed: {e}")
        return False

def test_files():
    print("\n🔍 Testing required files...")
    
    required_files = [
        'bot.py',
        'database.py',
        'config.py',
        'main.py',
        'requirements.txt',
        '.env' or '.env.example'
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - NOT FOUND")
            return False
    
    return True

def test_directories():
    print("\n🔍 Testing directories...")
    
    required_dirs = ['logs', 'backups', 'exports']
    
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ⚠️  {dir_name}/ - creating...")
            Path(dir_name).mkdir(exist_ok=True)
            print(f"  ✅ {dir_name}/ - created")
    
    return True

async def run_all_tests():
    print("""
╔════════════════════════════════════════╗
║      🤖 Anime Bot Test Suite          ║
╚════════════════════════════════════════╝
""")
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Files", test_files()))
    results.append(("Directories", test_directories()))
    results.append(("Database", test_database()))
    results.append(("Bot Connection", await test_bot_connection()))
    
    print("\n" + "="*40)
    print("📊 Test Results:")
    print("="*40)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        if result:
            print(f"✅ {test_name}: PASSED")
            passed += 1
        else:
            print(f"❌ {test_name}: FAILED")
            failed += 1
    
    print("="*40)
    print(f"\n📈 Summary: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n✅ All tests passed! Bot is ready to run.")
        print("   Run: python main.py")
        return True
    else:
        print(f"\n❌ {failed} test(s) failed. Please fix the issues.")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(run_all_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
