import tkinter as tk
import vlc
from tkinter import filedialog
import os
import json
import tkinter.messagebox as messagebox
import VirtualKeyboard as vk

class MusicPlayer:
    def __init__(self, master):
        master.title("G.M.P. - Gym Music Player")

        # Get screen width and height
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Set window size to screen size
        master.geometry(f"{screen_width}x{screen_height}")
   
        self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
        self.player = self.instance.media_player_new()

        # Create a label for the song listbox
        self.playlist_label = tk.Label(master, text="Songs in current playlist:")
        self.playlist_label.pack()

        self.playlist_box = tk.Listbox(master, height=20, width=75)  # New listbox for the playlist
        self.playlist_box.pack()

        # Create a label for the playlist listbox
        self.playlist_listbox_label = tk.Label(master, text="Saved playlists:")
        self.playlist_listbox_label.pack()

        self.save_entry = tk.Entry(master)  # Create a text entry widget
        self.virtual_keyboard = vk.VirtualKeyboard(master, self.save_entry)

        self.playlists_file = 'playlists.json'  # File to save the playlists

        try:
            with open(self.playlists_file, 'r') as f:  # Try to open the file
                self.playlists = json.load(f)  # Load the playlists from the file
        except FileNotFoundError:
            self.playlists = {}
        except PermissionError:
            messagebox.showerror("Error", "Permission denied")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding JSON")
        except Exception as e:
            messagebox.showerror("Error", str(e))

        self.playlist_listbox = tk.Listbox(master)
        self.playlist_listbox.pack()

        # After loading the playlists from the file
        self.update_playlist_listbox()

        # After saving a playlist
        playlist_name = self.save_entry.get()  # Get the playlist name from the text entry widget
        if playlist_name:  # If the user entered a playlist name
            self.playlists[playlist_name] = self.playlists  # Add the new playlist to self.playlists

        # After deleting a playlist
        if playlist_name in self.playlists:  # If the playlist exists
            del self.playlists[playlist_name]  # Delete the playlist
        self.update_playlist_listbox()

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

        self.load_entry = tk.Entry(master)  # Create a text entry widget for loading playlists
        self.load_entry.pack()
        self.load_button = tk.Button(master, text="Load Playlist", command=self.load_playlist_ui)
        self.load_entry.bind('<FocusIn>', self.focus_in_load_entry)
        self.load_button.pack()

        self.save_entry = tk.Entry(master)
        self.save_entry.pack()
        self.save_button = tk.Button(master, text="Save Playlist", command=self.save_playlist)
        self.save_entry.bind('<FocusIn>', self.focus_in_save_entry)
        self.save_button.pack()

        self.virtual_keyboard = vk.VirtualKeyboard(master, self.save_entry)

        self.keyboard_button = tk.Button(master, text="Virtual Keyboard", command=self.virtual_keyboard.show)
        self.keyboard_button.pack()

        self.delete_button = tk.Button(master, text="Delete Playlist")
        self.delete_button.pack()
        self.delete_button.bind('<Button-1>', lambda event: self.delete_playlist())

    def launch_virtual_keyboard(self):
        self.virtual_keyboard.show()

    def update_playlist_listbox(self):
        self.playlist_listbox.delete(0, tk.END)  # Clear the listbox
        for playlist_name in self.playlists:  # Loop through the saved playlists
            self.playlist_listbox.insert(tk.END, playlist_name)  # Add each playlist name to the listbox

    def add_to_playlist_ui(self):
        filename = filedialog.askopenfilename(filetypes=[("Music Files", "*.mp4")])
        if filename:
            self.playlist.append(filename)
            self.playlist_box.insert(tk.END, filename)  # Add the song to the playlist box
            with open(self.playlist_file, 'w') as f:  # Open the playlist file
                json.dump(self.playlist, f)  # Save the playlist to the file

    def focus_in_save_entry(self, event):
        self.virtual_keyboard.text_entry = self.save_entry

    def save_playlist(self):
        playlist_name = self.save_entry.get()
        if not playlist_name.strip():  # Check if the playlist name is empty
            messagebox.showerror("Error", "You have to name a playlist")
            return
        confirm = messagebox.askyesno("Confirm", "Do you want to save this playlist? You may have to restart the program afterwards to see results.")
        if confirm:
            self.playlists[playlist_name] = self.playlist
            with open(self.playlists_file, 'w') as f:
                json.dump(self.playlists, f)

    def focus_in_load_entry(self, event):
        self.virtual_keyboard.text_entry = self.load_entry

    def load_playlist_ui(self):
        # Get the selected playlist name from the listbox
        selected = self.playlist_listbox.curselection()
        if selected: 
            playlist_name = self.playlist_listbox.get(selected[0])
            self.load_playlist(playlist_name)
        else:
            messagebox.showerror("Error", "No playlist selected")

    def load_playlist(self, playlist_name):
        if playlist_name in self.playlists:
            self.playlist = self.playlists[playlist_name]
            self.playlist_box.delete(0, tk.END)
            for song in self.playlist:
                self.playlist_box.insert(tk.END, song)
        else:
            messagebox.showerror("Error", f"No playlist named {playlist_name}")

    def delete_playlist(self):
        # Get the selected playlist name from the listbox
        selected = self.playlist_listbox.curselection()
        if selected:  # If a playlist is selected
            playlist_name = self.playlist_listbox.get(selected[0])
        else:
            messagebox.showerror("Error", "No playlist selected")
            return
        if playlist_name not in self.playlists:  # Check if the playlist exists
            messagebox.showerror("Error", "Playlist not found")
            return
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete the highlighted playlist?")
        if confirm:
            del self.playlists[playlist_name]
            with open(self.playlists_file, 'w') as f:
                json.dump(self.playlists, f)
            self.playlist_listbox.delete(selected[0])  # Remove the playlist from the listbox

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