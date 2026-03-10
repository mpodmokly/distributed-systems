import socket
import threading


clients = [] # [name, conn]
stop = False

def handle_client(conn: socket.socket):
    while True:
        client_name = conn.recv(1024).decode()
        flag = True

        for cli in clients:
            if cli[0] == client_name:
                print(f"Client {client_name} already exists")
                conn.send("ERROR".encode())
                flag = False
        
        if flag:
            print(f"Client {client_name} accepted")
            conn.send("ACCEPT".encode())
            clients.append([client_name, conn])
            break
    
    try:
        while True:
            msg = conn.recv(1024).decode()

            if stop:
                break

            if msg == "EXIT":
                for i in range(len(clients)):
                    if clients[i][0] == client_name:
                        clients.pop(i)
                        break
                
                conn.close()
                break
            else:
                msg_text = f"{client_name}: {msg}"
                print(msg_text)

                for cli in clients:
                    if cli[0] != client_name:
                        cli[1].send(msg_text.encode())
    except ConnectionResetError:
        pass
    finally:
        print(f"{client_name}: disconnected")


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
except KeyboardInterrupt:
    print("Server closed")
finally:
    stop = True
    for cli in clients:
        cli[1].close()
    server.close()
