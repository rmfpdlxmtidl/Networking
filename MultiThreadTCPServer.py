# 20171758 Gwak Taeuk
# BasicTCPServer.py

from socket import *
from time import *
from threading import Thread
import json


# If N client connects, there will be N client threads, N client sockets, along with 1 serer socket in the main thread
# In this way, threading will automatically take care of multiple clients
def connectionThread(connectionSocket):
    # send and receive data through the connection socket
    while True:
        # server will receive the command and reply with an appropriate response based on the command
        request = connectionSocket.recv(1024).decode()
        # when the connection disconnects for the TCP case, or when client disconnects
        if(request == ''):
            break
        # extract command number from client request
        requestJson = json.loads(request)
        command = requestJson['command']

        # convert text to UPPER-case letters
        if(command == '1'):
            print('Command', command)
            response = requestJson['message'].upper()
            connectionSocket.send(response.encode())
        # tell the client what the IP address and port number of the client is
        elif(command == '2'):
            print('Command', command)
            address = {
                "IP": clientAddress[0],
                "Port": clientAddress[1]
            }
            response = json.dumps(address)
            connectionSocket.send(response.encode())
        # tell the client what the current time on the server is
        elif(command == '3'):
            print('Command', command)
            connectionSocket.send(strftime(
                '%H-%M-%S', localtime(time())).encode())  # TCP
        # tell the client how long it (server program) has been running for
        elif(command == '4'):
            print('Command', command)
            connectionSocket.send(strftime(
                '%H-%M-%S', gmtime(time() - start)).encode())  # TCP
        # test time out
        elif(command == '6'):
            print('Command', command)
            sleep(15)
        # test buffer overflow
        elif(command == '7'):
            print('Command', command)
            response = requestJson['message']
            connectionSocket.send(response.encode())
        else:
            print('Unknown Response, Command', command)
            continue

    connectionSocket.close()


# measure the server starting time
start = time()

# create TCP socket that following IPv4 on the port #10825
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 21758
serverSocket.bind(('', serverPort))
connectionSocket = None

# print the port number of the socket
print("The server socket was created on port", serverSocket.getsockname()[1])

# try to listen, accept, send, and receive
try:
    # Server has a main thread with a server socket that is waiting for client connections
    while True:
        # listen to port #10825
        serverSocket.listen(1)
        print("The server socket is listening to port", serverSocket.getsockname()[1])

        # When a client connects to the server and server 'accept()'s, server has a new socket for that client,
        (connectionSocket, clientAddress) = serverSocket.accept()
        print('Connection requested from', clientAddress)

        # and server creates a new thread for that connection. connection socket is given to the client thread
        t = Thread(target=connectionThread, args=(connectionSocket,))
        # Then, this client thread in the server will use the client socket to communicate with the client
        t.start()        

# when the user enters ‘Ctrl-C’, the program should not show any error messages
except KeyboardInterrupt:
    if(connectionSocket != None):
        connectionSocket.close()
    print('\nBye bye~')
# client shutdown without notice?
except ConnectionResetError:
    if(connectionSocket != None):
        connectionSocket.close()
    print('ConnectionResetError: Connection is reset by remote host')

serverSocket.close()
