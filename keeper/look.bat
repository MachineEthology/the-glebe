@echo off
setlocal
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PYTHONDONTWRITEBYTECODE=1
title The Glebe - the whole garden from above
rem  The garden is the folder above this one.
cd /d "%~dp0.."
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found on this computer, so this cannot run.
  echo.
  pause
  exit /b 1
)
python "shed\look.py"
echo.
if exist "ground\plan.png" (
  start "" "ground\plan.png"
) else (
  echo There is no ground\plan.png to open yet.
)
echo.
pause
