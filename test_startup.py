#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import threading
import time
import os

os.chdir(os.path.dirname(__file__))

print('[*] Testing bot startup...')
print('[*] Checking configuration...')

try:
    from config import TOKEN, ADMIN_ID, ADMIN_IDS
    print(f'[OK] Config loaded')
    print(f'    - ADMIN_ID: {ADMIN_ID}')
    print(f'    - ADMIN_IDS: {ADMIN_IDS}')
    print(f'    - TOKEN: {TOKEN[:20]}...' if TOKEN else '    - TOKEN: NOT SET')
except Exception as e:
    print(f'[ERROR] Config error: {e}')
    sys.exit(1)

print('[*] Testing database...')
try:
    from database import Database
    db = Database()
    users = db.get_all_users()
    print(f'[OK] Database connected ({len(users)} users)')
except Exception as e:
    print(f'[ERROR] Database error: {e}')
    sys.exit(1)

print('[*] Testing bot initialization...')
try:
    from bot import AnimeBot
    bot = AnimeBot()
    print('[OK] Bot initialized successfully')
except Exception as e:
    print(f'[ERROR] Bot initialization error: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)

print('[*] Testing main app...')
try:
    from main import AnimeBotMain
    print('[OK] Main app can be imported')
except Exception as e:
    print(f'[ERROR] Main app error: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)

print('')
print('[SUCCESS] All systems operational!')
print('[OK] Bot is ready to run with: python main.py')
