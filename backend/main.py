from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.auth import get_current_user, router as auth_router
from backend.db import init_db, get_operations, create_operation, stop_operation, export_operations
from fastapi.responses import FileResponse
from datetime import datetime
import os

app = FastAPI(title="Výrobné operácie")

# Povolenie CORS pre frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # upraviť na konkrétnu doménu v produkcii
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializácia DB
init_db()

# Pripojenie autentifikačných routrov (napr. /login)
app.include_router(auth_router)

# Endpoint: vytvorenie novej operácie (START)
@app.post("/start")
def start_operation(worker_id: str, order_number: str, user=Depends(get_current_user)):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return create_operation(worker_id, order_number, start_time=now)

# Endpoint: ukončenie operácie (STOP)
@app.post("/stop")
def stop_operation_endpoint(operation_id: int, user=Depends(get_current_user)):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return stop_operation(operation_id, stop_time=now)

# Endpoint: výpis operácií (admin vidí všetko, inak filtrované)
@app.get("/operations")
def list_operations(worker_id: str = None, order_number: str = None, user=Depends(get_current_user)):
    if user["role"] == "admin":
        return get_operations(worker_id, order_number)
    else:
        return get_operations(worker_id=user["username"], order_number=order_number)

# Endpoint: export do CSV
@app.get("/export")
def export_to_csv(worker_id: str = None, order_number: str = None, user=Depends(get_current_user)):
    if user["role"] != "admin":
        worker_id = user["username"]
    csv_file = export_operations(worker_id, order_number)
    return FileResponse(csv_file, filename=os.path.basename(csv_file), media_type='text/csv')
