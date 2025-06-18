# 🕒 Odhlasovanie výrobných operácií

Webová aplikácia na sledovanie času výrobných operácií, s podporou viacerých používateľov, autentifikáciou, exportom do CSV a administračným rozhraním.

---

## 📦 Zložky projektu

backend/ # API v Pythone (FastAPI)
frontend/ # Webové rozhranie (HTML/JS/CSS)
data.db # SQLite databáza
README.md # Tento popis


---

## 🚀 Spustenie backendu

### Požiadavky
- Python 3.8+
- FastAPI
- Uvicorn
- SQLite (súčasť Pythonu)
  
### Inštalácia knižníc
```bash
pip install fastapi uvicorn python-multipart

🚀 Spustenie
uvicorn backend.main:app --reload
Aplikácia pobeží na: http://localhost:8000

👥 Používateľské účty
Admin: admin / admin
Bežní používatelia sa pridávajú do tabuľky users v databáze.

📤 Export a filtrovanie
Koncový bod /records umožňuje filtrovanie podľa dátumu (start_date, end_date)
Koncový bod /export vracia CSV

🧪 Testovanie API
Môžeš testovať cez Swagger rozhranie:
http://localhost:8000/docs

📱 Frontend
Zložka frontend/ obsahuje HTML stránku s podporou mobilných zariadení.
Pre zjednodušenie môžeš otvoriť frontend/index.html priamo v prehliadači.

🔒 Bezpečnosť
Tento projekt používa jednoduchú autentifikáciu pre demonštračné účely. V reálnom nasadení odporúčame:
Používať hashovanie hesiel (napr. bcrypt)
Zabezpečené spojenie cez HTTPS
Overovanie tokenov s expiráciou

---