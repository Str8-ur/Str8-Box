import socket
import threading
import os

# Server setup
HOST = '10.8.3.77'
PORT = 12345
clients = []  # List of (client_socket, username)

def broadcast(message, client):
    for c, _ in clients:
        if c != client:
            try:
                c.send(message.encode('utf-8'))
            except:
                remove(c)

def remove(client):
    for c, username in clients:
        if c == client:
            clients.remove((c, username))
            broadcast(f"{username} has left the chat.", client)
            break

def broadcast_user_list():
    users = [username for _, username in clients]
    user_list_message = "USER_LIST " + ",".join(users)
    broadcast(user_list_message, None)

def handle_client(client):
    username = client.recv(1024).decode('utf-8')
    clients.append((client, username))
    broadcast(f"{username} has joined the chat.", client)
    broadcast_user_list()

    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message.startswith("@"):
                recipient, private_message = message[1:].split(" ", 1)
                send_private_message(recipient, private_message, client)
            elif message == "TYPING":
                broadcast(f"{username} is typing...", client)
            elif message.startswith("FILE"):
                handle_file_transfer(client, message)
            else:
                broadcast(f"{username}: {message}", client)
        except:
            remove(client)
            break

def send_private_message(recipient, message, sender_client):
    for client, username in clients:
        if username == recipient:
            client.send(message.encode('utf-8'))
            break

def handle_file_transfer(client, file_info):
    file_name, file_size = file_info.split(" ")
    file_size = int(file_size)
    with open(file_name, "wb") as f:
        data = client.recv(file_size)
        f.write(data)
    broadcast(f"File {file_name} has been uploaded.", client)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        client, address = server.accept()
        print(f"Connected with {address}")
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    start_server()
