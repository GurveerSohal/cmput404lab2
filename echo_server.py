#!/usr/bin/env python3
import socket
import time
from threading import Thread
import os

# Entity: GeeksForGeeks
# URL: https://www.geeksforgeeks.org/python-os-fork-method/

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def handleConnection(conn):
        #recieve data, wait a bit, then send it back
        full_data = conn.recv(BUFFER_SIZE)
        print(full_data)
        time.sleep(0.5)
        conn.sendall(full_data)
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            pid = os.fork()

            if pid == 0:
                handleConnection(conn)
                os._exit(0)

            conn.close()

if __name__ == "__main__":
    main()
