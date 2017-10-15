#!/usr/bin/env python

import socket

def handle_request(client):
    buf = client.recv(1024)
    client.send(b"<h1>hello world</h1>")

def main():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host=''
    port=8888
    sock.bind((host,port))
    sock.listen(5)

    while True:
        conn,addr=sock.accept()
        handle_request(conn)
        conn.close()
if __name__ == '__main__':
    main()
