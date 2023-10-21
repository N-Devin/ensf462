from socket import *

# Define the server address and port
serverName = 'localhost'
serverPort = 12000

# Create a socket object
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to the server
clientSocket.connect((serverName, serverPort))

# Get the user's name
user_name = input('Enter your name: ')
clientSocket.send(user_name.encode())

# Receive the server's name
server_name = clientSocket.recv(1024).decode()
print(f'Connected to {server_name}')

while True:
    # Client's turn
    print(f'{user_name}, your turn:')
    message = input()

    # Send the client's message to the server
    clientSocket.send(message.encode())

    if message.lower() == 'bye':
        print('Disconnected from the server.')
        break

    # Server's turn
    print(f'Waiting for response...')
    server_message = clientSocket.recv(1024).decode()

    if server_message.lower() == 'bye':
        print('Disconnected from the server.')
        break

    print(server_message)

    # Check if the server wants to disconnect
    if server_message.lower() == 'bye':
        print('Client disconnected.')
        break

# Close the connection
clientSocket.close()
