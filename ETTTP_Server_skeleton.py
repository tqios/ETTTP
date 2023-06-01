'''
  ETTTP_Sever_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg

    
if __name__ == '__main__':
    
    global send_header, recv_header
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'
    
    while True:
        client_socket, client_addr = server_socket.accept()
        
        # start = str(random.randrange(0,2)).encode()   # select random to start

        ###################################################################
        # Send start move information to peer
        # client_socket.send(start)


        start = random.randrange(0,2)
        print("start : ", start)
        if start == 0:
            send_msg = "SEND ETTTP/1.0\r\nHost:127.0.0.1\r\nFirst-Move: server\r\n\r\n"
            client_socket.send(send_msg.encode()) #msg보내고
            msg = client_socket.recv(SIZE).decode() #ack받고
            # print('에크메시지',msg)
            if check_msg(msg): #ack가 ETTTP인지 확인
                ack_msg = msg.split("\r\n")[2]
                # print("ack_msg : ", ack_msg)


        else:
            send_msg = "SEND ETTTP/1.0\r\nHost:127.0.0.1\r\nFirst-Move: client\r\n\r\n"
            client_socket.send(send_msg.encode())
            msg = client_socket.recv(SIZE).decode()
            print(msg)
            if check_msg(msg):
                ack_msg = msg.split("\r\n")[2]
                # print("ack_msg : ", ack_msg)

        ######################### Fill Out ################################
        # Receive ack - if ack is correct, start game
        # data = client_socket.recv(SIZE).decode()
        # print(data)

        ###################################################################

        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        print()
        root.play(start_user=start)
        root.mainloop()
        
        client_socket.close()
        
        break
    server_socket.close()