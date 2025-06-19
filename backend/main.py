from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from backend.auth import get_current_user, router as auth_router
from backend.db import init_db, get_operations, create_operation, stop_operation, export_operations, get_all_users, create_user, delete_user, set_user_active_status
from datetime import datetime
from pydantic import BaseModel
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

# Sprístupnenie adresára pre FastAPI
app.mount("/static", StaticFiles(directory="static"), name="static")


# API endpointy pre Admina
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

class UserStatusUpdate(BaseModel):
    is_active: bool

# Zoznam používateľov
@app.get("/api/users")
def list_users(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    return get_all_users(db)

# Vytvorenie používateľa
@app.post("/api/users")
def add_user(user: UserCreate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    return create_user(db, user.username, user.password, user.role)

# Vymazanie používateľa
@app.delete("/api/users/{user_id}")
def remove_user(user_id: int, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Používateľ neexistuje")
    return {"detail": "Používateľ odstránený"}

# Zmena aktívneho stavu
@app.patch("/api/users/{user_id}")
def toggle_user_status(user_id: int, status: UserStatusUpdate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    updated_user = set_user_active_status(db, user_id, status.is_active)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Používateľ neexistuje")
    return updated_user


app = FastAPI()
# Mount statických súborov (napr. CSS, JS, HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/admin", response_class=FileResponse)
def get_admin_page():
    file_path = os.path.join("static", "admin.html")
    return FileResponse(file_path, media_type='text/html')