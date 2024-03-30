from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread

backlog = 5
data_payload = 2048

def handle_client(client: socket, address):
    while True:
        data = client.recv(data_payload)

        if not data:
            client.close()
            print(f"Connection with {address} closed")
            break
        else:
            client_response = data.decode('utf-8')
            print(f"Message from {address}: {client_response}")
            client.send(client_response.encode())
    

def start_server(host, port):
    try:
        # create TCP socket
        server = socket(AF_INET, SOCK_STREAM) 
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        # bind socket to address
        server.bind((host,port))

        # Listening to clients, backlog value is the max number of queued connections
        server.listen(backlog)
        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, client_address = server.accept()
            print(f"Accepted connection from {client_address}")

            client_thread = Thread(target = handle_client, args = (client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        server.close()
        print("Closed server")


if __name__ == '__main__':
    start_server('localhost', 65432)
