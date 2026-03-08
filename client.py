import socket
import threading


def handle_message():
    server_msg = ""

PORT = 9000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", PORT))

while True:
    name = input("Type client name: ")
    client.send(name.encode())
    response = client.recv(1024)

    if response.decode() == "ERROR":
        print(f"Server: {name} already exists, type other")
    elif response.decode() == "ACCEPT":
        print("Connection accepted")
        break
    else:
        print("Unknown error occurred")
        break

# handle message

print("Type message:\n")
try:
    while True:
        msg = input()
        client.send(msg.encode())

        if msg == "STOP":
            print("Client closed")
            break
except KeyboardInterrupt:
    print("Client closed")
finally:
    client.close()
