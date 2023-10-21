from socket import *

# Define the server port
serverPort = 12000

# Create a socket object and bind it to the server port
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('0.0.0.0', serverPort))  # Bind to all available interfaces
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    # Accept incoming connections
    connectionSocket, addr = serverSocket.accept()
    print(f'Connected to {addr}')

    # Prompt the server operator for a name
    server_name = input('Enter your name: ')
    print('Waiting for a client...')

    client_name = connectionSocket.recv(1024).decode()
    print(f'Connected to {client_name}')

    while True:
        # Server's turn
        print(f'{server_name}, your turn:')
        response = input()

        # Send the server's message to the client
        connectionSocket.send(f'{server_name}: {response}'.encode())

        if response.lower() == 'bye':
            print('Client disconnected.')
            connectionSocket.close()
            break

        # Client's turn
        print(f'Waiting for response...')
        client_message = connectionSocket.recv(1024).decode()

        if client_message.lower() == 'bye':
            print('Client disconnected.')
            break

        print(f'{client_name}: {client_message}')

        # Check if the client wants to disconnect
        if client_message.lower() == 'bye':
            print('Server disconnected.')
            break

    # Close the connection
    connectionSocket.close()
