'''
  ETTTP_Client_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Jun 03, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg
    


if __name__ == '__main__':

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)  
        
        ###################################################################
        ######################### Fill Out ################################
        # Send ACK
        # data = client_socket.send()

        # TODO : 메시지 받을 때 ME, YOU 로 받아 ACK 보내기
        recv = client_socket.recv(SIZE).decode()

        if check_msg(recv, MY_IP):
            recv_msg = recv.split("\r\n")[2]
            if recv_msg.endswith("ME"):
                start = 0
                ack = "ACK ETTTP/1.0\r\nHost:" + str(SERVER_IP) + "\r\nFirst-Move: YOU\r\n\r\n"
                client_socket.send(ack.encode())
            else:
                start = 1
                ack = "ACK ETTTP/1.0\r\nHost:" + str(SERVER_IP) + "\r\nFirst-Move: ME\r\n\r\n"
                client_socket.send(ack.encode())

        ###################################################################

        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        