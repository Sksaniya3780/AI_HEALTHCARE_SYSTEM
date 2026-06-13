import sqlite3
import os
import sys

# --------------------------------------------------
# Ensure project root is in path
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from config.settings import DATABASE_PATH


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------
def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# --------------------------------------------------
# INIT DATABASE
# --------------------------------------------------
def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # PATIENTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        blood_group TEXT,
        phone TEXT,
        address TEXT,
        disease TEXT,
        allergies TEXT,
        insurance TEXT
    )
    """)

    # DOCTORS TABLE
    cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    specialization TEXT,
    department TEXT,
    qualification TEXT,
    experience INTEGER,
    phone TEXT,
    email TEXT,
    available_slots TEXT
)
""")

    # BEDS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS beds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ward_type TEXT,
        bed_number TEXT,
        status TEXT,
        patient_name TEXT
    )
    """)

    # STAFF TABLE
    cursor.execute("""
CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    role TEXT,
    department TEXT,
    shift TEXT,
    phone TEXT,
    email TEXT
)
""")

    conn.commit()
    conn.close()

    print("✅ Database initialized successfully!")


if __name__ == "__main__":
    init_db()