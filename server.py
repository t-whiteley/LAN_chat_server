import socket
import threading

SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT = '!DISC'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, PORT))

client_count = []

def start():
    server.listen()
    print('[SERVER STARTED]')
    while True:
        conn, addr = server.accept()
        client_count.append((conn, addr))
        thread = threading.Thread(target=handleclient, args=(conn, addr))
        thread.start()

def handleclient(conn, addr):
    print(f'[{addr[0]} connected - {len(client_count)} online]')
    while True:
        msg_len = conn.recv(HEADER).decode(FORMAT)
        msg = conn.recv(int(msg_len)).decode(FORMAT)

        if msg == DISCONNECT:
            client_count.remove((conn, addr))
            print(f'[{addr[0]} disconnected - {len(client_count)} online]')
            break
        else:
            print(f'<{addr[0]}> {msg}')
            broadcast(msg, conn, addr)



def broadcast(msg, conn, addr):
    send_len = str(len(msg)).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    send_addr = str(addr[0]).encode(FORMAT)
    send_addr += b' ' * (HEADER - len(send_addr))
    send_msg = msg.encode(FORMAT)


    for client in client_count:
        client_conn = client[0]
        client_conn.send(send_len)
        client_conn.send(send_addr)
        client_conn.send(send_msg)


start()