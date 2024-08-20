import socket
import threading
import customtkinter as ctk
from tkinter import messagebox

# CustomTkinter setup
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

# Client setup
SERVER_HOST = '10.8.3.77'  # Your server's IP address
SERVER_PORT = 12345         # Server port
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Str8Box(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Str8 Box")
        self.geometry("500x400")

        # Chat display area
        self.chat_display = ctk.CTkTextbox(self, width=400, height=300, wrap="word")
        self.chat_display.grid(row=0, column=0, padx=10, pady=10)
        self.chat_display.configure(state="disabled")

        # Message entry field
        self.message_entry = ctk.CTkEntry(self, width=300)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Send button
        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        # Start the client connection
        try:
            client.connect((SERVER_HOST, SERVER_PORT))
            threading.Thread(target=self.receive_messages).start()
        except:
            messagebox.showerror("Connection Error", "Unable to connect to the server.")
            self.destroy()

    def receive_messages(self):
        """
        Handles receiving messages from the server and displaying them in the chat box.
        """
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message:
                    self.chat_display.configure(state="normal")
                    self.chat_display.insert("end", message + "\n")
                    self.chat_display.configure(state="disabled")
                    self.chat_display.yview("end")
            except:
                print("An error occurred. Connection closed.")
                client.close()
                break

    def send_message(self):
        """
        Sends the message typed in the entry field to the server.
        """
        message = self.message_entry.get()
        if message:
            client.send(message.encode('utf-8'))
            self.message_entry.delete(0, 'end')

if __name__ == "__main__":
    app = Str8Box()
    app.mainloop()
