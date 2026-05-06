from db import get_connection
import sqlite3

class PlaylistManager:
    def __init__(self):
        self.current_playlist = "Default"
        self.index = 0

    def get_all_playlist_names(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM playlists')
        names = [row[0] for row in cursor.fetchall()]
        conn.close()
        return names

    def get_current_songs(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT songs.file_path 
            FROM songs 
            JOIN playlists ON songs.playlist_id = playlists.id 
            WHERE playlists.name = ?
        ''', (self.current_playlist,))
        songs = [row[0] for row in cursor.fetchall()]
        conn.close()
        return songs

    def get_all_songs(self):
        return self.get_current_songs()

    def add_song(self, file_path):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM playlists WHERE name = ?', (self.current_playlist,))
        playlist_id = cursor.fetchone()[0]
        cursor.execute('INSERT INTO songs (playlist_id, file_path) VALUES (?, ?)', (playlist_id, file_path))
        conn.commit()
        conn.close()

    # --- NEW: Function to remove a single song ---
    def remove_song(self, file_path):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM playlists WHERE name = ?', (self.current_playlist,))
        playlist_id = cursor.fetchone()[0]
        cursor.execute('DELETE FROM songs WHERE playlist_id = ? AND file_path = ?', (playlist_id, file_path))
        conn.commit()
        conn.close()

    def create_playlist(self, name):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO playlists (name) VALUES (?)', (name,))
            conn.commit()
        except sqlite3.IntegrityError:
            pass 
        conn.close()

    def delete_playlist(self, name):
        if len(self.get_all_playlist_names()) <= 1:
            return 
            
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM playlists WHERE name = ?', (name,))
        conn.commit()
        conn.close()
        
        self.current_playlist = self.get_all_playlist_names()[0]
        self.index = 0

    def switch_playlist(self, name):
        self.current_playlist = name
        self.index = 0

    def next_song(self):
        songs = self.get_current_songs()
        if not songs: return None
        self.index = (self.index + 1) % len(songs)
        return songs[self.index]

    def prev_song(self):
        songs = self.get_current_songs()
        if not songs: return None
        self.index = (self.index - 1) % len(songs)
        return songs[self.index]