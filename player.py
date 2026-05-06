import pygame
from mutagen.mp3 import MP3
import os

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_song = None
        self.is_playing = False  # This is the attribute the GUI was missing!
        self.length = 0
        self.current_pos_offset = 0 # To handle seek position

    def load_song(self, path):
        if not path or not os.path.exists(path):
            return
            
        self.current_song = path
        pygame.mixer.music.load(path)
        
        # Get song length using Mutagen
        audio = MP3(path)
        self.length = audio.info.length
        
        self.current_pos_offset = 0
        pygame.mixer.music.play()
        self.is_playing = True

    def play(self):
        if self.current_song:
            pygame.mixer.music.play()
            self.is_playing = True

    def pause(self):
        pygame.mixer.music.pause()
        self.is_playing = False

    def unpause(self):
        pygame.mixer.music.unpause()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def seek(self, seconds):
        if self.current_song:
            # Pygame's set_pos works differently depending on the system, 
            # so the most reliable way is to restart at the new position.
            pygame.mixer.music.play(start=seconds)
            self.current_pos_offset = seconds
            self.is_playing = True

    def get_position(self):
        if not self.is_playing and not pygame.mixer.music.get_busy():
            return self.current_pos_offset
            
        # pygame.mixer.music.get_pos() returns time in milliseconds 
        # since the last play() call started.
        pos = (pygame.mixer.music.get_pos() / 1000.0) + self.current_pos_offset
        return pos

    def set_volume(self, volume):
        # Pygame volume is 0.0 to 1.0
        pygame.mixer.music.set_volume(volume / 100.0)