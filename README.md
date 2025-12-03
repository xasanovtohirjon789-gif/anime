# 🎬 Anime Bot - Telegram Anime Management Bot

Telegram uchun to'liq anime boshqaruv botlari. Qismli izlash, admin paneli va guruh boshqaruvi.

## 🌟 Xususiyatlar

### 👤 Foydalanuvchi Qismi
- ✅ Majburiy obuna kanallari tekshiruvi
- 📝 Anime kodini bo'yicha qidirish
- 🎬 Qismlarni sahifa-sahifa ko'rish (10 ta qism sahifada)
- ⬅️➡️ Qismlar o'rtasida navigatsiya
- 📺 Video qismlarini ko'rish

### ⚙️ Admin Panel
- ➕ Anime qo'shish (izoh + qismlar)
- ❌ Anime o'chirish
- ✏️ Anime tahrirlash (qism qo'shish/o'chirish)
- 📍 Guruh boshqaruvi (qo'shish/o'chirish)
- 📊 Statistika va analitika
- 📢 Xabar broadcast qilish
- 💾 Ma'lumotlar bazasi zaxiralash

### 🛠️ Texnik Xususiyatlar
- SQLite ma'lumotlar bazasi
- Qism pagination (10 ta qism sahifada)
- Foydalanuvchi sessiyalar
- Xatolik boshqaruvi
- Rate limiting
- Broadcasting funksiyasi
- Analitika tracking

## 📦 O'rnatish

### Talab qilinadigan narsalar
- Python 3.9+
- pip

### 1. Loyihani klonlash
```bash
cd /path/to/project
```

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. .env faylini sozlash
```bash
cp .env.example .env
```

`.env` faylida Telegram bot tokeningizni qo'shing:
```
TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE
```

### 4. Admin ID'larini qo'shish
`config.py` faylida admin ID'larini qo'shing:
```python
ADMIN_IDS = [
    5763542336,  # Sizning Telegram ID
    5763542336,  # Boshqa admin
]
```

### 5. Majburiy kanallarni sozlash
`config.py` faylida MANDATORY_CHANNELS qo'shing:
```python
MANDATORY_CHANNELS = [
    {
        'channel_id': '@channel_username',
        'link': 'https://t.me/channel_username',
        'name': 'Kanal nomi'
    },
]
```

### 6. Setup skriptini ishlating
```bash
python setup.py
```

## 🚀 Botni Ishga Tushirish

### Birinchi marta ishga tushirish
```bash
python main.py
```

### O'rinli ishga tushirish (Linux/macOS)
```bash
nohup python main.py &
```

### Windows-da o'rinli ishga tushirish
```bash
python main.py
# yoki
start pythonw.exe main.py
```

## 📚 Foydalanuvchi Qo'llanmasi

### Anime Izlash
1. `/start` komandasi yuboring
2. Majburiy kanallarga obuna bo'ling
3. "✅ Tekshirish" tugmasini bosing
4. Anime kodini kiriting (faqat raqam)
5. Anime izohi ko'rinadi
6. "🎬 Animeni ko'rish" tugmasini bosing
7. Qismlarni tanlang

### Admin Komandalar

#### Anime Qo'shish
```
/admin -> "➕ Anime qo'shish" -> 
Izoh yuboring -> 
1-qism videosini yuboring -> 
Yana qism qo'shish? -> 
Anime kodini kiriting
```

#### Anime O'chirish
```
/admin -> "❌ Anime o'chirish" -> 
Anime kodini yuboring
```

#### Anime Tahrirlash
```
/admin -> "✏️ Anime tahrirlash" -> 
Anime kodini yuboring -> 
Kerakli amalni tanlang:
- Qism qo'shish
- Qism o'chirish
- Animeni o'chirish
```

#### Guruh Qo'shish
```
/admin -> "➕ Guruh qo'shish" ->
Guruh ID sini yuboring ->
Guruh linkini yuboring ->
Guruh nomini yuboring
```

#### Statistika Ko'rish
```
/stats - Bot statistikasi
/analytics - Faoliyat hisoboti
/top - Eng ko'p ko'rilgan animeler
```

#### Xabar Broadcast Qilish
```
/admin -> Broadcast ->
Turni tanlang (foydalanuvchilar/guruhlar) ->
Xabarni yuboring ->
Tasdiqlash
```

## 🗄️ Ma'lumotlar Bazasi Tuzilishi

