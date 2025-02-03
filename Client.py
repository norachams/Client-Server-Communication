from socket import *
import socket

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


'''Connect to the server and send messages'''
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))  # Connect to the server
    print(f"Connected to server at {HOST}:{PORT}")

    try:
        while True:
            message = input("Enter message ('status' for clients, 'exit' to disconnect): ")
            #send message to server
            client_socket.send(message.encode())

            #recieve response
            data = client_socket.recv(1024).decode()
            print(f"Received from server:")
            print(f"{data}")

            if message.lower() == "exit":
                print("Disconnecting...")
                break

    except Exception as e:
        print(f"Error: {e}")

    client_socket.close()

if __name__ == '__main__':
    start_client()



