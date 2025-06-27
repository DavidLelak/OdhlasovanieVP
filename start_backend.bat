@echo off
REM Aktivácia virtuálneho prostredia, ak existuje
IF EXIST venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) ELSE (
    echo [INFO] Virtuálne prostredie neexistuje. Spúšťam bez aktivácie.
)

REM Spustenie FastAPI aplikácie cez Uvicorn z priečinka backend/
echo [INFO] Spúšťam backend z backend/main.py ...
uvicorn backend.main:app --reload

pause
