import sqlite3

DB_NAME = "app.db"

def init_db():
    # Initialize database connection and create users table
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, email TEXT, password TEXT, handle TEXT)''')
    conn.commit()
    conn.close()

def create_user(email, password, handle):
    # Insert a new user record into the database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO users (email, password, handle) VALUES (?, ?, ?)", (email, password, handle))
    conn.commit()
    conn.close()

def authenticate_user(email, password):
    # Check if a user exists with the given email and password
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()
    return user
