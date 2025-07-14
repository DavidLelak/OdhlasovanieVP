@echo off
echo [INFO] Spúšťam PowerShell s povolením skriptov pre aktuálneho používateľa...
powershell -Command "Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force"

echo [INFO] Overujem verziu node.js a npm:
node -v
npm -v

echo [HOTOVO] Pokračuj spustením: npm install
pause