import socket
import threading

# Constants
SERVER_IP = '127.0.0.1'
TCP_PORT = 12345
UDP_PORT = 12346
BUFFER_SIZE = 1024

# Function to handle receiving messages from the server
def receive_tcp_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            print(data.decode('utf-8'))
        except Exception as e:
            print(f"Error: {str(e)}")
            break

# Create a TCP socket for the client
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((SERVER_IP, TCP_PORT))

# Create a thread to receive TCP messages
tcp_receive_thread = threading.Thread(target=receive_tcp_messages, args=(tcp_socket,))
tcp_receive_thread.start()

# Function to handle receiving UDP messages from the server
def receive_udp_messages():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', UDP_PORT))
    while True:
        try:
            data, addr = udp_socket.recvfrom(BUFFER_SIZE)
            print(data.decode('utf-8'))
        except Exception as e:
            print(f"Error: {str(e)}")
            break

# Create a thread to receive UDP messages
udp_receive_thread = threading.Thread(target=receive_udp_messages)
udp_receive_thread.start()

# Main client loop for sending messages
try:
    while True:
        message = input()
        if message:
            tcp_socket.send(message.encode('utf-8'))
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.sendto(message.encode('utf-8'), (SERVER_IP, UDP_PORT))
except KeyboardInterrupt:
    print("Client shutting down.")
finally:
    tcp_socket.close()


