import sqlite3
from datetime import date

def get_connection():
    conn = sqlite3.connect("rentcar.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            login         TEXT    NOT NULL UNIQUE,
            password      TEXT    NOT NULL,
            role          TEXT    NOT NULL,
            status        TEXT    NOT NULL,
            created_at    TEXT    NOT NULL
        );
        CREATE TABLE IF NOT EXISTS cars (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            brand       TEXT    NOT NULL,
            model       TEXT    NOT NULL,
            year        INTEGER NOT NULL,
            plate       TEXT    NOT NULL UNIQUE,
            category    TEXT    NOT NULL CHECK(category IN ('economy', 'compact', 'midsize', 'suv', 'luxury')),
            fuel_type   TEXT    NOT NULL CHECK(fuel_type IN ('gasoline', 'diesel', 'electric', 'hybrid')),
            insurance   TEXT    NOT NULL,
            daily_rate  REAL    NOT NULL,
            status      TEXT    NOT NULL DEFAULT 'available' CHECK(status IN ('available', 'rented', 'maintenance'))
        );
        CREATE TABLE IF NOT EXISTS customers (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            nif         TEXT NOT NULL UNIQUE,
            id_card     TEXT NOT NULL,
            birth_date  TEXT NOT NULL,
            email       TEXT NOT NULL,
            phone       TEXT NOT NULL,
            address     TEXT NOT NULL,
            license_no  TEXT NOT NULL UNIQUE,
            status      TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'inactive')),
            created_at  TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS rentals (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            car_id       INTEGER NOT NULL REFERENCES cars(id),
            customer_id  INTEGER NOT NULL REFERENCES customers(id),
            start_date   TEXT    NOT NULL,
            end_date     TEXT    NOT NULL,
            return_date  TEXT,
            total_cost   REAL    NOT NULL CHECK(total_cost >= 0),
            status       TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'returned'))
        );
        CREATE TABLE IF NOT EXISTS invoices (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            rental_id   INTEGER NOT NULL REFERENCES rentals(id),
            issue_date  TEXT    NOT NULL,
            amount      REAL    NOT NULL CHECK(amount >= 0),
            tax         REAL    NOT NULL DEFAULT 0 CHECK(tax >= 0),
            total       REAL    NOT NULL CHECK(total >= 0),
            status      TEXT    NOT NULL DEFAULT 'unpaid' CHECK(status IN ('paid', 'unpaid'))
        );
    """)

    if cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        #pw_hash, salt = hash_password("admin123")
        cursor.execute(
            "INSERT INTO users (name, login, password, role, status, created_at) "
            "VALUES (?, ?, ?, 'admin', 'active', ?)",
            ("admin", "admin", "admin123", date.today().isoformat())
        )
    
    conn.commit()
    conn.close()
    
def authenticate(username: str, password: str) -> dict | None:
    conn = get_connection()
    user = conn.execute(
        "SELECT id, name, login, password, role "
        "FROM users WHERE login = ? AND password = ?",
        (username, password)
    ).fetchone()
    conn.close()

    if user:
        return {"id": user[0], "name": user[1], "login": user[2], "password": user[3], "role": user[4]}
    return None
