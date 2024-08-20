import socket
import threading

# Server setup
HOST = '10.8.3.77'  # Your local IP address
PORT = 12345        # Port to listen on

# List to keep track of connected clients
clients = []

def broadcast(message, _client):
    """
    Sends the message to all clients except the sender.
    """
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                remove(client)

def handle_client(client):
    """
    Handles communication with a connected client.
    """
    while True:
        try:
            # Receive message from the client
            message = client.recv(1024)
            if message:
                print(f"Received message: {message.decode('utf-8')}")
                broadcast(message, client)
            else:
                remove(client)
                break
        except:
            remove(client)
            break

def remove(client):
    """
    Removes a client from the list of clients and closes the connection.
    """
    if client in clients:
        clients.remove(client)
    client.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server started, listening on {HOST}:{PORT}")

    while True:
        # Accept a new connection
        client, addr = server.accept()
        print(f"New connection from {addr}")

        # Add client to the list of clients
        clients.append(client)

        # Start a new thread to handle the client
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    main()
