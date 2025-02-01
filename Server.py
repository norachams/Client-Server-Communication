import socket
import threading
import datetime
'''
The server will:
- Accept up to 3 clients
- Assign names dynamically
- Maintain a cache (list of active clients)
- Echo messages back using CLI 
- Respond to "Status" requests
- Handle "Exit" client diconnections gracefully
'''

#server configurations
HOST = "127.0.0.1"
PORT = 12345
MAX_CLIENTS = 3

#Global Cache for connected clients
clients = {}
client_counter = 1 #assgin unique client names

''' Handles communication with a client'''
def handle_cleint(client_socket, client_name):
    global clients
    clients[client_name] = {"connected_at": datetime.datetime.now(), "socket":client_socket}

    try:
        while true:
            #recieve message
            data = client_socket.reccv(1024).decode()
            if not data:
                break

            print(f"[{client_name}] Sent: {data}")

            #handle special command like "status" and "exit"
            if data.lower() == "status":
                status_response = "\n".join(
                    [f"{name}: Connected at {info['connected_at']}" for name, info in clients.items()]
                )
                client_socket.send(status_response.encode())
            elif data.lower() == "exit":
                print(f"[{client_name}] Disconnected")
                break #exit and close connection
            #if we didnt get either of the special command then we will make the server echo message
            else:
                response = f"{data} ACK"
                client_socket.send(response.encode())

    except Exception as e:
        print(f"Error handling {client_name}: {e}")

    # Remove client from cache
    del clients[client_name]
    client_socket.close()


'''start the server to handle multiple clients'''
def start_server():
    global client_counter

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))  # Bind to localhost on port 12345
    server_socket.listen(MAX_ClIENTS)
    print(f"Server started on {HOST}:{PORT}, listening for clients...")

    while True:
        if len(clients) < MAX_CLIENTS:
            client_socket, addr = server_socket.accept()
            client_name = f"Client{client_counter:02d}"  # Assign Client01, Client02...
            client_counter += 1
            print(f"[NEW CONNECTION] {client_name} connected from {addr}")

            # Start a new thread for the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_name))
            client_thread.start()


if __name__ == '__main__':
    start_server()