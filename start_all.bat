@echo off
REM Prechod do korenoveho priecinka projektu
cd /d %~dp0

echo [INFO] Aktivujem virtualne prostredie...
REM Aktivácia virtuálneho prostredia, ak existuje
IF EXIST venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) ELSE (
    echo [INFO] Virtuálne prostredie neexistuje. Spúšťam bez aktivácie.
)

echo [INFO] Spustam FastAPI backend z backend/main.py...
uvicorn backend.main:app --reload

pause