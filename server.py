import socket
import threading
import time
import ast


PORT = 15000
HOST = "127.0.0.1"
ADDR = (HOST, PORT)
FORMAT = "utf-8"
DICT_CLIENT = {}

clients = []
names = []


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


# sending the message to the all clients that are currently connected to the server
def broadcast(message):
    for client in clients:
        client.send(message)
    print(message.decode(FORMAT))


# sending private message
def private_broadcast(message, list):
    for client in list:
        client.send(message)
    print(message.decode(FORMAT))


# disconnect the client and removing their name from the list
def leave(client):
    client.close()
    index = clients.index(client)
    clients.remove(client)
    name = names[index]
    names.remove(name)
    message = f"{name} left the chat.\n{names}\n".encode(FORMAT)
    broadcast(message)



# handling client states
def handle_client(client):
    connected = True
    while connected:

        try:

            message = client.recv(1024)
            msg = message.decode(FORMAT)

            if msg.startswith("["):
                msg = msg.split("\n")
                private_list = ast.literal_eval(msg[0])
                private_list = [key for key, value in DICT_CLIENT.items() if value in private_list]
                private_broadcast(f"private message from {msg[1]}".encode(FORMAT), private_list)

            else:
                broadcast(message)
                if msg.split(": ")[1] == "bye":
                    leave(client)
                    break

        except:
            leave(client)
            break




def start():
    print(f"[LISTENING] server is listening on {HOST}")
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

        # sending "Hi" to the client
        client.send(f"Hi {name}, welcome to the chat room.\n".encode(FORMAT))

        # broadcasting the list of clients & joined message
        message = f"{name} joined the chat room.\n {names}\n".encode(FORMAT)
        broadcast(message)

        # running a thread for every client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


print("[STARTING] server is starting ...")
time.sleep(0.6)
start()
