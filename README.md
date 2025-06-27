# Aplikácia na sledovanie výrobných operácií

Táto aplikácia je postavená na FastAPI a slúži na zaznamenávanie začiatku a konca výrobných operácií.

## 🛠️ Požiadavky

- Python 3.8+
- Balíky z `requirements.txt`

## 📦 Inštalácia

1. Naklonuj repozitár alebo rozbaľ ZIP:
    ```bash
    unzip final_project_fastapi.zip
    cd final_project
    ```

2. Vytvor virtuálne prostredie a aktivuj ho:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. Nainštaluj závislosti:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Spustenie aplikácie

```bash
uvicorn main:app --reload
```

Aplikácia bude bežať na: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🔐 Autentifikácia

- Podporované sú tokeny:
  - `admin`
  - `user`

Príklad použitia:
- Pri volaní chránených endpointov nastav v hlavičke:
  ```
  Authorization: Bearer admin
  ```

## 📋 API Endpointy

| Metóda | Cesta     | Popis                          |
|--------|-----------|--------------------------------|
| POST   | /start    | Spustenie operácie             |
| POST   | /stop     | Ukončenie operácie             |
| GET    | /admin    | Admin HTML rozhranie           |

## 🗃️ Databáza

Používa sa SQLite súbor `app.db`. Záznamy o operáciách sa ukladajú do tabuľky `operations`.

## 📁 Štruktúra projektu

```
main.py
auth.py
sqlite_utils.py
db.py
requirements.txt
```

## 📄 Licencia

Projekt je voľne použiteľný na interné účely.