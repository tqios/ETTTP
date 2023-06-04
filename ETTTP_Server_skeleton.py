'''
  ETTTP_Sever_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol

  2171085 김지윤
  2171087 이희원

  Jun 04, 2023
 
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

        ###################################################################
        # Send start move information to peer
        ######################### Fill Out ################################
        # Receive ack - if ack is correct, start game

        # 시작할 사람을 정해 메시지 전송
        # ack로 상대방이 메시지를 잘 받았는지 확인 후 게임 진행
        start = random.randrange(0,2)
        if start == 0:
            send_msg = "SEND ETTTP/1.0\r\nHost:"+str(client_addr[0])+"\r\nFirst-Move: ME\r\n\r\n"
            client_socket.send(send_msg.encode()) #msg보내고
            ack = client_socket.recv(SIZE).decode() #ack받고
            if not (check_msg(ack, MY_IP) and ack.endswith("YOU\r\n\r\n")): #ack가 ETTTP이고 ack_msg가 YOU인지 확인
                quit()

        else:
            send_msg = "SEND ETTTP/1.0\r\nHost:"+str(client_addr[0])+"\r\nFirst-Move: YOU\r\n\r\n"
            client_socket.send(send_msg.encode())
            ack = client_socket.recv(SIZE).decode()
            if not (check_msg(ack, MY_IP) and ack.endswith("ME\r\n\r\n")): #ack가 ETTTP이고 ack_msg가 ME인지 확인
                quit();

        ###################################################################

        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
        
        client_socket.close()
        
        break
    server_socket.close()