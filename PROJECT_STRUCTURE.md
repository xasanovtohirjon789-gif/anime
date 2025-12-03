# 📂 Project Structure - Anime Bot

## 🎯 Quick Overview

This is a comprehensive Telegram bot for managing anime content with user panel, admin panel, and database management. ~10,000 lines of Python code.

## 📁 File Structure

### Core Application Files

```
bot.py (>2000 lines)
├── AnimeBot class - Main bot handler
├── User panel handlers (start, search, view)
├── Admin panel handlers (add, delete, edit)
├── Pagination and parts management
└── Callback query handlers
```

**Purpose:** Main bot logic with conversation handlers

---

```
main.py (~500 lines)
├── AnimeBotMain class
├── Additional admin handlers
├── Bot initialization
├── Command handlers
└── Test and stats commands
```

**Purpose:** Entry point and main application initialization

---

```
database.py (>1500 lines)
├── Database class
├── User management
├── Anime CRUD operations
├── Parts management
├── Groups management
├── Statistics queries
└── Data export/import
```

**Purpose:** SQLite database operations and ORM

---

### Configuration Files

```
config.py (~50 lines)
├── BOT TOKEN
├── ADMIN_IDs
├── MANDATORY_CHANNELS
├── DATABASE_PATH
└── Constants
```

**Purpose:** Bot configuration and settings

---

```
constants.py (>500 lines)
├── Enum classes
├── Bot states
├── Error messages
├── Success messages
├── Button labels
├── Database queries
└── File size limits
```

**Purpose:** Constants and enums used throughout

---

```
.env.example (~5 lines)
```

**Purpose:** Environment variables template

---

### Utility and Helper Modules

```
utils.py (>700 lines)
├── ValidationUtils - Input validation
├── TextFormatting - Message formatting
├── ErrorMessages - Error text
├── SuccessMessages - Success text
├── ButtonLabels - UI labels
├── PaginationUtils - Page calculations
├── SecurityUtils - Input sanitization
└── LoggerUtils - Logging helpers
```

**Purpose:** Utility functions and formatting

---

```
middleware.py (>600 lines)
├── UserSessionMiddleware - Session tracking
├── RateLimitMiddleware - Request limiting
├── ErrorHandlerMiddleware - Error tracking
├── CommandValidationMiddleware - Command validation
└── ContextPreservationMiddleware - Context storage
```

**Purpose:** Middleware for request handling

---

```
handlers.py (>600 lines)
├── GeneralHandlers - General message handling
├── SearchHandlers - Search functionality
├── NotificationHandlers - Notifications
├── AnalyticsHandlers - Analytics tracking
├── CallbackHandlers - Callback processing
├── MediaHandlers - Media file handling
├── PaginationHandlers - Pagination logic
├── StateManagementHandlers - State tracking
└── ValidationHandlers - Input validation
```

**Purpose:** Various handler classes for different operations

---

```
admin_utils.py (>700 lines)
├── AdminUtils class
├── Statistics functions
├── Export/import operations
├── Data analytics
├── Cleanup functions
└── User information
```

**Purpose:** Admin utilities and statistics

---

```
advanced_admin.py (>800 lines)
├── AdvancedAdminPanel - Advanced admin features
├── Broadcast functionality
├── Group selection
├── UserManagementPanel - User management
├── ModeratorPanel - Moderation features
└── Report handling
```

**Purpose:** Advanced admin panel features

---

```
extended_features.py (>500 lines)
├── ExtendedFeatures class
├── Message broadcasting
├── Admin statistics
├── Analytics reports
├── Export functionality
└── Backup features
```

**Purpose:** Extended bot features

---

### Setup and Installation

```
setup.py (>300 lines)
├── Directory creation
├── Database initialization
├── Environment file checking
├── Dependency verification
├── Admin ID setup
├── Bot connection test
└── Admin script generation
```

**Purpose:** One-time setup script

---

```
requirements.txt
├── python-telegram-bot==20.7
├── python-dotenv==1.0.0
├── requests==2.31.0
└── aiohttp==3.9.1
```

**Purpose:** Python package dependencies

---

### Testing

```
test_bot.py (~400 lines)
├── Import tests
├── Configuration tests
├── Database tests
├── Bot connection tests
├── File verification
├── Directory creation
└── Test reporting
```

**Purpose:** Comprehensive bot testing

---

### Documentation

```
README.md (~400 lines)
├── Features overview
├── Installation guide
├── Usage instructions
├── Command reference
├── Database schema
├── Troubleshooting
└── Support info
```

**Purpose:** Main documentation

---

```
CONFIGURATION.md (~500 lines)
├── Environment variables
├── Config options
├── Database setup
├── Security settings
├── Logging configuration
├── Customization guide
└── Configuration checklist
```

**Purpose:** Configuration reference

---

```
DEPLOYMENT.md (~600 lines)
├── Local deployment
├── Docker deployment
├── VPS setup
├── Heroku deployment
├── AWS deployment
├── Monitoring
├── Troubleshooting
└── Performance tips
```

**Purpose:** Deployment guide for various platforms

---

```
PROJECT_STRUCTURE.md (this file)
```

**Purpose:** Project overview and structure

---

### Deployment Files

```
Dockerfile
├── Python 3.11 base image
├── Dependencies installation
├── App setup
└── Health check
```

