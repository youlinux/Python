#!/usr/bin/env python


# 在服务器端，socket() 返回的套接字用于监听（listen）和接受（accept）客户端的连接请求。这个套接字不能用于与客户端之间发送和接收数据。

#accept()
#接受一个客户端的连接请求，并返回一个新的套接字。所谓“新的”就是说这个套接字与socket()
#返回的用于监听和接受客户端的连接请求的套接字不是同一个套接字。与本次接受的客户端的通信是通过在这个新的套接字上发送和接收数据来完成的。

#再次调用accept()
#可以接受下一个客户端的连接请求，并再次返回一个新的套接字（与socket()
#返回的套接字、之前accept()
#返回的套接字都不同的新的套接字）。这个新的套接字用于与这次接受的客户端之间的通信。

#假设一共有3个客户端连接到服务器端。那么在服务器端就一共有4个套接字：第1个是socket()
#返回的、用于监听的套接字；其余3个是分别调用3次accept() 返回的不同的套接字。

# 如果已经有客户端连接到服务器端，不再需要监听和接受更多的客户端连接的时候，可以关闭由socket()
# 返回的套接字，而不会影响与客户端之间的通信。

# 当某个客户端断开连接、或者是与某个客户端的通信完成之后，服务器端需要关闭用于与该客户端通信的套接字。

import socket
import sys

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("socket created ok")

host=""
port=8888

s.bind((host,port))
s.listen(10)


conn,addr=s.accept()

data=conn.recv(1024)
conn.sendall(data)
print(data)

conn.close()
s.close()