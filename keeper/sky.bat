@echo off
setlocal
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PYTHONDONTWRITEBYTECODE=1
title The Glebe - what the garden understood of the sky
rem  Reads gate\sky.txt line by line: the day each line was read for, what was understood, what it changed.
cd /d "%~dp0.."
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found on this computer, so this cannot run.
  echo.
  pause
  exit /b 1
)
if not exist "gate\sky.txt" (
  echo There is no gate\sky.txt yet. Write one line per day in it, beginning with the date, and run this again.
  echo.
)
python "shed\sky.py" --gate
echo.
pause
