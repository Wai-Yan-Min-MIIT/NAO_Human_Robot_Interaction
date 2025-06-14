# tts_client.py (Python 3.12.2)
import socket

def send_message_to_nao(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))
    client_socket.sendall(message.encode('utf-8'))
    response = client_socket.recv(1024)
    print('Response from server:', response.decode('utf-8'))
    client_socket.close()

# Example usage (can be commented out or removed)
# if __name__ == "__main__":
#     message = "Hello, Nao!"
#     send_message_to_nao(message)
