Traditional music players are often complex or require internet connectivity. There is a need for a simple, lightweight, offline desktop music player that allows users:
Play audio files easily 
Manage playlists 
Control playback (play, pause, skip) 
Adjust volume and seek audio
**Modules**
main.py: The entry point. Initializes the database check and injects the backend into the GUI.
db.py: Handles the SQLite connection, table creation, and schema initialization.
gui.py: Houses the Tkinter event loop, canvas widgets, and tkinterdnd2 drag-and-drop receptors.
player.py: Manages the Pygame mixer engine and track metadata processing.
playlist.py: Executes SQL queries to manage library state and tracks the current active song index. 
