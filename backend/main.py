from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Base, User
from crud import (
    create_user,
    get_all_users,
    delete_user,
    set_user_active_status,
    get_user_by_username,
)
from pydantic import BaseModel

# Inicializácia databázy
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Admin API")

# Povolenie CORS pre frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Základná závislosť na databázovej session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schémy pre API
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

class UserStatusUpdate(BaseModel):
    is_active: bool

# Vzorka: overenie admina (tu len natvrdo pre demo)
def get_current_user():
    return {"username": "admin", "role": "admin"}

def require_admin(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Prístup zamietnutý")
    return user

# API endpoints
@app.get("/api/users")
def list_users(current_user: dict = Depends(require_admin), db: Session = Depends(get_db)):
    return get_all_users(db)

@app.post("/api/users")
def add_user(user: UserCreate, current_user: dict = Depends(require_admin), db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Používateľ už existuje")
    return create_user(db, user.username, user.password, user.role)

@app.delete("/api/users/{user_id}")
def remove_user(user_id: int, current_user: dict = Depends(require_admin), db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Používateľ neexistuje")
    return {"detail": "Používateľ odstránený"}

@app.patch("/api/users/{user_id}")
def toggle_user_status(user_id: int, status: UserStatusUpdate, current_user: dict = Depends(require_admin), db: Session = Depends(get_db)):
    updated_user = set_user_active_status(db, user_id, status.is_active)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Používateľ neexistuje")
    return updated_user

# Servírovanie statickej admin HTML stránky
@app.get("/admin", response_class=FileResponse)
def get_admin_page():
    return FileResponse("static/admin.html", media_type="text/html")