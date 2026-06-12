import sqlite3
import hashlib

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

# USERS
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT
)
""")

# MATCHS
c.execute("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY,
    team_a TEXT,
    team_b TEXT,
    score_a INTEGER,
    score_b INTEGER
)
""")

# BETS
c.execute("""
CREATE TABLE IF NOT EXISTS bets (
    username TEXT,
    match_id INTEGER,
    prono_a INTEGER,
    prono_b INTEGER
)
""")

conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest() 