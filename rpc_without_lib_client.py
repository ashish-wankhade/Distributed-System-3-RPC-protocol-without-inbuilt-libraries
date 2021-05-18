import socket

PORT = 8020
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

HEADER = 1024
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

while True:
    message = input("For Addition Press 1\n"
                    "For Subtraction Press 2\n"
                    "For Disconnecting Press 3\n"
                    "Enter Opertion - ")

    client.send(str(message).encode(FORMAT))

    server_response = client.recv(1024).decode(FORMAT)
    print(server_response)

    if server_response == 'OK SEND THE NUMBERS':
        print("Enter the 2 nos.")

        a = int(input("Enter Value of a - "))
        b = int(input("Enter Value of b - "))
        client.send(str(a).encode(FORMAT))
        client.send(str(b).encode(FORMAT))

        operation = client.recv(1024).decode(FORMAT)
        ans = client.recv(1024).decode(FORMAT)
        if operation == "add":
            print(f"Addition of ({a}) + ({b}) = {ans}")
        if operation == "sub":
            print(f"Subtraction of ({a}) - ({b}) = {ans}")
    if message == 3:
        connected = False
