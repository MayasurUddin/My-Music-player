from db import get_connection

class SettingsManager:
    def __init__(self):
        self.volume = self.load()

    def load(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT volume FROM settings WHERE id = 1')
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 70.0
        except Exception:
            return 70.0

    def save(self, volume):
        self.volume = volume
        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Update the existing row
            cursor.execute('UPDATE settings SET volume = ? WHERE id = 1', (self.volume,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database error saving settings: {e}")