import tkinter as tk

class VirtualKeyboard:
    def __init__(self, root, text_entry):
        self.text_entry = text_entry
        self.virtual_keyboard = tk.Toplevel(root)
        self.virtual_keyboard.withdraw()

        # Define the layout of the virtual keyboard
        keyboard_layout = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '<-'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
            [' ', '.', ',', '?', '!', ':', ';', '<', '>']
        ]

        # Create buttons for each key in the virtual keyboard layout
        for row in keyboard_layout:
            row_frame = tk.Frame(self.virtual_keyboard)
            row_frame.pack(fill=tk.X)
            for key in row:
                button = tk.Button(row_frame, text=key, width=5)
                button.bind("<Button-1>", self.button_click)
                button.pack(side=tk.LEFT)

    def button_click(self, event):
        key = event.widget.cget("text")
        if key == '<-':  # If the backspace button is clicked
            # Delete the last character in the text entry field
            if self.text_entry.get():
                self.text_entry.delete(len(self.text_entry.get())-1)
        else:  # If any other button is clicked
            # Insert the corresponding character into the text entry field
            self.text_entry.insert(tk.END, key)

    # Function to show the virtual keyboard
    def show(self):
        self.virtual_keyboard.deiconify()