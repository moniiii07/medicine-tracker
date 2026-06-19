import psycopg2
import os

def get_connection():
    """Get database connection — uses cloud DB when deployed, local when developing."""
    db_url = os.environ.get("DATABASE_URL")
    
    if db_url:
        # Cloud deployment — use Supabase
        conn = psycopg2.connect(db_url)
    else:
        # Local development — fall back to SQLite
        import sqlite3
        return None
    
    return conn


def init_db():
    conn = get_connection()
    if conn is None:
        # Local SQLite fallback
        import sqlite3
        conn = sqlite3.connect("medicines.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                dosage TEXT,
                timing TEXT,
                notes TEXT
            )
        """)
        conn.commit()
        conn.close()
        return

    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            dosage TEXT,
            timing TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_medicine(name, dosage, timing, notes):
    conn = get_connection()
    if conn is None:
        import sqlite3
        conn = sqlite3.connect("medicines.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO medicines (name, dosage, timing, notes)
            VALUES (?, ?, ?, ?)
        """, (name, dosage, timing, notes))
        conn.commit()
        conn.close()
        return

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO medicines (name, dosage, timing, notes)
        VALUES (%s, %s, %s, %s)
    """, (name, dosage, timing, notes))
    conn.commit()
    conn.close()


def get_all_medicines():
    conn = get_connection()
    if conn is None:
        import sqlite3
        conn = sqlite3.connect("medicines.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medicines")
        rows = cursor.fetchall()
        conn.close()
        return rows

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines")
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_medicine(medicine_id):
    conn = get_connection()
    if conn is None:
        import sqlite3
        conn = sqlite3.connect("medicines.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM medicines WHERE id = ?", (medicine_id,))
        conn.commit()
        conn.close()
        return

    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicines WHERE id = %s", (medicine_id,))
    conn.commit()
    conn.close()


def get_medicines_by_timing(timing_keyword):
    conn = get_connection()
    if conn is None:
        import sqlite3
        conn = sqlite3.connect("medicines.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM medicines
            WHERE LOWER(timing) LIKE ?
        """, (f"%{timing_keyword.lower()}%",))
        rows = cursor.fetchall()
        conn.close()
        return rows

    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM medicines
        WHERE LOWER(timing) LIKE %s
    """, (f"%{timing_keyword.lower()}%",))
    rows = cursor.fetchall()
    conn.close()
    return rows