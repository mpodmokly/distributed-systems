import socket


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

client.close()
