#!/usr/bin/env

# socket_client.py

import socket # 导入socker模块

#创建socket对象

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("socket created")

'''
socket.socket 模块.方法  该函数创建一个socket
该函数需要两个参数 
1、address family
	AF_INET Internet之间的通信
	AF_UNIX 同一个机器之间的通信
2、type
	SOCK_STREAM 用于tcp
	SOCKET_DGRAM 用户udp

'''

# 提供远程服务器域名和端口
host = 'www.baidu.com'
port = 80

# socket.gethostbyname 根据域名获取远程主机ip地址的函数
remote_ip = socket.gethostbyname(host)

# 连接远程服务器 connect函数
# 对象.函数
s.connect((remote_ip,port))
print("socket connect to HOST %s port %d" %(remote_ip,port))

#定义发送的http  (http请求报文)
message="GET /index.html HTTP/1.0\r\n\r\n"

# str to bytes
bytes_message=bytes(message,encoding = "utf8")

#发送消息
s.send(bytes_message)

#接收响应信息
replay=s.recv(4096)
print(replay)
