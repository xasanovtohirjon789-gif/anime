#!/usr/bin/env python3
import subprocess
import sys

print("🚀 Anime Bot - Quick Start")
print("=" * 50)

packages = [
    "python-telegram-bot==20.7",
    "python-dotenv",
    "requests",
    "aiohttp"
]

print("\n📦 Installing dependencies...")
for pkg in packages:
    print(f"   Installing {pkg}...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", pkg])

print("\n✅ All dependencies installed!")
print("\n🤖 Starting bot...")
print("=" * 50)

try:
    from main import AnimeBotMain
    bot = AnimeBotMain()
    bot.run()
except KeyboardInterrupt:
    print("\n\n❌ Bot stopped by user")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
