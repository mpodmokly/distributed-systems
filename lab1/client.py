import socket
import threading


stop = False

def handle_message(client: socket.socket):
    try:
        while True:
            server_msg = client.recv(1024).decode()

            if stop:
                break
            print(server_msg)
    except (ConnectionAbortedError, OSError, ConnectionResetError):
        pass


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

thread = threading.Thread(target=handle_message, args=(client,))
thread.start()

print("Type message:")
try:
    while True:
        msg = input()
        client.send(msg.encode())

        if msg == "EXIT":
            print("Client closed")
            break
except KeyboardInterrupt:
    print("Client closed")
finally:
    stop = True
    client.close()
