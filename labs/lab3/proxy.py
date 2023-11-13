from socket import *
import sys

if len(sys.argv) <= 1:
    print(
        'Usage : "python ProxyServer.py server_ip"\n[server_ip: IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('10.9.132.111', 8888))
tcpSerSock.listen(5)

# requested_files is a dictionary that stores the file name as the key and 'True' as the value
requested_files = {}

while True:
    # begin receiving data from the client
    print('Ready to serve...')
    tcpCliSock, address = tcpSerSock.accept()
    print('Received a connection from:', address)

    # Receive the message from the client
    message = tcpCliSock.recv(1024).decode()
    print(message)

    # Extract the filename from the given message
    filename = message.split()[1].partition("/")[2]
    print(filename)
    file_in_use = "/" + filename

    if file_in_use not in requested_files:
        # Check whether the file exist in the cache
        try:
            # Create a socket on the proxy server to connect to the web server
            connection = socket(AF_INET, SOCK_STREAM)
            hostname = filename.replace("www.", "", 1)
            print(hostname)

            # Connect to the socket to port 80
            connection.connect((hostname, 80))
            # Create a temporary file on this socket and ask port 80
            fileobj = connection.makefile('r', 0)
            fileobj.write(f"GET /{filename} HTTP/1.0\n\n")

            # Read the response into a buffer
            buffer = fileobj.readlines()

            # Create a new file in the cache for the requested file
            temp_File = open(file_in_use, "wb")
            for data in buffer:
                temp_File.write(data.encode())
                tcpCliSock.send(data.encode())

            # Mark the file as requested
            requested_files[file_in_use] = True

        except Exception as e:
            print("Error: ", e)

    # Proxy server finds a cache hit and generates a response message
    try:
        f = open(file_in_use[1:], "r")
        outputdata = f.readlines()

        # Send one HTTP header line into socket
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        tcpCliSock.send("Content-Type: text/html\r\n")
        for i in range(len(outputdata)):
            tcpCliSock.send(outputdata[i].encode())
        print('Read from cache')

    except IOError:
        pass

    # Close the client and the server sockets
    tcpCliSock.close()
