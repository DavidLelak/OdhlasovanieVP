@echo off
REM Aktivácia virtuálneho prostredia (ak existuje)
IF EXIST venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) ELSE (
    echo [INFO] Virtuálne prostredie 'venv' neexistuje. Spúšťam bez aktivácie.
)

REM Spustenie backendu
echo [INFO] Spúšťam FastAPI cez Uvicorn...
python -m uvicorn backend.main:app --reload

pause