### anime
- `id` - Unikal ID
- `code` - Anime kodi (unikal raqam)
- `description` - Anime izohi
- `photo_id` - Rasm Telegram file ID
- `created_at` - Yaratilgan vaqti
- `updated_at` - O'zgartirilgan vaqti

### anime_parts
- `id` - Unikal ID
- `anime_code` - Anime kodi
- `part_number` - Qism raqami
- `file_id` - Video Telegram file ID
- `created_at` - Yaratilgan vaqti

### groups
- `id` - Unikal ID
- `group_id` - Telegram guruh ID
- `link` - Guruh linki
- `name` - Guruh nomi
- `created_at` - Yaratilgan vaqti

### anime_groups
- `anime_code` - Anime kodi
- `group_id` - Guruh ID
- `added_at` - Qo'shilgan vaqti

### users
- `user_id` - Telegram user ID
- `username` - Username
- `first_name` - Birinchi ism
- `last_name` - Oxirgi ism
- `created_at` - Ro'yxatdan o'tgan vaqti
- `last_seen` - Oxirgi faoliyat vaqti

## 🔧 Sozlamalar

### config.py

```python
TOKEN = 'YOUR_BOT_TOKEN'              # Telegram bot token
ADMIN_IDS = [123456789]               # Admin Telegram ID'lari
MANDATORY_CHANNELS = [...]            # Majburiy obuna kanallari
DATABASE_PATH = 'anime_bot.db'        # Ma'lumotlar bazasi yo'li
MAX_MESSAGE_LENGTH = 4096             # Maksimal xabar uzunligi
PARTS_PER_PAGE = 10                   # Sahifada qismlar soni
```

## 📊 Komandalar

| Komanda | Tavsifi | Ruxsat |
|---------|---------|--------|
| `/start` | Botni boshlash | Hammaga |
| `/help` | Yordam | Hammaga |
| `/admin` | Admin panel | Admin |
| `/stats` | Bot statistikasi | Admin |
| `/analytics` | Faoliyat hisoboti | Admin |
| `/top` | Eng ko'p ko'rilgan animeler | Admin |
| `/backup` | Ma'lumotlar bazasi zaxiralash | Admin |
| `/export` | Animeler ro'yxati eksport | Admin |
| `/groups` | Guruhlar ro'yxati | Admin |
| `/broadcast` | Xabar yuborish | Admin |
| `/test` | Bot test | Admin |

## 🔒 Xavfsizlik

- Admin ID tekshiruvi
- Kod tekshiruvi (faqat raqam)
- Rate limiting (30 so'rov/minut)
- Input sanitizatsiya
- Obuna tekshiruvi
- Session tracking

## 📈 Analitika

Bot quyidagi ma'lumotlarni tracking qiladi:
- Foydalanuvchi faoliyati
- Anime ko'rishlar soni
- Eng ko'p ko'rilgan animeler
- Kunlik ko'rishlar statistikasi
- Foydalanuvchi haqida ma'lumot

## 🐛 Muammolarni Hal Qilish

### Bot ishlamayapti
```
1. Token to'g'ri ekanligini tekshiring
2. Python 3.9+ o'rnatilganini tekshiring
3. Interni ulanishini tekshiring
4. python setup.py ishlating
```

### Admin panel ochilmaydi
```
1. Sizning Telegram ID'ni config.py da qo'shing
2. Botni o'chirib qayta ishga tushiring
```

### Animeler qo'shilmaydi
```
1. Anime kodi raqam ekanligini tekshiring
2. Video formatini tekshiring
3. Ma'lumotlar bazasi ruxsatlarini tekshiring
```

## 📝 Log Faylari

Botning log faylari `logs/` papkasida saqlanadi:
- `bot.log` - Asosiy log
- `admin.log` - Admin faoliyatlari
- `errors.log` - Xatolar

## 🔄 Yangilash

Yangisini o'rnatish uchun:
```bash
git pull origin main
pip install -r requirements.txt
python setup.py
```

## 📞 Qo'llab-Quvalash

Muammolar bo'lsa:
1. Log fayllarini tekshiring
2. config.py ni tekshiring
3. Ma'lumotlar bazasini qayta o'rnatib ko'ring
4. Botni o'chirib qayta ishga tushiring

## 📄 Litsenziya

MIT License

## 👨‍💻 Takomillash

Foydalanuvchi hamkorligini kutamiz!

---

**Versiya:** 1.0.0
**Oxirgi O'zgartirilgan:** 2024
**Holat:** ✅ Faol
