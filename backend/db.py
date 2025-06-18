import sqlite3
from datetime import datetime
import csv
import os

DB_FILE = "data.db"

# Inicializácia databázy – vytvorenie tabuľky, ak neexistuje
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                worker_id TEXT NOT NULL,
                order_number TEXT NOT NULL,
                start_time TEXT NOT NULL,
                stop_time TEXT
            )
        """)
        conn.commit()

# Spustenie operácie (záznam START)
def create_operation(worker_id: str, order_number: str, start_time: str):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO operations (worker_id, order_number, start_time)
            VALUES (?, ?, ?)
        """, (worker_id, order_number, start_time))
        conn.commit()
        return {"message": "Operácia spustená", "operation_id": cursor.lastrowid}

# Ukončenie operácie (záznam STOP)
def stop_operation(operation_id: int, stop_time: str):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE operations
            SET stop_time = ?
            WHERE id = ? AND stop_time IS NULL
        """, (stop_time, operation_id))
        conn.commit()
        if cursor.rowcount == 0:
            return {"error": "Operácia neexistuje alebo už bola ukončená"}
        return {"message": "Operácia ukončená"}

# Filtrovanie operácií
def get_operations(worker_id=None, order_number=None):
    query = "SELECT * FROM operations WHERE 1=1"
    params = []
    if worker_id:
        query += " AND worker_id = ?"
        params.append(worker_id)
    if order_number:
        query += " AND order_number = ?"
        params.append(order_number)

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

# Export do CSV (vygeneruje súbor export.csv)
def export_operations(worker_id=None, order_number=None):
    operations = get_operations(worker_id, order_number)
    filename = "export.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "worker_id", "order_number", "start_time", "stop_time"])
        writer.writeheader()
        writer.writerows(operations)
    return filename
