-- Vytvorenie tabuľky pre operácie
CREATE TABLE IF NOT EXISTS operation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    worker_id TEXT NOT NULL,
    order_number TEXT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME
);

-- Vytvorenie tabuľky pre používateľov
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT 0
);

-- Pridanie administrátora (heslo: admin)
INSERT INTO user (username, password_hash, is_admin)
VALUES ('admin', '$pbkdf2-sha256$29000$ZGFtbXk$W0MMTBFu7rZL5cKTP9Ui6x7NIsRCzBu35zU8V9F5Q/I', 1);
