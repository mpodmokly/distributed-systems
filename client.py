import socket


PORT = 9000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", PORT))

while True:
    msg = input("Message: ")
    client.send(msg.encode())

    data = client.recv(1024)
    print(f"Server: {data.decode()}")
