#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
os.chdir(os.path.dirname(__file__))

from database import Database

db = Database()

print("[*] Checking database...")
print()

print("[1] All users:")
users = db.get_all_users()
print(f"    Total: {len(users)}")
if users:
    for u in users[:3]:
        print(f"    - {u}")

print()
print("[2] All anime:")
anime_list = db.get_all_anime()
print(f"    Total: {len(anime_list)}")
if anime_list:
    for a in anime_list[:3]:
        print(f"    - Code: {a['code']}, Desc: {a['description'][:50] if a['description'] else 'No desc'}")

print()
print("[3] All groups:")
groups = db.get_all_groups()
print(f"    Total: {len(groups)}")
if groups:
    for g in groups[:3]:
        print(f"    - {g['name']} ({g['group_id']})")

print()
print("[4] Mandatory channels:")
channels = db.get_mandatory_channels()
print(f"    Total: {len(channels)}")
if channels:
    for c in channels[:3]:
        print(f"    - {c['name']} ({c['channel_id']})")

print()
print("[OK] Database check complete!")
