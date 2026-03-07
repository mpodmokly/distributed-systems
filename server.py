import socket


PORT = 9000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", PORT))
server.listen()
print("Server running")

conn, addr = server.accept()
print(f"Connected with: {addr}")

while True:
    data = conn.recv(1024)
    msg = data.decode()
    print(f"Client: {msg}")

    response = "odp"
    conn.send(response.encode())
    break

conn.close()
server.close()
