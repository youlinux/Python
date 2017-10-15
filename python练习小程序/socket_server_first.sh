#!/usr/bin/env

import socket #导入socket模块

import sys # 导入sys模块,可以执行系统命令

HOST = '' # 本机的所有IP
PORT = 8888 #本机的8888端口

# 创建socket对象
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("socket created")

# 绑定
s.bind((HOST,PORT))

#监听连接
# 最多10个连接,之后的连接将会被拒绝
s.listen(10)


# 接收连接
conn,addr=s.accept()

print(conn) # socket对象
print(addr[0]) # 来源ip
print(addr[1]) # 来源端口



#可以使用telnet 命令测试