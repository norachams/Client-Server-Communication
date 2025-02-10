from socket import *
import socket
import os

'''
The client will:
- Connect to the server
- Send its name upon connecting
- Allow users to type messages from a command line
- Recieve responses from the server
- Support the 'status' and 'exit' commands
'''
HOST = "127.0.0.1"
PORT = 12345

DOWNLOAD_DIRECTORY = "downloaded_files"


'''Connect to the server and send messages'''
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))  # Connect to the server
    print(f"Connected to server at {HOST}:{PORT}")

    try:
        while True:
            message = input("Enter message ('status', 'list', 'get <file>', 'exit'): ")
            #send message to server
            client_socket.send(message.encode())

            if message.lower() == "exit":
                print("Disconnecting...")
                break

            #recieve response
            response = client_socket.recv(1024).decode()
            if message.lower() == "list":
                print(f"Available files:\n{response}")

            
            elif message.startswith("get "):
                filename = message.split(" ", 1)[1]
                file_path =  os.path.join(DOWNLOAD_DIRECTORY, filename)
                
                #recieve the file data
                with open(file_path, "wb") as file:
                    data = client_socket.recv(4096)  # Receive file data
                    file.write(data)
                print(f"File '{filename}' downloaded successfully to '{DOWNLOAD_DIRECTORY}/")

            else:
                print(f"Server: {response}")            

    except Exception as e:
        print(f"Error: {e}")

    client_socket.close()

if __name__ == '__main__':
    start_client()



