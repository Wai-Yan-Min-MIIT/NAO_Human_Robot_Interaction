# text_to_speech.py (Python 2.7)
import socket
from naoqi import ALProxy

# Naoqi setup
#nao_ip = "192.168.1.21"  # Replace with your Nao's IP address
#nao_ip = "172.16.215.13"
nao_ip = "172.16.100.11"
nao_port = 9559
tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)

# Create a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen(1)

print("TTS Server is listening...")

while True:
    conn, addr = server_socket.accept()
    print('Connected by', addr)
    data = conn.recv(1024)
    if not data:
        break
    message = data.decode('utf-8')
    print('Received:', message)
    
    # Ensure message is a UTF-8 encoded string, not Unicode
    try:
        tts.say(str(message))
    except RuntimeError as e:
        print("Error in tts.say:", e)

    conn.sendall(b'Message received')
    conn.close()
