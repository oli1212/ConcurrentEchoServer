from socket import socket, AF_INET, SOCK_STREAM

data_payload = 2048

def start_client(host, port):
    # create client TCP socket
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((host,port))

        while True:
            message = input("Enter message to send (type 'quit' to end connection): ")
            # encode message
            client_socket.sendall(message.encode('utf-8'))
            print(f"Client sent: {message}")

            # if message from client is "quit", close client connection from server
            if message.lower() == "quit":
                client_socket.close()
                break
            
            response = client_socket.recv(data_payload).decode()
            print(f"Server: {response}")
    except ConnectionError:
        client_socket.close()
        print("Connection to server failed, please make sure server is on.")

if __name__ == '__main__':
    start_client('localhost', 65432)