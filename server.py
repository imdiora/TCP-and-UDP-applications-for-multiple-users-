
import socket
import threading

# Server configuration
TCP_PORT = 12345
UDP_PORT = 12346

# Create sockets
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind sockets
tcp_socket.bind(('0.0.0.0', TCP_PORT))
udp_socket.bind(('0.0.0.0', UDP_PORT))

# Lists to keep track of connected clients
tcp_clients = []
udp_clients = []

# Function to handle TCP connections
def handle_tcp(client_socket, address):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            # Broadcast the message to all TCP clients
            for client in tcp_clients:
                if client != client_socket:
                    client.send(data)
        except:
            print(f"Client {address} disconnected.")
            tcp_clients.remove(client_socket)
            client_socket.close()
            break

# Function to handle UDP messages
def handle_udp():
    while True:
        data, addr = udp_socket.recvfrom(1024)
        # Broadcast the UDP message to all UDP clients (including sender)
        for client in udp_clients:
            udp_socket.sendto(data, client)

# Start the UDP handler thread
udp_thread = threading.Thread(target=handle_udp)
udp_thread.start()

# Start the TCP server
tcp_socket.listen(5)
print(f"TCP Server listening on port {TCP_PORT}")

while True:
    client, address = tcp_socket.accept()
    print(f"Accepted connection from {address}")
    tcp_clients.append(client)
    client_handler = threading.Thread(target=handle_tcp, args=(client, address))
    client_handler.start()
