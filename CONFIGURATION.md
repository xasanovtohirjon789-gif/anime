# ⚙️ Configuration Guide - Anime Bot

## 📝 Environment Variables (.env)

### Required Variables

#### TOKEN
Telegram Bot API token

```
TOKEN=YOUR_BOT_TOKEN_HERE
```

**How to get:**
1. Open Telegram
2. Search for @BotFather
3. Send `/newbot`
4. Follow instructions
5. Copy token

### Optional Variables

```
DATABASE_PATH=anime_bot.db
LOG_LEVEL=INFO
```

## 🔑 config.py Configuration

### Basic Settings

```python
TOKEN = 'YOUR_BOT_TOKEN_HERE'
```

Bot token. Get from @BotFather.

### Admin IDs

```python
ADMIN_IDS = [
    123456789,      # Your Telegram ID
    987654321,      # Other admin
]
```

**How to get your ID:**
1. Send any message to @userinfobot
2. Bot shows your ID
3. Add it to ADMIN_IDS

### Mandatory Channels

```python
MANDATORY_CHANNELS = [
    {
        'channel_id': '@anime_channel',
        'link': 'https://t.me/anime_channel',
        'name': 'Anime Channel'
    },
    {
        'channel_id': '@my_channel',
        'link': 'https://t.me/my_channel',
        'name': 'My Channel'
    }
]
```

Users must subscribe to these channels before using the bot.

### Database Settings

```python
DATABASE_PATH = 'anime_bot.db'
```

Location of SQLite database file.

### Message Settings

```python
MAX_MESSAGE_LENGTH = 4096    # Telegram limit
PARTS_PER_PAGE = 10          # Episodes per page
```

## 🗄️ Database Configuration

Database automatically initializes on first run with SQLite.

### Tables

**anime**
- `id` - Primary key
- `code` - Anime code (unique number)
- `description` - Anime description
- `photo_id` - Thumbnail image
- `created_at` - Creation timestamp
- `updated_at` - Update timestamp

**anime_parts**
- `anime_code` - Reference to anime
- `part_number` - Episode number
- `file_id` - Video file ID from Telegram

**groups**
- `group_id` - Telegram group/channel ID
- `link` - Group link
- `name` - Group name

**users**
- `user_id` - Telegram user ID
- `username` - User's username
- `first_name` - User's first name
- `last_name` - User's last name

**user_history**
- `user_id` - Reference to user
- `anime_code` - Which anime watched
- `part_number` - Which episode
- `viewed_at` - When watched

## 🎯 Feature Configuration

### Rate Limiting

```python
# middleware.py
MAX_REQUESTS_PER_MINUTE = 30
TIME_WINDOW = 60  # seconds
```

Limits requests per user.

### Session Timeout

```python
# middleware.py
SESSION_TIMEOUT_HOURS = 24
```

How long user session stays active.

### Broadcast Settings

```python
# middleware.py
MAX_BROADCAST_PER_HOUR = 5
MIN_DELAY_BETWEEN_MESSAGES = 0.05  # seconds
```

Limits for mass messaging.

## 🎬 Anime Configuration

### Code Validation

```python
# constants.py
MIN_CODE = 1
MAX_CODE = 999999
```

Anime codes must be between these values.

### Description Settings

```python
MIN_DESCRIPTION_LENGTH = 10
MAX_DESCRIPTION_LENGTH = 4000
```

Anime description length limits.

### Parts Configuration

```python
MAX_PARTS_PER_ANIME = 1000
MIN_PARTS = 1
```

Maximum episodes per anime.

## 📱 Telegram Settings

### Chat Type

Only private chats (direct messages to bot).

### File Limits

```python
# constants.py
MAX_VIDEO_SIZE = 2000000000      # 2GB
MAX_PHOTO_SIZE = 5242880         # 5MB
```

## 🔐 Security Configuration

### Input Validation

- Anime codes: Numbers only
- Group IDs: Numbers only (with optional minus)
- Text input: Max 1000 characters
- URLs: Must start with https://t.me/

### Rate Limiting

Default: 30 requests per minute per user

To change:
```python
# middleware.py
rate_limit_middleware = RateLimitMiddleware(
    max_requests=50,  # Change this
    time_window=60
)
```

### Admin Protection

Only admin IDs in config can use /admin command.

## 📊 Logging Configuration

### Log Levels

```
DEBUG - Detailed debugging info
INFO - General information
WARNING - Warning messages
ERROR - Error messages
CRITICAL - Critical errors
```

### Log Files

```
logs/bot.log       - General logs
logs/admin.log     - Admin actions
logs/errors.log    - Errors only
```

Change in logging setup:
```python
logging.basicConfig(
    level=logging.INFO,  # Change this
    filename='logs/bot.log'
)
```

## 🚀 Deployment Configuration

### Docker Environment

```dockerfile
ENV TOKEN=your_token
ENV PYTHONUNBUFFERED=1
```

### Systemd Service

```ini
[Service]
Environment="TOKEN=your_token"
```

### Heroku

```bash
heroku config:set TOKEN=your_token
```

## 📦 Python Packages

### Version Requirements

```
Python >= 3.9
python-telegram-bot >= 20.0
python-dotenv >= 1.0
```

All versions in requirements.txt

## 🔧 Advanced Configuration

### Custom Middlewares

Add to main.py:

```python
from telegram.ext import Application
app = Application.builder().token(TOKEN).build()
app.add_handler(custom_handler)
```

### Custom Handlers

Create new handler in handlers.py:

```python
async def my_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")
```

## 🛠️ Customization

### Custom Messages

Edit utils.py messages:

```python
class ErrorMessages:
    CUSTOM_MESSAGE = "Your message"
```

### Custom Buttons

Edit ButtonLabels in utils.py:

```python
class ButtonLabels:
    CUSTOM = "🎯 Custom Button"
```

### Custom Emojis

Edit ButtonEmojis in constants.py:

```python
class ButtonEmojis:
    CUSTOM = "🆕"
```

## 📝 Configuration Checklist

Before running bot:

- [ ] TOKEN set in .env
- [ ] Admin IDs added to config.py
- [ ] Mandatory channels configured
- [ ] DATABASE_PATH correct
- [ ] Log directories exist
- [ ] Backup directory exists
- [ ] All permissions correct
- [ ] No syntax errors in config.py

## 🧪 Testing Configuration

Run tests:

```bash
python test_bot.py
```

Tests verify:
- Imports
- Configuration
- Database
- Bot connection
- Required files

## 📞 Configuration Help

### Error: TOKEN not set

Solution:
1. Create .env file
2. Add: `TOKEN=your_token`
3. Save and restart

### Error: Admin ID not found

Solution:
1. Get your ID from @userinfobot
2. Add to ADMIN_IDS in config.py
3. Restart bot

### Error: No mandatory channels

Solution:
1. Add channels to MANDATORY_CHANNELS
2. Include channel_id, link, and name
3. Restart bot

### Error: Database locked

Solution:
1. Stop all bot instances
2. Wait 30 seconds
3. Restart bot

## 📚 More Information

- See README.md for installation
- See DEPLOYMENT.md for deployment
- See bot commands with /help

---

**Last Updated:** 2024
**Version:** 1.0.0
