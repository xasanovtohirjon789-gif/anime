#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
os.chdir(os.path.dirname(__file__))

from database import Database

db = Database()

print("[*] Adding test data to database...")
print()

print("[1] Adding mandatory channels...")
db.add_mandatory_channel(
    -1002179331541,
    "https://t.me/+yWlBa7lZF9tlN2M6",
    "ANITOX CHANEL"
)
print("    [OK] Mandatory channel added")

print()
print("[2] Adding groups...")
db.add_group(-1001234567890, "https://t.me/anime_group_1", "Anime Guruh 1")
db.add_group(-1001234567891, "https://t.me/anime_group_2", "Anime Guruh 2")
print("    [OK] 2 groups added")

print()
print("[3] Adding anime...")
anime_data = [
    {
        "code": 1001,
        "description": "Naruto - Ninja Jang'ami Hikayasi",
        "parts": [
            {"part_number": 1, "file_id": "AgACAgIAAxkBAAIBZmdhZ2JkdGp1ZWZ5VmFqZWp6WU4rAAIAqjEbm7RN"},
            {"part_number": 2, "file_id": "AgACAgIAAxkBAAIBZmdhZ2JkdGp1ZWZ5VmFqZWp6WU4rAAIAqjEbm7RN"}
        ],
        "groups": [1, 2]
    },
    {
        "code": 1002,
        "description": "One Piece - Dengiz Piratlari",
        "parts": [
            {"part_number": 1, "file_id": "AgACAgIAAxkBAAIBZmdhZ2JkdGp1ZWZ5VmFqZWp6WU4rAAIAqjEbm7RN"},
        ],
        "groups": [1]
    },
    {
        "code": 1003,
        "description": "Dragon Ball - Zumaralarning Jang'ami",
        "parts": [
            {"part_number": 1, "file_id": "AgACAgIAAxkBAAIBZmdhZ2JkdGp1ZWZ5VmFqZWp6WU4rAAIAqjEbm7RN"},
        ],
        "groups": [2]
    }
]

for anime in anime_data:
    db.add_anime(
        code=anime["code"],
        description=anime["description"],
        photo_id=None,
        parts=anime["parts"],
        groups=anime["groups"]
    )
    print(f"    [OK] Anime {anime['code']} added: {anime['description']}")

print()
print("[OK] Test data added successfully!")
print()
print("Database status:")
print(f"  - Anime: {db.get_total_anime_count()}")
print(f"  - Parts: {db.get_total_parts_count()}")
print(f"  - Groups: {len(db.get_all_groups())}")
print(f"  - Channels: {len(db.get_mandatory_channels())}")
