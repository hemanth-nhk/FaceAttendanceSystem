import sqlite3
import bcrypt

def init_student_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT
                )''')
    conn.commit()
    conn.close()

def student_exists(username):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM students WHERE username = ?", (username,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def validate_student(username, password):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT password FROM students WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()

    if result is None:
        return False

    stored_hashed_pw = result[0]
    return bcrypt.checkpw(password.encode(), stored_hashed_pw.encode())

def add_student(username, password):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # Store as string
    try:
        conn = sqlite3.connect("students.db")
        c = conn.cursor()
        c.execute("INSERT INTO students (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Optional helper for debugging or listing
def get_all_students():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT username FROM students")
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]
