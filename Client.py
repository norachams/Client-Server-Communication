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
            client_socket.send(message.encode())

            if message.lower() == "exit":
                print("Disconnecting...")
                break

            # Check the type of command before receiving any data
            if message.lower() == "list":
                response = client_socket.recv(1024).decode()
                print(f"Available files:\n{response}")

            elif message.startswith("get "):
                filename = message.split(" ", 1)[1]
                print(f"Downloading '{filename}'...")

                file_path = os.path.join(DOWNLOAD_DIRECTORY, filename)
                os.makedirs(DOWNLOAD_DIRECTORY, exist_ok=True)
                
                # Start by receiving the first chunk.
                data = client_socket.recv(1024)
                
                # Check if the file wasn't found.
                if data.decode(errors="ignore") == "File not found":
                    print(f"Error: '{filename}' does not exist on the server.")
                else:
                    with open(file_path, "wb") as file:
                        # Check if this first chunk already contains the marker.
                        if data.endswith(b"FILE_TRANSFER_COMPLETE"):
                            file.write(data[:-len(b"FILE_TRANSFER_COMPLETE")])
                        else:
                            file.write(data)
                            while True:
                                data = client_socket.recv(1024)
                                # Look for the marker at the end of this chunk.
                                if data.endswith(b"FILE_TRANSFER_COMPLETE"):
                                    file.write(data[:-len(b"FILE_TRANSFER_COMPLETE")])
                                    break
                                file.write(data)
                    print(f"File '{filename}' downloaded successfully to '{DOWNLOAD_DIRECTORY}/'")


            else:
                # For any other commands, just receive and print the response.
                response = client_socket.recv(1024).decode()
                print(f"Server: {response}")
    

    except Exception as e:
        print(f"Error: {e}")

    client_socket.close()

if __name__ == '__main__':
    start_client()



