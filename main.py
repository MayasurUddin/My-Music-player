from gui import MusicGUI
from player import MusicPlayer
from playlist import PlaylistManager
from settings import SettingsManager
from db import setup_database

def main():
    setup_database()

    player = MusicPlayer()
    playlist = PlaylistManager()
    settings = SettingsManager()

    app = MusicGUI(player, playlist, settings)
    app.run()

if __name__ == "__main__":
    main()