**Purpose:** Docker containerization

---

```
docker-compose.yml
├── Bot service definition
├── Volume management
├── Logging configuration
└── Network setup
```

**Purpose:** Docker Compose orchestration

---

### Scripts

```
scripts.sh (~400 lines)
├── Setup and installation
├── Bot management (start/stop)
├── Logging utilities
├── Backup functions
├── Database operations
└── Testing commands
```

**Purpose:** Linux/macOS shell utilities

---

```
run.bat (~200 lines)
├── Menu interface
├── Installation
├── Bot management
├── Backup utilities
└── Connection testing
```

**Purpose:** Windows batch utilities

---

### Configuration

```
.gitignore
```

**Purpose:** Git ignore patterns

---

## 📊 Code Statistics

| Component | Lines | Purpose |
|-----------|-------|---------|
| bot.py | 2000+ | Main bot logic |
| database.py | 1500+ | Database operations |
| admin_utils.py | 700+ | Admin utilities |
| advanced_admin.py | 800+ | Advanced admin |
| extended_features.py | 500+ | Extended features |
| handlers.py | 600+ | Message handlers |
| middleware.py | 600+ | Request middleware |
| utils.py | 700+ | Utility functions |
| main.py | 500+ | Application entry |
| config.py | 50+ | Configuration |
| constants.py | 500+ | Constants/enums |
| Documentation | 2000+ | Guides and help |
| **TOTAL** | **~10,000+** | Complete bot |

## 🔄 Data Flow

```
User Message
    ↓
[middleware.py] - Track session, rate limit, validate
    ↓
[handlers.py] - Route to appropriate handler
    ↓
[bot.py] - Process command/callback
    ↓
[database.py] - Query/update database
    ↓
Bot Response
```

## 🗄️ Database Schema

```
┌─────────────────────────────────────┐
│            ANIME BOT DATABASE       │
└─────────────────────────────────────┘
           ↓
    ┌──────────┴──────────┬──────────────────┬──────────────┐
    ↓                     ↓                  ↓              ↓
  users              anime            anime_parts       groups
  ├─ user_id         ├─ id             ├─ id            ├─ id
  ├─ username        ├─ code           ├─ anime_code    ├─ group_id
  ├─ first_name      ├─ description    ├─ part_number   ├─ link
  ├─ last_name       ├─ photo_id       ├─ file_id       ├─ name
  └─ timestamps      └─ timestamps     └─ timestamps    └─ timestamps
                           ↓
                      anime_groups
                      ├─ anime_code
                      ├─ group_id
                      └─ timestamps
                           ↓
                      user_history
                      ├─ user_id
                      ├─ anime_code
                      └─ timestamps
```

## 🎯 Key Features by File

### User Features
- **bot.py**: Search, view, pagination
- **database.py**: Retrieve anime data
- **handlers.py**: Validate input

### Admin Features
- **bot.py**: CRUD operations
- **admin_utils.py**: Statistics
- **advanced_admin.py**: Broadcasting
- **extended_features.py**: Export/backup

### System Features
- **middleware.py**: Rate limiting, sessions
- **utils.py**: Validation, formatting
- **handlers.py**: State management
- **database.py**: Data persistence

## 🚀 Startup Sequence

1. **setup.py** - Initialize directories and database
2. **config.py** - Load configuration
3. **database.py** - Connect to database
4. **main.py** - Start application
5. **bot.py** - Register handlers
6. **middleware.py** - Apply middleware
7. **Application runs** - Listen for updates

## 📦 Module Dependencies

```
main.py
├── bot.py
├── database.py
├── admin_utils.py
├── extended_features.py
└── config.py

bot.py
├── database.py
├── config.py
├── handlers.py
└── middleware.py

handlers.py
├── database.py
├── config.py
├── utils.py
└── middleware.py

database.py
└── sqlite3 (built-in)

admin_utils.py
├── database.py
└── config.py

advanced_admin.py
├── database.py
└── config.py
```

## 📈 Scalability

### Current Capacity
- Users: Unlimited
- Anime: 1,000,000+
- Episodes: 1,000+ per anime
- Groups: Unlimited
- Concurrent users: Limited by Telegram API

### Performance Optimization
- Database indexing on frequently queried fields
- Pagination to reduce data transfer
- Rate limiting to prevent abuse
- Session caching for active users

## 🔒 Security Features

- Admin ID verification
- Input validation and sanitization
- Rate limiting per user
- Subscription verification
- Database access control
- Error handling without info leakage
- Secure logging

## 📝 Configuration Hierarchy

```
/etc/environment     (System env vars)
    ↓
.env file            (Project env vars)
    ↓
config.py            (Bot config)
    ↓
constants.py         (Default values)
    ↓
middleware.py        (Runtime settings)
```

## 🎓 Learning Path

1. **Understand config.py** - Configuration basics
2. **Read database.py** - Data structure
3. **Study bot.py** - Main logic
4. **Review handlers.py** - Handler patterns
5. **Check middleware.py** - Request flow
6. **Explore admin_utils.py** - Analytics
7. **Review advanced_admin.py** - Advanced features

---

**Version:** 1.0.0
**Last Updated:** 2024
**Total Files:** 30+
**Total Lines:** 10,000+
