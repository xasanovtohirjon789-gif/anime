#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

os.chdir(os.path.dirname(__file__))

try:
    from bot import AnimeBot
    from main import AnimeBotMain
    from database import Database
    from config import ADMIN_ID, ADMIN_IDS, TOKEN
    from handlers import GeneralHandlers
    from admin_utils import AdminUtils
    from utils import ValidationUtils
    
    print('[OK] All imports successful')
    print(f'[OK] ADMIN_ID: {ADMIN_ID}')
    print(f'[OK] ADMIN_IDS: {ADMIN_IDS}')
    print(f'[OK] TOKEN loaded: {bool(TOKEN)}')
    print('[OK] Database initialized')
    print('[OK] All modules loaded correctly')
except Exception as e:
    print(f'[ERROR] Import error: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
