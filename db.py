import sqlite3
import os

def get_connection():
    """Opens a connection to the database and enforces relationship rules."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/music_player.db")
    # This line tells SQLite to automatically delete songs if their parent playlist is deleted (Cascade Delete)
    conn.execute("PRAGMA foreign_keys = 1") 
    return conn

def setup_database():
    """Creates the tables if they don't exist yet."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Create Settings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            volume REAL
        )
    ''')
    
    # 2. Create Playlists Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')
    
    # 3. Create Songs Table (Linked to Playlists)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            playlist_id INTEGER,
            file_path TEXT,
            FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE
        )
    ''')
    
    # Insert default volume if the table is completely empty
    cursor.execute('SELECT COUNT(*) FROM settings')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO settings (id, volume) VALUES (1, 70.0)')
        
    # Insert "Default" playlist if no playlists exist
    cursor.execute('SELECT COUNT(*) FROM playlists')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO playlists (name) VALUES ("Default")')
        
    conn.commit()
    conn.close()