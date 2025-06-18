from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import sqlite3
import csv
import io

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import auth

from auth import get_current_user, authenticate_user, create_access_token, UserOut
from db import init_db

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE = "data.db"

class OperationStart(BaseModel):
    worker_id: str
    order_number: str

class OperationStop(BaseModel):
    worker_id: str
    order_number: str

@app.post("/login", response_model=UserOut)
def login(form_data: dict):
    username = form_data.get("username")
    password = form_data.get("password")
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["username"]})
    return {"username": user["username"], "is_admin": user["is_admin"], "token": token}

@app.post("/start")
def start_operation(data: OperationStart, user=Depends(get_current_user)):
    now = datetime.now().isoformat(sep=" ", timespec="seconds")
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "INSERT INTO operation (worker_id, order_number, start_time) VALUES (?, ?, ?)",
            (data.worker_id, data.order_number, now),
        )
    return {"status": "started", "timestamp": now}

@app.post("/stop")
def stop_operation(data: OperationStop, user=Depends(get_current_user)):
    now = datetime.now().isoformat(sep=" ", timespec="seconds")
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.execute(
            "SELECT id FROM operation WHERE worker_id=? AND order_number=? AND end_time IS NULL ORDER BY start_time LIMIT 1",
            (data.worker_id, data.order_number)
        )
        row = cur.fetchone()
        if row:
            conn.execute("UPDATE operation SET end_time=? WHERE id=?", (now, row[0]))
            return {"status": "stopped", "timestamp": now}
        else:
            raise HTTPException(status_code=404, detail="No open operation found.")

@app.get("/records")
def get_records(start_date: Optional[str] = None, end_date: Optional[str] = None, user=Depends(get_current_user)):
    query = "SELECT * FROM operation WHERE 1=1"
    params = []
    if not user["is_admin"]:
        query += " AND worker_id = ?"
        params.append(user["username"])
    if start_date:
        query += " AND start_time >= ?"
        params.append(start_date)
    if end_date:
        query += " AND end_time <= ?"
        params.append(end_date)
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]

@app.get("/export")
def export_csv(start_date: Optional[str] = None, end_date: Optional[str] = None, user=Depends(get_current_user)):
    query = "SELECT * FROM operation WHERE 1=1"
    params = []
    if not user["is_admin"]:
        query += " AND worker_id = ?"
        params.append(user["username"])
    if start_date:
        query += " AND start_time >= ?"
        params.append(start_date)
    if end_date:
        query += " AND end_time <= ?"
        params.append(end_date)
    with sqlite3.connect(DATABASE) as conn:
        rows = conn.execute(query, params).fetchall()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "worker_id", "order_number", "start_time", "end_time"])
    for row in rows:
        writer.writerow(row)
    output.seek(0)
    return FileResponse(path_or_file=io.BytesIO(output.getvalue().encode()), media_type="text/csv", filename="export.csv")
