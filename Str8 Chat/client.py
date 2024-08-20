import socket
import threading

# Client setup
SERVER_HOST = '10.8.3.77'  # Your server's IP address
SERVER_PORT = 12345        # Server port
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receive_messages(self):
    """
    Handles receiving messages from the server and displaying them in the chat box.
    """
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                self.after(0, self.update_chat_display, message)
        except Exception as e:
            print(f"Error: {e}")
            client.close()
            break

def update_chat_display(self, message):
    """
    Updates the chat display area with new messages.
    """
    self.chat_display.configure(state="normal")
    self.chat_display.insert("end", message + "\n")
    self.chat_display.configure(state="disabled")
    self.chat_display.yview("end")

def send_messages():
    """
    Handles sending messages to the server.
    """
    while True:
        message = input("")
        client.send(message.encode('utf-8'))

def main():
    try:
        # Connect to the server
        client.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to the server at {SERVER_HOST}:{SERVER_PORT}")
        
        # Start a thread to receive messages from the server
        threading.Thread(target=receive_messages).start()

        # Start sending messages to the server
        send_messages()
        
    except:
        print("Unable to connect to the server.")
        client.close()

if __name__ == "__main__":
    main()
