import socket
import threading


clients = [] # [name, conn]
stop = False

def handle_client(conn: socket.socket):
    while True:
        client_name = conn.recv(1024).decode()

        if client_name in clients:
            print(f"Client {client_name} already exists")
            conn.send("ERROR".encode())
        else:
            print(f"Client {client_name} accepted")
            conn.send("ACCEPT".encode())
            clients.append([client_name, conn])
            break
    
    while True:
        msg = conn.recv(1024).decode()

        if stop:
            break

        if msg == "STOP":
            for i in range(len(clients)):
                if clients[i][0] == client_name:
                    clients.pop(i)
            
            print(f"{client_name}: disconnected")
            break
        else:
            for cli in clients:
                if cli[0] != client_name:
                    cli[1].send(f"{client_name}: {msg}".encode())


PORT = 9000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", PORT))
server.listen()
print("Server running")

try:
    while True:
        conn, addr = server.accept()
        print(f"Connected with: {addr}")
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()
        thread.join()
except KeyboardInterrupt:
    print("Server closed")
finally:
    stop = True
    conn.close()
    server.close()
