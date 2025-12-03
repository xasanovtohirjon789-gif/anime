#!/bin/bash

# Anime Bot Utility Scripts

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

echo_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

echo_error() {
    echo -e "${RED}❌ $1${NC}"
}

echo_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

# Install dependencies
install_deps() {
    echo_info "Kutubxonalar o'rnatilmoqda..."
    pip install -r requirements.txt
    echo_success "Kutubxonalar o'rnatildi!"
}

# Setup database
setup_db() {
    echo_info "Ma'lumotlar bazasi sozlanmoqda..."
    python3 -c "from database import Database; Database()"
    echo_success "Ma'lumotlar bazasi sozlandi!"
}

# Start bot
start_bot() {
    echo_info "Bot ishga tushmoqda..."
    python3 main.py
}

# Start bot in background
start_bot_bg() {
    echo_info "Bot o'rinli ishga tushmoqda..."
    nohup python3 main.py > logs/bot.log 2>&1 &
    echo_success "Bot o'rinli ishga tushdi! PID: $!"
}

# Stop bot
stop_bot() {
    echo_info "Bot o'chirilmoqda..."
    pkill -f "python3 main.py"
    echo_success "Bot o'chirildi!"
}

# Check bot status
check_status() {
    echo_info "Bot holati tekshirilmoqda..."
    if pgrep -f "python3 main.py" > /dev/null; then
        echo_success "Bot ishlayapti!"
        ps aux | grep "python3 main.py" | grep -v grep
    else
        echo_error "Bot ishlamayapti!"
    fi
}

# View logs
view_logs() {
    echo_info "Log ko'rsilmoqda..."
    tail -f logs/bot.log
}

# Backup database
backup_db() {
    echo_info "Ma'lumotlar bazasi zaxiralanalmoqda..."
    BACKUP_FILE="backups/anime_bot_$(date +%Y%m%d_%H%M%S).db"
    cp anime_bot.db "$BACKUP_FILE"
    echo_success "Zaxira yaratildi: $BACKUP_FILE"
}

# Restore database
restore_db() {
    if [ -z "$1" ]; then
        echo_error "Zaxira fayli belgilang!"
        return
    fi
    
    echo_warning "Diqqat! Bu amalni qaytarish mumkin emas!"
    read -p "Davom ettirasizmi? (yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        cp "$1" anime_bot.db
        echo_success "Zaxira qaytarildi!"
    fi
}

# Export anime list
export_anime() {
    echo_info "Animeler eksport qilinmoqda..."
    python3 -c "from admin_utils import AdminUtils; AdminUtils().export_anime_list()"
    echo_success "Eksport tugadi!"
}

# Clear logs
clear_logs() {
    echo_warning "Barcha log fayllar o'chiriladi!"
    read -p "Davom ettirasizmi? (yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        rm -f logs/*.log
        echo_success "Log fayllar o'chirildi!"
    fi
}

# Run setup
run_setup() {
    echo_info "Setup skripti ishga tushmoqda..."
    python3 setup.py
}

# Test bot connection
test_connection() {
    echo_info "Bot ulanishi sinovdan o'tmoqda..."
    python3 -c "
import asyncio
from telegram import Bot
from config import TOKEN

async def test():
    try:
        bot = Bot(token=TOKEN)
        me = await bot.get_me()
        print('✅ Bot ulanishi muvaffaqiyatli!')
        print(f'   Bot: @{me.username}')
        return True
    except Exception as e:
        print(f'❌ Xato: {e}')
        return False

asyncio.run(test())
    "
}

# Generate admin ID
get_admin_id() {
    echo_info "Admin ID'ni olish uchun:"
    echo "1. Bot'ga /start yuboring"
    echo "2. Bot sizga ID'ni beradi"
    echo "3. Shu ID'ni config.py da ADMIN_IDS ga qo'shing"
}

# Database statistics
db_stats() {
    echo_info "Ma'lumotlar bazasi statistikasi:"
    python3 -c "
from admin_utils import AdminUtils
stats = AdminUtils().get_bot_statistics()
print(f\"Foydalanuvchilar: {stats['total_users']}\")
print(f\"Animeler: {stats['total_anime']}\")
print(f\"Qismlar: {stats['total_parts']}\")
print(f\"Guruhlar: {stats['total_groups']}\")
    "
}

# Help menu
show_help() {
    echo_info "Anime Bot - Utility Commands"
    echo ""
    echo "Asosiy:"
    echo "  install       - Kutubxonalarni o'rnatish"
    echo "  setup         - Bot'ni sozlash"
    echo "  start         - Bot'ni ishga tushirish"
    echo "  start-bg      - Bot'ni o'rinli ishga tushirish"
    echo "  stop          - Bot'ni o'chirish"
    echo "  status        - Bot holati"
    echo ""
    echo "Logs va Database:"
    echo "  logs          - Log ko'rish"
    echo "  backup        - Database zaxira"
    echo "  restore FILE  - Database qaytarish"
    echo "  stats         - Database statistikasi"
    echo ""
    echo "Export va Tools:"
    echo "  export        - Animeler eksport"
    echo "  clear-logs    - Log'larni o'chirish"
    echo "  test          - Bot ulanishini sinovdan o'tkazish"
    echo ""
    echo "Information:"
    echo "  help          - Bu menyu"
    echo "  admin-id      - Admin ID'ni olish"
    echo ""
}

# Main menu
case "$1" in
    install)
        install_deps
        ;;
    setup)
        run_setup
        ;;
    start)
        start_bot
        ;;
    start-bg)
        start_bot_bg
        ;;
    stop)
        stop_bot
        ;;
    status)
        check_status
        ;;
    logs)
        view_logs
        ;;
    backup)
        backup_db
        ;;
    restore)
        restore_db "$2"
        ;;
    export)
        export_anime
        ;;
    clear-logs)
        clear_logs
        ;;
    test)
        test_connection
        ;;
    stats)
        db_stats
        ;;
    admin-id)
        get_admin_id
        ;;
    help)
        show_help
        ;;
    *)
        echo_error "Noma'lum komanda: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
