@echo off
REM Anime Bot - Windows Command Script

setlocal enabledelayedexpansion

color 0B

:menu
cls
echo.
echo ╔════════════════════════════════════════╗
echo ║      🤖 Anime Bot Command Menu        ║
echo ╚════════════════════════════════════════╝
echo.
echo 1. Install Dependencies (Kutubxonalarni o'rnatish)
echo 2. Setup Database (Database sozlash)
echo 3. Run Bot (Bot'ni ishga tushirish)
echo 4. Setup Bot (Complete setup)
echo 5. View Logs (Log ko'rish)
echo 6. Backup Database (Database zaxira)
echo 7. Check Status (Holati tekshirish)
echo 8. Test Connection (Ulanishni sinovdan o'tkazish)
echo 9. Exit (Chiqish)
echo.
set /p choice="Enter your choice: "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto setup_db
if "%choice%"=="3" goto run_bot
if "%choice%"=="4" goto setup_bot
if "%choice%"=="5" goto view_logs
if "%choice%"=="6" goto backup
if "%choice%"=="7" goto status
if "%choice%"=="8" goto test
if "%choice%"=="9" goto end
goto invalid

:install
cls
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo ✅ Installation complete!
pause
goto menu

:setup_db
cls
echo Setting up database...
python setup.py
echo.
echo ✅ Database setup complete!
pause
goto menu

:run_bot
cls
echo Starting bot...
python main.py
pause
goto menu

:setup_bot
cls
echo Running complete setup...
python setup.py
echo.
echo ✅ Setup complete! Bot is ready to run.
echo Run 'python main.py' to start the bot.
pause
goto menu

:view_logs
cls
echo Recent logs:
if exist logs\bot.log (
    type logs\bot.log | more
) else (
    echo Log file not found!
)
pause
goto menu

:backup
cls
echo Creating database backup...
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
copy anime_bot.db backups\anime_bot_!mydate!_!mytime!.db
echo ✅ Backup created!
pause
goto menu

:status
cls
echo Checking bot status...
tasklist | find "python.exe" >nul
if %errorlevel%==0 (
    echo ✅ Bot is running!
    tasklist | find "python.exe"
) else (
    echo ❌ Bot is not running!
)
pause
goto menu

:test
cls
echo Testing bot connection...
python -c "import asyncio; from telegram import Bot; from config import TOKEN; bot = Bot(token=TOKEN); print('✅ Connection successful!')"
pause
goto menu

:invalid
cls
echo ❌ Invalid choice! Please try again.
pause
goto menu

:end
cls
echo Goodbye!
exit /b 0
