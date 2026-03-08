import socket


clients = []

def handle_client(conn: socket.socket):
    while True:
        client_name = conn.recv(1024).decode()

        if client_name in clients:
            print(f"Client {client_name} already exists")
            conn.send("ERROR".encode())
        else:
            print(f"Client {client_name} accepted")
            conn.send("ACCEPT".encode())
            clients.append(client_name)
            # start client thread
            break


PORT = 9000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", PORT))
server.listen()
print("Server running")

while True:
    conn, addr = server.accept()
    print(f"Connected with: {addr}")
    handle_client(conn)
    
    break

conn.close()
server.close()
