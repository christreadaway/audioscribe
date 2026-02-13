@echo off
title AudioScribe
echo ============================================================
echo   AudioScribe - Local Audio Transcription
echo ============================================================
echo.

:: Navigate to the folder where this batch file lives
cd /d "%~dp0"
echo Working directory: %cd%

:: Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found.
    echo Please create it first with:  py -3.11 -m venv .venv
    echo Then install dependencies:    pip install -r requirements.txt
    pause
    exit /b 1
)

:: Check that dependencies are installed, auto-install if needed
python -c "import whisperx; import gradio" >nul 2>&1
if errorlevel 1 (
    echo Dependencies not found. Installing from requirements.txt...
    if exist "requirements.txt" (
        pip install -r requirements.txt
    ) else (
        echo ERROR: requirements.txt not found in %cd%
        echo Please make sure all project files are in this folder.
        pause
        exit /b 1
    )
)

:: Launch AudioScribe
echo Starting AudioScribe...
echo Your browser will open to http://127.0.0.1:7860
echo.
python audioscribe_windows.py

pause
