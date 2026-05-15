@echo off
echo ==========================================
echo   AmexInvestment - Windows Setup
echo ==========================================
echo.

REM Check if Python is installed
py --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or 'py' command not found.
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)

echo [1/4] Python found:
py --version
echo.

REM Upgrade pip first
echo [2/4] Upgrading pip...
py -m pip install --upgrade pip
echo.

REM Install requirements
echo [3/4] Installing dependencies...
py -m pip install -r requirements.txt
echo.

REM Initialize database
echo [4/4] Initializing database...
py -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database created!')"
echo.

echo ==========================================
echo   Setup Complete!
echo ==========================================
echo.
echo To start the app, run: py app.py
echo Then open: http://localhost:5000
echo.
echo Default admin login:
echo   Email: admin@amexinvestment.com
echo   Password: admin123
echo.
pause
