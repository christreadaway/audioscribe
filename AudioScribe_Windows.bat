@echo off
title AudioScribe
echo ============================================================
echo   AudioScribe - Local Audio Transcription
echo ============================================================
echo.

:: Navigate to the folder where this batch file lives
cd /d "%~dp0"

:: Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found.
    echo Please create it first with:  py -3.11 -m venv .venv
    echo Then install dependencies:    pip install torch torchaudio whisperx gradio==3.50.2
    pause
    exit /b 1
)

:: Launch AudioScribe
echo Starting AudioScribe...
echo Your browser will open to http://127.0.0.1:7860
echo.
python audioscribe_windows.py

pause
