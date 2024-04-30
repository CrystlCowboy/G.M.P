import tkinter as tk
import vlc
from tkinter import filedialog
import os
import json
import tkinter.messagebox as messagebox
import VirtualKeyboard as vk

class MusicPlayer:
    def __init__(self, master):
        master.title("Music Player")

        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        self.player = self.instance.media_player_new()

        self.playlist_box = tk.Listbox(master, height=25, width=60)  # New listbox for the playlist
        self.playlist_box.pack()

        self.save_entry = tk.Entry(master)  # Create a text entry widget
        self.virtual_keyboard = vk.VirtualKeyboard(master, self.save_entry)

        self.playlists_file = 'playlists.json'  # File to save the playlists

        try:
            with open(self.playlists_file, 'r') as f:  # Try to open the file
                self.playlists = json.load(f)  # Load the playlists from the file
        except FileNotFoundError:
            self.playlists = {}

        self.playlist = []
        self.current_song_index = 0

        self.play_button = tk.Button(master, text="Play", command=self.play)
        self.play_button.pack()

        self.pause_button = tk.Button(master, text="Pause", command=self.pause)
        self.pause_button.pack()

        self.stop_button = tk.Button(master, text="Stop", command=self.stop)
        self.stop_button.pack()

        self.next_button = tk.Button(master, text="Next", command=self.next)
        self.next_button.pack()

        self.prev_button = tk.Button(master, text="Previous", command=self.previous)
        self.prev_button.pack()

        self.add_button = tk.Button(master, text="Add to Playlist", command=self.add_to_playlist_ui)
        self.add_button.pack()

        self.remove_button = tk.Button(master, text="Remove Song", command=self.remove_song)
        self.remove_button.pack()

        self.load_entry = tk.Entry(master)
        self.load_entry.pack()
        self.load_button = tk.Button(master, text="Load Playlist", command=self.load_playlist_ui)
        self.load_button.pack()

        self.save_entry = tk.Entry(master)
        self.save_entry.pack()
        self.save_button = tk.Button(master, text="Save Playlist", command=self.save_playlist)
        self.save_button.pack()

        self.virtual_keyboard = vk.VirtualKeyboard(master, self.save_entry)

        self.keyboard_button = tk.Button(master, text="Virtual Keyboard", command=self.virtual_keyboard.show)
        self.keyboard_button.pack()

        self.delete_button = tk.Button(master, text="Delete Playlist", command=self.delete_playlist)  
        self.delete_button.pack()

    def launch_virtual_keyboard(self):
        self.virtual_keyboard.show()

    def add_to_playlist_ui(self):
        filename = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp4")])
        if filename:
            self.playlist.append(filename)
            self.playlist_box.insert(tk.END, filename)  # Add the song to the playlist box
            with open(self.playlist_file, 'w') as f:  # Open the playlist file
                json.dump(self.playlist, f)  # Save the playlist to the file

    def save_playlist(self):
        playlist_name = self.save_entry.get()
        self.playlists[playlist_name] = self.playlist
        with open(self.playlists_file, 'w') as f:
            json.dump(self.playlists, f)

    def load_playlist_ui(self):
        playlist_name = self.load_entry.get()
        self.load_playlist(playlist_name)

    def load_playlist(self, playlist_name):
        if playlist_name in self.playlists:
            self.playlist = self.playlists[playlist_name]
            self.playlist_box.delete(0, tk.END)
            for song in self.playlist:
                self.playlist_box.insert(tk.END, song)
        else:
            messagebox.showerror("Error", f"No playlist named {playlist_name}")

    def delete_playlist(self):
        playlist_name = self.load_entry.get()  # Get the name of the playlist to delete
        if playlist_name in self.playlists:
            del self.playlists[playlist_name]  # Remove the playlist from the dictionary
            with open(self.playlists_file, 'w') as f:  # Open the playlists file
                json.dump(self.playlists, f)  # Save the updated playlists to the file
            self.player.stop()  # Stop the player
            self.playlist.clear()  # Clear the playlist
            self.playlist_box.delete(0, tk.END)  # Clear the playlist box
        else:
            messagebox.showerror("Error", f"No playlist named {playlist_name}")

    def remove_song(self):  # New method to remove songs
        selected_song_index = self.playlist_box.curselection()  # Get the index of the selected song
        if selected_song_index:
            selected_song_index = selected_song_index[0]
            if selected_song_index == self.current_song_index:  # If the song being removed is the current song
                self.player.stop()  # Stop the player
            self.playlist_box.delete(selected_song_index)  # Remove the song from the listbox
            del self.playlist[selected_song_index]  # Remove the song from the playlist
            if selected_song_index < self.current_song_index:  # If the removed song was before the current song
                self.current_song_index -= 1  # Decrement the current song index
            with open(self.playlist_file, 'w') as f:  # Open the playlist file
                json.dump(self.playlist, f)  # Save the playlist to the file

    def play(self):
        selected_song_index = self.playlist_box.curselection()  # Get the index of the selected song
        if selected_song_index:  # If a song is selected
            selected_song_index = selected_song_index[0]  # curselection returns a tuple, so get the first item
            self.current_song_index = selected_song_index  # Set the current song index to the selected song index
        if self.playlist:  # If there are songs in the playlist
            media = self.instance.media_new(self.playlist[self.current_song_index])  # Get the media for the current song
            self.player.set_media(media)  # Set the media for the player
            self.player.play()  # Play the song

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def next(self):
        if self.playlist:
            self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
            self.play()

    def previous(self):
        if self.playlist:
            self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
            self.play()

root = tk.Tk()
app = MusicPlayer(root)
root.mainloop()