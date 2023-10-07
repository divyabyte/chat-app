import socket
import threading

HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 3000      # Port to listen on

# Dictionary to store client connections
clients = {}

def handle_client(client_socket, client_address):
    client_name = client_socket.recv(1024).decode().strip()
    clients[client_name] = client_socket

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print(f"Connection closed by {client_address} ({client_name})")
                del clients[client_name]
                client_socket.close()
                break
            print(f"Received message from {client_address} ({client_name}): {data.decode('utf-8', 'ignore')}")

            # Check if the message is intended for a specific client
            message = data.decode('utf-8', 'ignore').strip()
            message = message.strip("'")  # Remove the single quotes
            if message.startswith('@'):
                recipient, private_message = message.split(' ', 1)
                recipient = recipient[1:]  # Remove the '@' symbol
                if recipient in clients:
                    clients[recipient].sendall(f"{client_name}: {private_message}".encode())
                else:
                    client_socket.sendall("User not found or offline.".encode())
            else:
                client_socket.sendall("Please specify user name with @.".encode())
        except Exception as e:
            print(f"Error: {e}")
            del clients[client_name]
            client_socket.close()
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()
