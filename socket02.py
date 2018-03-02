#!/usr/bin/env python

import socket
import sys

tcpip = '10.11.1.39'
tcpport = 22
buffersize = 1024
message = "hello"

try:
    tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsocket.connect((tcpip, tcpport))
    tcpsocket.send(message)
    print "message sent successfully"
    data = tcpsocket.recv(buffersize)
    tcpsocket.close()
    print "response: ", data
    # tcpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # tcpsocket.settimeout(3)
    # tcpsocket.bind((tcpip, tcpport))
    # listen for incoming connections
    # tcpsocket.listen(5)
except socket.error, (value, message):
    print "Error ocurred while creating the socket. Error Code: " + str(value) + ", Error Message: " + message
    sys.exit(1)

# connection, address = tcpsocket.accept()
# data = connection.recv(buffersize)
# print "message from client:", data

