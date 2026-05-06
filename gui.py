import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
from PIL import Image, ImageTk

# --- UI CONSTANTS ---
BG = "#ffffff"
BOX_BG = "#f0f0f0"
ACCENT = "#000000"

class CanvasSlider(tk.Canvas):
    def __init__(self, parent, width=200, height=20, bg=BG, callback=None):
        super().__init__(parent, width=width, height=height, bg=bg, highlightthickness=0)
        self.width = width
        self.height = height
        self.callback = callback
        self.val = 0
        self.max_val = 100
        self.is_dragging = False

        self.track = self.create_line(10, height//2, width-10, height//2, fill="#e0e0e0", width=2)
        self.thumb = self.create_oval(0, 0, 10, 10, fill=ACCENT, outline=ACCENT)
        
        self.bind("<Button-1>", self._on_click)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)
        self._update_thumb()

    def _update_thumb(self):
        pct = self.val / self.max_val if self.max_val > 0 else 0
        x = 10 + (pct * (self.width - 20))
        y = self.height // 2
        self.coords(self.thumb, x-5, y-5, x+5, y+5)

    def set_val(self, val):
        if not self.is_dragging:
            self.val = val
            self._update_thumb()

    def _on_click(self, event):
        self.is_dragging = True
        self._move_thumb(event.x)

    def _on_drag(self, event):
        self._move_thumb(event.x)

    def _on_release(self, event):
        self.is_dragging = False
        if self.callback:
            self.callback(self.val)

    def _move_thumb(self, x):
        x = max(10, min(x, self.width - 10))
        pct = (x - 10) / (self.width - 20)
        self.val = pct * self.max_val
        self._update_thumb()

class MusicGUI:
    def __init__(self, player, playlist, settings):
        self.player = player
        self.playlist = playlist
        self.settings = settings

        self.root = TkinterDnD.Tk()
        self.root.title("Music Player")
        self.root.geometry("850x550")
        self.root.configure(bg=BG)

        self.build_ui()
        self.refresh_playlist_ui()
        self.update_progress()

    def build_ui(self):
        # Main Layout
        self.left = tk.Frame(self.root, bg=BG, width=400)
        self.left.pack(side="left", fill="both", expand=True, padx=20)
        
        self.right = tk.Frame(self.root, bg=BOX_BG, width=450)
        self.right.pack(side="right", fill="both", expand=True)
        
        self.build_left_panel()
        self.build_right_panel()

    def build_left_panel(self):
        # Cover Art
        try:
            img = Image.open("assets/default_cover.png")
            img = img.resize((250, 250), Image.Resampling.LANCZOS)
            self.cover_image = ImageTk.PhotoImage(img)
            self.cover_label = tk.Label(self.left, image=self.cover_image, bg=BG)
        except:
            self.cover_label = tk.Label(self.left, text="No Cover Art", bg=BOX_BG, width=30, height=15)
        self.cover_label.pack(pady=40)

        # Progress Slider
        self.progress_slider = CanvasSlider(self.left, width=300, callback=self.on_seek)
        self.progress_slider.pack(pady=10)

        # Controls
        ctrl_frame = tk.Frame(self.left, bg=BG)
        ctrl_frame.pack(pady=20)

        tk.Button(ctrl_frame, text="⏮", font=("Arial", 20), bg=BG, bd=0, command=self.prev_song).pack(side="left", padx=15)
        self.play_btn = tk.Button(ctrl_frame, text="▶", font=("Arial", 24), bg=BG, bd=0, command=self.toggle_play)
        self.play_btn.pack(side="left", padx=15)
        tk.Button(ctrl_frame, text="⏭", font=("Arial", 20), bg=BG, bd=0, command=self.next_song).pack(side="left", padx=15)

    def build_right_panel(self):
        tk.Label(self.right, text="PLAYLISTS", font=("Arial", 12, "bold"), bg=BOX_BG).pack(pady=(20, 5))
        
        # Playlist Selection
        self.pl_var = tk.StringVar()
        # FIXED: Changed current_playlist_name to current_playlist
        self.pl_var.set(self.playlist.current_playlist)
        
        self.pl_dropdown = tk.OptionMenu(self.right, self.pl_var, *self.playlist.get_all_playlist_names(), command=self.change_playlist)
        self.pl_dropdown.config(bg=BOX_BG, bd=0, highlightthickness=0)
        self.pl_dropdown.pack(pady=5)

        # Song Listbox
        self.listbox = tk.Listbox(self.right, bg=BOX_BG, bd=0, highlightthickness=0, font=("Arial", 10), selectbackground="#e0e0e0")
        self.listbox.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Drag & Drop Binding
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.drop_files)

        # Bottom Buttons
        btn_frame = tk.Frame(self.right, bg=BOX_BG)
        btn_frame.pack(fill="x", side="bottom", pady=10)
        
        tk.Button(btn_frame, text="+ New Playlist", bg=BOX_BG, bd=0, command=self.new_playlist).pack(side="left", padx=20)
        tk.Button(btn_frame, text="+ Add Songs", bg=BOX_BG, bd=0, command=self.add_songs_dialog).pack(side="right", padx=20)
