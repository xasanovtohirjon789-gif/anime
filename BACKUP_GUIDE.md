# 💾 Backup va Data Persistence Guide

## 🔐 Data Xavfsizligi - 3 Qavatli Tizim

### ✅ Qatat 1: SQLite Doimiy Saqlash (Asosiy)
```
Bot restart → Database saqlanib qoladi
Kod o'zgartirilsa → Hamma data xavfsiz
Process crash → Data intact
```

**Fayllar:**
- `anime_bot.db` - Asosiy database (doimiy)
- `user_history.db` - Tarix (doimiy)

---

### ✅ Qatat 2: Avtomatik JSON Backup
Bot ishga tushganda avtomatik backup:
```
backups/anime_backup_20240101_120000.json
```

**Nima saqlanadi:**
- ✅ Barcha animelari (kod + izoh + foto)
- ✅ Barcha videolar (file ID'lari)
- ✅ Barcha guruhlar
- ✅ Barcha foydalanuvchilar
- ✅ Yaratilgan vaqti

---

### ✅ Qatat 3: Manual Backup Komandalar

## 🛠️ Backup Komandalar

### 1. Telegram dan `/backup` yuboring
```
Admin: /backup
Bot: "✅ Backup Tugadi!"
   - Database: backups/anime_bot_20240101_120000.db
   - JSON: backups/anime_backup_20240101_120000.json
```

Barcha animelari, videolar va izohlar saqlanadi! 💾

### 2. Buyruq qatoridan backup
```bash
# JSON export
python database_backup.py export

# Lengthening backup (Database + JSON)
python database_backup.py full

# Backuplar ro'yxati
python database_backup.py list

# JSON'dan import
python database_backup.py import backups/anime_backup_20240101.json
```

---

## 📊 Backup Fayllar Tuzilishi

### Database Backup (.db)
```
anime_bot_20240101_120000.db
├── users table
├── anime table
├── anime_parts table
├── groups table
└── user_history table
```

SQLite binary format, zichroq va tez.

### JSON Backup (.json)
```json
{
  "backup_timestamp": "2024-01-01T12:00:00",
  "anime": [
    {
      "id": 1,
      "code": 1,
      "description": "Anime izoh",
      "photo_id": "file_id",
      "parts": [
        {
          "part_number": 1,
          "file_id": "video_file_id"
        }
      ]
    }
  ],
  "groups": [...],
  "users": [...]
}
```

O'qish va tahrirlash oson.

---

## 🔄 Data Talab Qilinadigan Operatsiyalar

### Kod O'zgartirishida
```
1. Bot ishga tushadi
2. Avtomatik backup yaratiladi ✅
3. Database inicializatsiya
4. Hamma data saqlanib qoladi ✅
5. Bot ishlashni davom etadi
```

### Bot Qayta Ishga Tushganda
```
1. Database ulanadi
2. Tables tekshiriladi (agar yo'q → yaratiladi)
3. Hamma eski data saqlanib qoladi ✅
4. Yangi data qo'shilishi mumkin
```

### Server Crash'da
```
1. Database file xavfsiz (disk'da)
2. JSON backup disk'da
3. Bot restart
4. Hamma ma'lumot qaytadi ✅
```

---

## 🚀 Restore (Qaytarish)

### Database'dan Restore

```bash
# Eski backup'dan qaytarish
cp backups/anime_bot_20240101_120000.db anime_bot.db
python main.py
```

### JSON'dan Restore

```python
from database_backup import DatabaseBackup

backup = DatabaseBackup()
backup.import_from_json('backups/anime_backup_20240101.json')
```

Yoki:
```bash
python database_backup.py import backups/anime_backup_20240101.json
```

---

## 📋 Backup Sheduli (Tavsiya)

| Vaqt | Amal | Foyda |
|------|------|-------|
| Bot start | Avtomatik JSON | Har ishga tushganda |
| Har hafta | `/backup` | Qo'shimcha xavfsizlik |
| Har oy | Manual full backup | Arxiv |
| Critical update | Pre-update backup | Eski holga qaytarish |

---

## 🗄️ Backup Storage

### Lokal Storage
```
backups/
├── anime_bot_20240101_120000.db
├── anime_bot_20240102_120000.db
├── anime_backup_20240101_120000.json
└── anime_backup_20240102_120000.json
```

Disk joyini kuzating! 📊

### Cloud Storage (Optional)
```bash
# Google Drive'ga backup
cp backups/anime_bot_*.db /path/to/drive

# AWS S3'ga
aws s3 cp backups/ s3://my-backup/ --recursive

# Dropbox'ga
cp backups/*.* ~/Dropbox/anime-bot-backups/
```

---

## 🔍 Backup Tekshirish

### Backup Holati Ko'rish
```bash
python database_backup.py list
```

Natija:
```
📦 backups/anime_bot_20240101_120000.db
   Size: 245.3 KB
   Animeler: 50
   Guruhlar: 3

📦 backups/anime_backup_20240101_120000.json
   Size: 180.5 KB
   Animeler: 50
```

### Database Integrity Tekshirish
```bash
sqlite3 anime_bot.db "PRAGMA integrity_check;"
```

Agar "ok" bo'lsa - data xavfsiz! ✅

---

## ⚠️ Muhim Eslatmalar

1. **Database Ulanish Vaqtida**
   - Database boshqa process'da ochilmagan bo'lishi kerak
   - `anime_bot.db` faylini kesish yo'q!

2. **JSON Backup Hajmi**
   - Katta video'lar file_id sifatida saqlanadi
   - JSON fayl 1-100 MB orasida

3. **Taqdim Etilgan Backup**
   - Haftada birasa yangi backup qo'shishni tavsiya qilamiz
   - Eski backuplar o'chirib qo'ying (3 oydan ko'p)

4. **Security**
   - Backup fayllarini xavfsiz joyga qo'ying
   - Paroliga qo'shing (shu kerak bo'lsa)

---

## 🎯 Backup Strategiyasi

### Kunlik
```bash
# Avtomatik
python main.py  # Bot ishga tushayotganda backup qiladi
```

### Haftalik
```bash
# Manual
/admin → /backup (Telegram dan)
```

### Oylik
```bash
# Archive
cp backups/anime_backup_*.json archives/
```

### Xavf Ostida
```bash
# Darhol
python database_backup.py full
```

---

## 📞 Muammolar va Yechimlar

### Problem: "Database locked"
```
Sabab: Boshqa bot instance ishga tushgan
Yechim: pkill -f "python main.py" → Qayta start
```

### Problem: "Backup xatosi"
```
Sabab: Disk joyy tugagan
Yechim: Eski backuplarni o'chiring → Qayta backup
```

### Problem: "Import failed"
```
Sabab: JSON fayl buzilgan
Yechim: Boshqa backup'dan qaytarish
```

---

## 💡 Tips va Triklar

1. **Cron Job'da Avtomatik Backup (Linux)**
```bash
0 2 * * * python /path/to/database_backup.py full
```

2. **Telegram'da Backup Yuborish**
```python
# Admin panel'dan faylni yuborish
with open('backups/anime_bot.db', 'rb') as f:
    await context.bot.send_document(admin_id, f)
```

3. **Backup Kompressiya**
```bash
tar -czf backup_$(date +%Y%m%d).tar.gz backups/
```

4. **Diff Backup (Faqat O'zgartirganlar)**
```bash
rsync -av --backup-dir=backups/diff anime_bot.db backup_location/
```

---

## ✅ Checklist

Bot ishga tushganda:
- [x] Avtomatik backup yaratiladi
- [x] Database ulanadi
- [x] Hamma eski data saqlanib qoladi
- [x] Yangi data qo'shilishi mumkin
- [x] Tarix saqlanadi

---

**Version:** 1.0.0
**Last Updated:** 2024
**Status:** ✅ Barcha data xavfsiz!
