import socket
import threading
import os
import tkinter as tk  # Import tkinter for Listbox
import customtkinter as ctk
from tkinter import filedialog

# Client setup
SERVER_HOST = '10.8.3.77'
SERVER_PORT = 12345

class Str8Box(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Str8 Box")
        self.geometry("600x400")

        # Initialize Client
        self.username = input("Enter your username: ")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER_HOST, SERVER_PORT))
        self.client.send(self.username.encode('utf-8'))

        # Chat display area
        self.chat_display = ctk.CTkTextbox(self, width=400, height=300, wrap="word")
        self.chat_display.grid(row=0, column=0, padx=10, pady=10)
        self.chat_display.configure(state="disabled")

        # User list
        self.user_list = tk.Listbox(self, width=25, height=18)  # Use tkinter Listbox
        self.user_list.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Message entry field
        self.message_entry = ctk.CTkEntry(self, width=300)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Bind Enter key to send message
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        # Send button
        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        # File button
        self.file_button = ctk.CTkButton(self, text="Send File", command=self.send_file)
        self.file_button.grid(row=2, column=0, padx=10, pady=10)

        # Typing indicator
        self.message_entry.bind("<KeyPress>", self.typing_indicator)
        self.typing_indicator_sent = False  # To track if the typing indicator has been sent

        # Status label
        self.status_label = ctk.CTkLabel(self, text="Connected")
        self.status_label.grid(row=2, column=1, padx=10, pady=10)

        # Start receiving messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message.startswith("USER_LIST"):
                    users = message[len("USER_LIST "):].split(",")
                    self.user_list.delete(0, 'end')
                    for user in users:
                        self.user_list.insert("end", user)
                elif message.startswith("FILE"):
                    self.display_message(message)
                else:
                    self.display_message(message)
            except Exception as e:
                self.update_status(f"Disconnected: {e}")
                self.client.close()
                break

    def send_message(self):
        message = self.message_entry.get()
        if message:
            full_message = f"{self.username}: {message}"
            self.client.send(full_message.encode('utf-8'))

            # Display the message without re-adding the username
            self.display_message(f"You: {message}")
            self.message_entry.delete(0, 'end')


    def send_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            file_name = file_path.split("/")[-1]
            file_size = os.path.getsize(file_path)
            self.client.send(f"FILE {file_name} {file_size}".encode('utf-8'))
            with open(file_path, "rb") as f:
                self.client.send(f.read())

    def typing_indicator(self, event):
        if not self.typing_indicator_sent:
            self.client.send("TYPING".encode('utf-8'))
            self.typing_indicator_sent = True  # Send typing indicator only once

    def display_message(self, message):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", message + "\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.yview("end")

    def update_status(self, status):
        self.status_label.configure(text=status)

if __name__ == "__main__":
    app = Str8Box()
    app.mainloop()
