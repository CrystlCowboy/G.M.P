import tkinter as tk
import vlc
from tkinter import filedialog
import os
import json

class MusicPlayer:
    def __init__(self, master):
        master.title("Music Player")

        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        self.player = self.instance.media_player_new()

        self.playlist_file = 'playlist.json'  # File to save the playlist

        self.playlist_box = tk.Listbox(master, height=25, width=60)  # New listbox for the playlist
        self.playlist_box.pack()

        if os.path.exists(self.playlist_file):  # If the playlist file exists
            with open(self.playlist_file, 'r') as f:  # Open the file
                self.playlist = json.load(f)  # Load the playlist from the file
                for song in self.playlist:  # Add each song in the playlist to the playlist box
                    self.playlist_box.insert(tk.END, song)  # Corrected line
        else:
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

        self.remove_button = tk.Button(master, text="Remove Song", command=self.remove_song)  # New button for removing songs
        self.remove_button.pack()

        self.delete_button = tk.Button(master, text="Delete Playlist", command=self.delete_playlist)  
        self.delete_button.pack()

    def add_to_playlist_ui(self):
        filename = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp4")])
        if filename:
            self.playlist.append(filename)
            self.playlist_box.insert(tk.END, filename)  # Add the song to the playlist box
            with open(self.playlist_file, 'w') as f:  # Open the playlist file
                json.dump(self.playlist, f)  # Save the playlist to the file

    def delete_playlist(self):  # New method to delete the playlist
        self.player.stop()  # Stop the player
        self.playlist.clear()  # Clear the playlist
        self.playlist_box.delete(0, tk.END)  # Clear the playlist box
        self.current_song_index = 0  # Reset the current song index
        with open(self.playlist_file, 'w') as f:  # Open the playlist file
            json.dump(self.playlist, f)  # Save the empty playlist to the file

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