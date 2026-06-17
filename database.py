import sqlite3

def init_db():
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


def add_medicine(name, dosage, timing, notes):
    conn = sqlite3.connect("medicines.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO medicines (name, dosage, timing, notes)
        VALUES (?, ?, ?, ?)
    """, (name, dosage, timing, notes))
    
    conn.commit()
    conn.close()


def get_all_medicines():
    conn = sqlite3.connect("medicines.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM medicines")
    rows = cursor.fetchall()
    
    conn.close()
    return rows
def delete_medicine(medicine_id):
    conn = sqlite3.connect("medicines.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM medicines WHERE id = ?", (medicine_id,))
    
    conn.commit()
    conn.close()
def get_medicines_by_timing(timing_keyword):
    conn = sqlite3.connect("medicines.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM medicines 
        WHERE LOWER(timing) LIKE ?
    """, (f"%{timing_keyword.lower()}%",))
    
    rows = cursor.fetchall()
    conn.close()
    return rows