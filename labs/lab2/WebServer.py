from socket import *
import threading

def handle_client(connectionSocket):
    try:
        # Receive the HTTP request message
        message = connectionSocket.recv(1024).decode()

        # Extract the filename from the request
        filename = message.split()[1][1:]
        print('Filename:', filename)

        # Open the requested file
        with open(filename, "rb") as f:
            outputdata = f.read()

        # Send HTTP response headers
        response_headers = "HTTP/1.1 200 OK\r\n\r\n"
        connectionSocket.send(response_headers.encode())

        # Send the content of the requested file to the client
        connectionSocket.sendall(outputdata)

    except IOError:
        # Send response message for file not found (404 Not Found)
        not_found_response = "HTTP/1.1 404 Not Found\r\n\r\nFile not found"
        connectionSocket.send(not_found_response.encode())

    # Close the client socket
    connectionSocket.close()



serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a server socket
serverPort = 6789
serverSocket.bind(('0.0.0.0', serverPort))
serverSocket.listen(5)
print('The server is ready to receive')

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    print('Connected by', addr)

    # Create a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(connectionSocket,))
    client_thread.start()
