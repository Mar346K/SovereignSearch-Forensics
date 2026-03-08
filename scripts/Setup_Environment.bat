@echo off
title Sovereign Search - First Time Setup
echo 🕵️ Initializing Forensic AI Environment...

:: Navigate to the project root (assuming script is run from scripts/ directory)
cd /d "%~dp0\.."

:: 1. Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Python is not installed or not in PATH. Please install Python 3.10+.
    pause
    exit
)

:: 2. Create and Activate Virtual Environment
echo [*] Setting up Python Virtual Environment...
if not exist ".venv" (
    python -m venv .venv
)
call .venv\Scripts\activate

:: 3. Install Dependencies
echo [*] Installing required Python packages...
python -m pip install --upgrade pip
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo [!] requirements.txt not found in the root directory!
    pause
    exit
)

:: 4. Initialize Vault Directories
echo [*] Initializing SQLite schema and Vault directories...
if not exist "data_in" mkdir data_in
if not exist "vector_db" mkdir vector_db

:: 5. Check for Ollama
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Ollama not found. Please install it from https://ollama.com
    start https://ollama.com
    pause
    exit
)

:: 6. Pull Required Local AI Models
echo [*] Downloading Intelligence Models (this may take a few minutes)...
ollama pull llama3.1
ollama pull nomic-embed-text

:: 7. Tesseract OCR Warning
echo.
echo ====================================================================
echo [i] NOTE: Forensic Assembly mode requires Tesseract OCR on Windows.
echo     If you haven't installed the binaries, please download from:
echo     https://github.com/UB-Mannheim/tesseract/wiki
echo     Ensure it is added to your System PATH.
echo ====================================================================
echo.

echo [SUCCESS] Environment is fully configured.
echo You can now launch the engine using scripts\01_START_VAULT.bat
pause