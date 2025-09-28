 
import sqlite3

def connect_db():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            course TEXT NOT NULL,
            year INTEGER,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_student(name, roll_no, course, year, email):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, roll_no, course, year, email) VALUES (?, ?, ?, ?, ?)",
                (name, roll_no, course, year, email))
    conn.commit()
    conn.close()

def view_students():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    return rows

def search_student(keyword):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE roll_no LIKE ? OR name LIKE ? OR course LIKE ?", 
                (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    rows = cur.fetchall()
    conn.close()
    return rows

def update_student(student_id, name, roll_no, course, year, email):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE students 
        SET name=?, roll_no=?, course=?, year=?, email=? 
        WHERE id=?
    """, (name, roll_no, course, year, email, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
