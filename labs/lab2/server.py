from socket import *
import threading

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')


def handle_client(connectionSocket):
    while True:
        sentence = connectionSocket.recv(1024).decode()
        capitalizedSentence = sentence.upper()
        connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()


while True:
    connectionSocket, addr = serverSocket.accept()
    print('Connected by', addr)
    client_thread = threading.Thread(
        target=handle_client, args=(connectionSocket,))
    client_thread.start()
