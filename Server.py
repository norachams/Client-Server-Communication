import socket
import threading
import datetime
import os
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
FILE_DIRECTORY = "server_files" 

#Global Cache for connected clients
clients = {}
client_counter = 1 #assgin unique client names


# Ensure the folder exists and create folder if it doesn’t exist
if not os.path.exists(FILE_DIRECTORY):
    os.makedirs(FILE_DIRECTORY)  


'''Returns a list of files available in the server repository'''
def list_files():
    """Returns a list of files in the server directory."""
    try:
        print(f"Checking files in: {FILE_DIRECTORY}")  # Debugging step
        files = os.listdir(FILE_DIRECTORY)
        print(f"Files found: {files}")  # Debugging step
        return "\n".join(files) if files else "No files available."
    except Exception as e:
        return f"Error accessing directory: {e}"


def send_file(cleint_socket, filename):
    file_path = os.path.join(FILE_DIRECTORY, filename)
    if os.path.exist(file_path):
        try:
            with open(file, "rb") as file:
                client_socket.sendall(file.read())
            print(f"File '{filename}' sent successfully.")
        except Exception as e:
            client_socket.send(f"Error sending file: {e}".encode())
    else:
        client_socket.send("File not found".endcode())

''' Handles communication with a client'''
def handle_client(client_socket, client_name):
    global clients
    clients[client_name] = {"connected_at": datetime.datetime.now(), "socket":client_socket}

    try:
        while True:
            #recieve message
            data = client_socket.recv(1024).decode()
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
            elif data.lower() == "list":
                client_socket.send(list_files().encode())
            elif data.startswith("get"):
                filename = data.split(" ", 1)[1]
                send_file(client_socket, filename)
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
    server_socket.listen(MAX_CLIENTS)
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