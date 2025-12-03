# ⚡ Quick Start Guide

## 3 Minutes Setup

### 1. Prerequisites
- Python 3.9+
- pip
- Telegram account

### 2. Installation

```bash
# Clone or download project
cd trasform

# Install dependencies
pip install -r requirements.txt

# Setup
python setup.py
```

### 3. Configure

```bash
# Copy example env
cp .env.example .env

# Edit .env - add your TOKEN
nano .env
```

Get TOKEN from @BotFather on Telegram

### 4. Add Admin ID

```bash
# Get your Telegram ID
# Send message to @userinfobot

# Edit config.py and add your ID
nano config.py
# Find: ADMIN_IDS = [123456789]
# Change: ADMIN_IDS = [YOUR_ID_HERE]
```

### 5. Run

```bash
python main.py
```

Bot is now running! 🚀

## First Steps

### 1. Open Telegram
- Search for your bot
- Send `/start`
- Subscribe to required channels
- Click "✅ Tekshirish" (Check)

### 2. Admin Setup
- Send `/admin`
- Add some anime:
  - Kodi: `1`
  - Izohi: `Popular Anime`
  - 1-qism video
  - Kodni kiriting: `1`

### 3. Search Anime
- Send `/start`
- Type `1`
- Click "🎬 Animeni ko'rish"
- Select episode

## Commands Reference

| Command | Purpose |
|---------|---------|
| `/start` | Start bot |
| `/help` | Show help |
| `/admin` | Admin panel |
| `/stats` | Bot stats |
| `/top` | Top anime |

## Troubleshooting

### Bot not starting?

```bash
# Check Python version
python --version  # Must be 3.9+

# Check dependencies
pip list | grep telegram

# Test setup
python test_bot.py
```

### Admin panel not showing?

```bash
# Check your ID
# Send to @userinfobot - get ID
# Edit config.py - add ID to ADMIN_IDS
# Restart bot
```

### Can't find bot?

```bash
# Check TOKEN is correct in .env
# Verify bot exists (check @BotFather)
# Restart bot
```

## File Structure

```
trasform/
├── bot.py              ← Main logic
├── database.py         ← Database
├── main.py             ← Start here
├── config.py           ← Settings
├── .env                ← TOKEN
├── requirements.txt    ← Dependencies
├── README.md           ← Full docs
└── ...
```

## Quick Commands

```bash
# View logs
tail -f logs/bot.log

# Backup database
cp anime_bot.db backups/backup.db

# Test connection
python test_bot.py

# Check bot is running
ps aux | grep "python main.py"
```

## Docker Quick Start

```bash
# Build
docker build -t anime-bot .

# Run
docker run -d -e TOKEN=YOUR_TOKEN anime-bot

# Logs
docker logs -f anime-bot
```

## Next Steps

1. ✅ Bot running
2. 📚 Read README.md for full features
3. ⚙️ See CONFIGURATION.md for settings
4. 🚀 See DEPLOYMENT.md to deploy
5. 🧪 Run test_bot.py to verify

## Support

- Check logs: `logs/bot.log`
- Run tests: `python test_bot.py`
- Read docs: `README.md`
- Check config: `config.py`

## Key Shortcuts

### Windows
Double-click `run.bat` for menu

### Linux/macOS
```bash
chmod +x scripts.sh
./scripts.sh help
```

---

**Ready to go!** 🎉

For full documentation, see README.md
