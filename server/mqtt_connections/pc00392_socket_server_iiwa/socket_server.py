#!/usr/bin/env python

__author__ = 'Jan Kempeneers'

import socket, sys, queue, threading

msg_in_str = ""

def main():
    run()

def run():
    global msg_in_str
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 30432  # Arbitrary non-privileged port
    q = queue.Queue()
    thread_sock_server = threading.Thread(target=create_socket_connection, args=(HOST, PORT, q))
    thread_sock_server.start()

    while True:
        conn = q.get()
        print(conn)
        print("attaching to new connection")
        while q.empty():
            msg_in = conn.recv(1024)
            msg_in_str = msg_in.decode()
            if msg_in_str != '':
                print(msg_in_str)
                answer_in_bytes = ("Message arrived: {}".format(msg_in_str)).encode('utf-8')
                conn.sendall(answer_in_bytes)
        conn.close()


def create_socket_connection(host, port, q):
    # open a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
    # bind socket to host and port, also catch exception.
    try:
        s.bind((host, port))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    print('Socket bind complete')
    # start listening to the socket

    while True:
        s.listen(10)
        print('Socket now listening')
        # server keeps listening, program continues only when connection is made
        conn, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))

        # return conn
        q.put(conn)

    # close the connection and socket after talking to the client
    s.close()


if __name__ == "__main__":
    main()
