import sqlite3
from datetime import datetime

DB_PATH = "app.db"

def init_sqlite_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                order_number TEXT,
                operation_code TEXT,
                start_time TEXT NOT NULL,
                end_time TEXT
            )
        """)
        conn.commit()

def create_operation(user_id: int, order_number: str, operation_code: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO operations (user_id, order_number, operation_code, start_time) VALUES (?, ?, ?, ?)",
            (user_id, order_number, operation_code, now)
        )
        conn.commit()
        return cursor.lastrowid

def stop_operation(operation_id: int):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE operations SET end_time = ? WHERE id = ? AND end_time IS NULL",
            (now, operation_id)
        )
        conn.commit()
        return cursor.rowcount > 0