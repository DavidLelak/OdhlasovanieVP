import sqlite3

DATABASE = "data.db"

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS operation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id TEXT NOT NULL,
            order_number TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            is_admin INTEGER NOT NULL
        )
        """)
        # Pridanie predvoleného admin účtu (ak ešte neexistuje)
        cur = conn.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if cur.fetchone()[0] == 0:
            conn.execute(
                "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                ("admin", "admin", 1)
            )
