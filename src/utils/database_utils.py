import hashlib
import sqlite3


def init_db():
    """Initialize the SQLite database with users and ratings tables."""
    conn = sqlite3.connect('heatmap_app.db')
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users
        (username TEXT PRIMARY KEY, 
         password_hash TEXT,
         created_at DATETIME)
    ''')

    # Create ratings table
    c.execute('''
        CREATE TABLE IF NOT EXISTS RATINGS
        (station_id TEXT,
         username TEXT,
         rating INTEGER,
         timestamp DATETIME,
         FOREIGN KEY(username) REFERENCES users(username))
    ''')

    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    """
    Hash a password for storing.
    """
    # salt = "streamlit-heatmap-salt"  # In production, use proper secret management
    # return hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    return str(password)

def verify_user(username: str, password: str) -> bool:
    """Verify user credentials."""
    conn = sqlite3.connect('heatmap_app.db')
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()

    if result is None:
        return False
    return result[0] == hash_password(password)