@echo off
title AI Assistant - Beautiful UI
echo.
echo 🤖 AI Assistant with Beautiful UI
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "app.py" (
    echo ❌ app.py not found. Please run this script from the my_ai_assistant folder
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ❌ .env file not found
    echo Please create .env file with your API keys
    pause
    exit /b 1
)

echo ✅ All checks passed!
echo.
echo Choose an option:
echo 1. Start locally (http://localhost:8501)
echo 2. Try to create permanent public link
echo 3. Open in browser automatically
echo.

set /p choice="Enter your choice (1/2/3): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Starting AI Assistant locally...
    echo 🌐 URL: http://localhost:8501
    echo.
    start "AI Assistant" cmd /k "streamlit run app.py --server.port 8501"
    timeout /t 3 /nobreak >nul
    start http://localhost:8501
) else if "%choice%"=="2" (
    echo.
    echo 🌐 Attempting to create permanent public link...
    python start_with_link.py
) else if "%choice%"=="3" (
    echo.
    echo 🚀 Starting AI Assistant and opening browser...
    start "AI Assistant" cmd /k "streamlit run app.py --server.port 8501"
    timeout /t 5 /nobreak >nul
    start http://localhost:8501
) else (
    echo.
    echo Invalid choice. Starting locally...
    start "AI Assistant" cmd /k "streamlit run app.py --server.port 8501"
    timeout /t 3 /nobreak >nul
    start http://localhost:8501
)

echo.
echo ✅ AI Assistant started!
echo 💡 Keep the terminal window open to maintain the connection
echo.
pause
