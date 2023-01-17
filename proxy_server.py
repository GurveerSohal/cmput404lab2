#!/usr/bin/env python3
import socket
import time
import os
import sys

# Entity: GeeksForGeeks
# URL: https://www.geeksforgeeks.org/python-os-fork-method/

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload)
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def handleConnection(conn, request):
    sys.stdout.write("forked child")
    try:
        #define address info, payload, and buffer size
        host = 'www.google.com'
        port = 80
        payload = request

        remote_ip = get_remote_ip(host)

        tempClient = create_tcp_socket()
        tempClient.connect((remote_ip , port))
        print (f'Socket Connected to {host} on ip {remote_ip}')
        
        #send the data and shutdown
        send_data(tempClient, payload)

        #continue accepting data until no more left
        full_data = b""
        while True:
            data = tempClient.recv(BUFFER_SIZE)
            if not data:
                 break
            full_data += data


        time.sleep(0.5)
        conn.sendall(full_data)
        conn.close()

    except Exception as e:
        full_data = b"error getting data from google\n"
        time.sleep(0.5)
        conn.sendall(full_data)
        conn.close()
        print(e)
    
    os._exit(0)


def main():
    with create_tcp_socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            #recieve data, wait a bit, then send it back
            request = conn.recv(BUFFER_SIZE)

            pid = os.fork()

            if pid == 0:
                handleConnection(conn, request) 

            conn.close()


if __name__ == "__main__":
    main()
