from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread

backlog = 5
data_payload = 2048

# handle each client thread
def handle_client(client: socket, address): 
    while True:
        # gets input from client
        data = client.recv(data_payload) 

        # if there is no message from the client close connection
        if not data: 
            client.close()
            print(f"Connection with {address} closed")
            break
        # if there is a message from the client print client address and message
        else:
            client_response = data.decode('utf-8')
            print(f"Message from {address}: {client_response}")
            client.send(client_response.encode())
    

def start_server(host, port):
    try:
        # create server TCP socket
        server = socket(AF_INET, SOCK_STREAM) 
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        # bind socket to address
        server.bind((host,port))

        # Listening to clients, backlog value is the max number of queued connections
        server.listen(backlog)
        print(f"Server listening on {host}:{port}")

        # loop until server closes
        while True:
            # accept client connections
            client_socket, client_address = server.accept()
            print(f"Accepted connection from {client_address}")
            # create a thread to hold multiple clients
            client_thread = Thread(target = handle_client, args = (client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        server.close()
        print("Closed server")


if __name__ == '__main__':
    start_server('localhost', 65432)
