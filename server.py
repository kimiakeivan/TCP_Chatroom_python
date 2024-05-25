import socket
import threading
import time
import ast

# 192.168.1.102
PORT = 1532
HOST_IP = "127.0.0.1"
ADDR = (HOST_IP, PORT)
FORMAT = "utf-8"
DICT_CLIENT = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


clients = []
names = []
private_clients = []
new_list = []


# send messages to the all clients that are currently connected to the server
def broadcast(message):
    for client in clients:
        client.send(message)
    print(message.decode(FORMAT))


def private_broadcast(message):
    global  new_list
    for client in new_list:
        client.send(message)
    print(message.decode(FORMAT))


def leave(client):
    client.close()
    index = clients.index(client)
    clients.remove(client)
    name = names[index]
    message = f"{name} left the chat.\n".encode(FORMAT)
    broadcast(message)
    names.remove(name)
    members()


def handle_client(client):
    connected = True
    while connected:

        try:

            message = client.recv(1024)
            msg = message.decode(FORMAT)
            global private_clients
            global new_list

            if msg.startswith("['"):
                msg = msg.split("\n")
                print(msg)
                clientlist = ast.literal_eval(msg[0])
                print(clientlist)
                print(DICT_CLIENT.values())
                new_list = [
                    key for key, value in DICT_CLIENT.items() if value in clientlist
                ]
                print("OK")
                private_broadcast(f"private message from {msg[1]}".encode(FORMAT))

            else:
                broadcast(message)
                if msg.split(": ")[1] == "bye":
                    leave(client)
                    break

        except:
            leave(client)
            break


def members():
    members = f"{names}\n".encode(FORMAT)
    broadcast(members)


def start():
    print(f"[LISTENING] server is listening on {HOST_IP}")
    server.listen()

    while True:
        # accepting clients
        client, address = server.accept()
        print(f"connected with{address}")

        # client.send("NAME".encode(FORMAT))
        name = client.recv(1024).decode(FORMAT)
        clients.append(client)
        names.append(name)
        DICT_CLIENT[client] = name

        # broadcasting the login notification of a new client
        message = f"{name} joined the chat room.\n".encode(FORMAT)
        broadcast(message)

        # sending "Hi" to the client
        client.send(f"Hi {name}, welcome to the chat room.\n".encode(FORMAT))

        members()

        # running a thread for every client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


print("[STARTING] server is starting ...")
time.sleep(0.6)
start()
