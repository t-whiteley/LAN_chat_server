import socket
import threading

CLIENT_IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT = '!DISC'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((CLIENT_IP, PORT))

exit_pass = False

def send():
    while True:
        msg = input('')
        msg_len = len(msg)
        send_len = str(msg_len).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))
        send_msg = msg.encode(FORMAT)
        client.send(send_len)
        client.send(send_msg)

        if msg == DISCONNECT:
            exit_pass = True
            break


def receive():
    while not exit_pass:
        msg_len = client.recv(HEADER).decode(FORMAT)
        addr = client.recv(HEADER).decode(FORMAT).strip()
        msg = client.recv(int(msg_len)).decode(FORMAT)
        print(f'<{addr}> {msg}')


send_thread = threading.Thread(target=send)
send_thread.start()

receive_thread = threading.Thread(target=receive)
receive_thread.start()