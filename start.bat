@echo off
powershell.exe -NoExit -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "& '.\.venv\Scripts\Activate.ps1'; python main.py"
