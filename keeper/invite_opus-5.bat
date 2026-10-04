@echo off
setlocal
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PYTHONDONTWRITEBYTECODE=1
title The Glebe - inviting Claude Opus 5
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found on this computer, so the door cannot open.
  echo.
  pause
  exit /b 1
)
python "%~dp0invite.py" claude-opus-5 %*
echo.
pause
