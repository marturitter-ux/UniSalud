import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "unisalud.db"

def connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            birth_date TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            blood_group TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS professionals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            specialty TEXT,
            registration TEXT,
            email TEXT,
            phone TEXT
        );
        CREATE TABLE IF NOT EXISTS institutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT,
            city TEXT,
            address TEXT,
            contact TEXT
        );
        CREATE TABLE IF NOT EXISTS studies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            modality TEXT NOT NULL,
            body_region TEXT,
            study_date TEXT,
            institution TEXT,
            professional TEXT,
            status TEXT DEFAULT 'Pendiente',
            report TEXT,
            file_name TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        );
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            professional TEXT,
            institution TEXT,
            appointment_date TEXT,
            appointment_time TEXT,
            reason TEXT,
            status TEXT DEFAULT 'Solicitado',
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        );
        CREATE TABLE IF NOT EXISTS consents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            consent_type TEXT,
            granted_to TEXT,
            consent_date TEXT,
            status TEXT,
            notes TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        );
        CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            actor TEXT,
            action TEXT,
            detail TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """)

def log_activity(actor, action, detail=""):
    with connect() as con:
        con.execute("INSERT INTO activity(actor, action, detail) VALUES(?,?,?)",
                    (actor, action, detail))
