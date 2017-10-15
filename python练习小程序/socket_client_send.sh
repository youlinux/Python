#!/usr/bin/env python

import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("socket created.....")

host="127.0.0.1"
port=8888

s.connect((host,port))

s.send(b"Hello World")

s.close()