class MusicGUI:
    def __init__(self, player, playlist, settings):
        self.player = player
        self.playlist = playlist
        self.settings = settings

        self.root = TkinterDnD.Tk()
        self.root.title("Music Player")
        self.root.geometry("850x550")
        self.root.configure(bg=BG)

        self.build_ui()
        self.refresh_playlist_ui()
        
        # Set initial volume from database
        self.player.set_volume(self.settings.volume)
        
        self.update_progress()

    def build_ui(self):
        self.left = tk.Frame(self.root, bg=BG, width=400)
        self.left.pack(side="left", fill="both", expand=True, padx=20)
        
        self.right = tk.Frame(self.root, bg=BOX_BG, width=450)
        self.right.pack(side="right", fill="both", expand=True)
        
        self.build_left_panel()
        self.build_right_panel()

    def build_left_panel(self):
        # Cover Art
        try:
            img = Image.open("assets/default_cover.png")
            img = img.resize((250, 250), Image.Resampling.LANCZOS)
            self.cover_image = ImageTk.PhotoImage(img)
            self.cover_label = tk.Label(self.left, image=self.cover_image, bg=BG)
        except:
            self.cover_label = tk.Label(self.left, text="No Cover Art", bg=BOX_BG, width=30, height=15)
        self.cover_label.pack(pady=(40, 10))

        # Progress Slider
        self.progress_slider = CanvasSlider(self.left, width=300, callback=self.on_seek)
        self.progress_slider.pack(pady=10)

        # Playback Controls
        ctrl_frame = tk.Frame(self.left, bg=BG)
        ctrl_frame.pack(pady=10)
        tk.Button(ctrl_frame, text="⏮", font=("Arial", 20), bg=BG, bd=0, command=self.prev_song).pack(side="left", padx=15)
        self.play_btn = tk.Button(ctrl_frame, text="▶", font=("Arial", 24), bg=BG, bd=0, command=self.toggle_play)
        self.play_btn.pack(side="left", padx=15)
        tk.Button(ctrl_frame, text="⏭", font=("Arial", 20), bg=BG, bd=0, command=self.next_song).pack(side="left", padx=15)

        # --- NEW: Volume Slider ---
        vol_frame = tk.Frame(self.left, bg=BG)
        vol_frame.pack(pady=20)
        tk.Label(vol_frame, text="🔈", bg=BG, font=("Arial", 12)).pack(side="left")
        self.vol_slider = CanvasSlider(vol_frame, width=150, callback=self.change_volume)
        self.vol_slider.pack(side="left", padx=10)
        self.vol_slider.set_val(self.settings.volume)

    def build_right_panel(self):
        tk.Label(self.right, text="PLAYLISTS", font=("Arial", 12, "bold"), bg=BOX_BG).pack(pady=(20, 5))
        
        self.pl_var = tk.StringVar()
        self.pl_var.set(self.playlist.current_playlist)
        
        self.pl_dropdown = tk.OptionMenu(self.right, self.pl_var, *self.playlist.get_all_playlist_names(), command=self.change_playlist)
        self.pl_dropdown.config(bg=BOX_BG, bd=0, highlightthickness=0)
        self.pl_dropdown.pack(pady=5)

        self.listbox = tk.Listbox(self.right, bg=BOX_BG, bd=0, highlightthickness=0, font=("Arial", 10), selectbackground="#e0e0e0")
        self.listbox.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.drop_files)

        # --- UPDATED: Bottom Button Panel ---
        btn_frame = tk.Frame(self.right, bg=BOX_BG)
        btn_frame.pack(fill="x", side="bottom", pady=15)
        
        # Playlist controls (Left side)
        pl_btns = tk.Frame(btn_frame, bg=BOX_BG)
        pl_btns.pack(side="left", padx=20)
        tk.Button(pl_btns, text="+ New", bg=BOX_BG, bd=0, font=("Arial", 9), command=self.new_playlist).pack(side="left")
        tk.Button(pl_btns, text="🗑 Delete", fg="red", bg=BOX_BG, bd=0, font=("Arial", 9), command=self.delete_playlist_ui).pack(side="left", padx=10)
        
        # Song controls (Right side)
        sg_btns = tk.Frame(btn_frame, bg=BOX_BG)
        sg_btns.pack(side="right", padx=20)
        tk.Button(sg_btns, text="🗑 Remove", fg="red", bg=BOX_BG, bd=0, font=("Arial", 9), command=self.remove_song_ui).pack(side="left", padx=10)
        tk.Button(sg_btns, text="+ Add", bg=BOX_BG, bd=0, font=("Arial", 9), command=self.add_songs_dialog).pack(side="left")

    def change_volume(self, val):
        self.player.set_volume(val)
        self.settings.save(val)

    def remove_song_ui(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            songs = self.playlist.get_all_songs()
            song_to_remove = songs[index]
            self.playlist.remove_song(song_to_remove)
            self.refresh_playlist_ui()
        else:
            messagebox.showwarning("Selection", "Please select a song to remove.")

    def delete_playlist_ui(self):
        current = self.playlist.current_playlist
        if messagebox.askyesno("Delete", f"Are you sure you want to delete '{current}'?"):
            self.playlist.delete_playlist(current)
            self.refresh_playlist_ui()
            
    def refresh_playlist_ui(self):
        self.listbox.delete(0, tk.END)
        # FIXED: Using the bridged function
        for song in self.playlist.get_all_songs():
            self.listbox.insert(tk.END, os.path.basename(song))
        
        # Refresh Dropdown
        menu = self.pl_dropdown["menu"]
        menu.delete(0, "end")
        for name in self.playlist.get_all_playlist_names():
            menu.add_command(label=name, command=lambda value=name: self.change_playlist(value))
        
        # FIXED: Changed current_playlist_name to current_playlist
        self.pl_var.set(self.playlist.current_playlist)

    def drop_files(self, event):
        files = self.root.tk.splitlist(event.data)
        for f in files:
            if f.lower().endswith(('.mp3', '.wav')):
                self.playlist.add_song(f)
        self.refresh_playlist_ui()

    def add_songs_dialog(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav")])
        for f in files:
            self.playlist.add_song(f)
        self.refresh_playlist_ui()

    def new_playlist(self):
        name = simpledialog.askstring("New Playlist", "Enter playlist name:")
        if name:
            self.playlist.create_playlist(name)
            self.refresh_playlist_ui()

    def change_playlist(self, name):
        self.playlist.switch_playlist(name)
        self.refresh_playlist_ui()

    def toggle_play(self):
        if self.player.is_playing:
            self.player.pause()
            self.play_btn.config(text="▶")
        else:
            # If nothing is loaded, play the first song in the list
            if not self.player.current_song:
                songs = self.playlist.get_all_songs()
                if songs:
                    self.player.load_song(songs[0])
            self.player.unpause()
            self.play_btn.config(text="⏸")

    def next_song(self):
        song = self.playlist.next_song()
        if song:
            self.player.load_song(song)
            self.play_btn.config(text="⏸")

    def prev_song(self):
        song = self.playlist.prev_song()
        if song:
            self.player.load_song(song)
            self.play_btn.config(text="⏸")

    def on_seek(self, val):
        if self.player.current_song:
            self.player.seek(val)

    def update_progress(self):
        if self.player.is_playing and not self.progress_slider.is_dragging:
            curr = self.player.get_position()
            total = self.player.length
            self.progress_slider.max_val = total
            self.progress_slider.set_val(curr)
            
            # Auto-next
            if curr >= total - 0.5 and total > 0:
                self.next_song()
                
        self.root.after(500, self.update_progress)

    def run(self):
        self.root.mainloop()