import socket
import threading
import csv
import datetime

PORT = 8020
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

HEADER = 1024
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def clients(conn, addr, clients_conn):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:

        msg = conn.recv(1024).decode(FORMAT)

        with open('log.csv', mode='a') as log:
            fieldnames = ['address', 'date', 'time', 'message']
            write = csv.DictWriter(log, fieldnames=fieldnames)
            address = str(addr[0]), str(addr[1])
            current_time = datetime.datetime.now()
            date = current_time.date()
            time = current_time.time()
            message = msg

            fill = {
                'address': address,
                'date': date,
                'time': time,
                'message': message
            }
            write.writerow(fill)

        msg = int(msg)
        print(f"[{addr}] just send {msg}")
        if msg == 1 or msg == 2:
            conn.send(("OK SEND THE NUMBERS").encode())
            a = conn.recv(1024).decode(FORMAT)
            b = conn.recv(1024).decode(FORMAT)
            if msg == 1:
                print(f"Addition operation is performed for {addr}")
                ans = add(int(a), int(b))
                conn.send(("add").encode())
                conn.send(str(ans).encode(FORMAT))
            if msg == 2:
                print(f"Subtraction operation is performed for {addr}")
                ans = sub(int(a), int(b))
                conn.send(("sub").encode())
                conn.send(str(ans).encode(FORMAT))
        if msg == 3:
            connected = False

    print(f'Disconnected {addr}')
    clients_conn.remove(str(addr))


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    clients_conn = []
    while True:
        conn, addr = server.accept()
        clients_conn.append(str(addr))
        thread = threading.Thread(target=clients, args=(conn, addr, clients_conn))
        thread.start()

        print(
            f"[ACTIVE CONNECTIONS] = {threading.activeCount() - 1}")  # -1 because one active thread is already running ie. start()


print("[STARTING] server is starting...")
start()
