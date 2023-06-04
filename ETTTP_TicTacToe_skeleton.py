'''
  ETTTP_TicTacToe_skeleton.py
 
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

SIZE=1024

class TTT(tk.Tk):
    # 생성자
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr
        self.recv_ip = src_addr
        
        self.total_cells = 9
        self.line_size = 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client:
            self.myID = 1   #0: server, 1: client
            self.title('34743-02-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"ME"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"YOU"}   
        else:
            self.myID = 0
            self.title('34743-02-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}   
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################

            
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    # create TicTacToe frame
    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # create TicTacToe frame
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    # create TicTacToe frame : 결과관련
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    # create TicTacToe frame
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    # create TicTacToe frame
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # 게임 시작 함수
    def play(self, start_user):
        '''
        Call this function to initiate the game

        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active



        if start_user == self.myID:
            self.my_turn = 1
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())



        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # 게임 종료 함수
    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    # 차례인 사용자가 버튼 클릭 시, 유효하면 board update + 차례바꾸기
    def my_move(self, e, user_move):
        '''
        Read button when the player clicks the button

        e: event
        user_move: button number, from 0 to 8
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv

        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer
        valid = self.send_move(user_move)

        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()

        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)

        # If the game is not over, change turn
        if self.state == self.active:
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # 문자열을 딕셔너리로 만듦
    def create_dictionary(self, msg):
        data = msg.split("\r\n")
        dic = {}
        if not msg :
            self.quit()

        for item in data:
            if ':' in item:
                key, value = item.split(':', 1)  # ':'을 기준으로 키와 값으로 분리
                dic[key.strip()] = value.strip()  # 공백을 제거하고 딕셔너리에 추가
        return dic

    # 받은 메시지의 유효성을 체크하고 유효한 경우, 메시지에서 좌표를 가져와 ack보낸 후 보드 업데이트
    # 유효하지 않은 경우 프로그램 종료
    def get_move(self):
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################
        msg = self.socket.recv(SIZE).decode()
        dic = self.create_dictionary(msg)


        msg_valid_check = check_msg(msg, self.recv_ip)

        if not msg_valid_check: # Message is not valid
            self.socket.close()
            self.quit()

        else:  # If message is valid - send ack, update board and change turn
            row = int(dic['New-Move'][1])
            col = int(dic['New-Move'][3])
            loc = row * 3 + col
            ack_msg = "ACK ETTTP/1.0\r\nHost:" + str(self.send_ip) + "\r\nNew-Move:(" + str(row) + "," + str(col) + ")\r\n\r\n"
            self.socket.send(ack_msg.encode());


            #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            self.update_board(self.computer, loc, get=True)
            if self.state == self.active:
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status ['text'] = ['Ready']
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    # textbox에 입력된 메시지를 분석해 ETTTP인지 확인 -> 이미 체크 된 자리이면 프로그램 종료
    # 신규 자리인 경우, 소켓에 메시지 전송 + ack받아 유효한 지 확인 후 보드 업데이트
    def send_debug(self):
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''

        if not self.my_turn:
            self.t_debug.delete(1.0,"end")
            return
        # get message from the input box
        d_msg = self.t_debug.get(1.0,"end")
        d_msg = d_msg.replace("\\r\\n","\r\n")   # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0,"end")

        ###################  Fill Out  #######################
        '''
        Check if the selected location is already taken or not
        '''
        if check_msg(d_msg, self.recv_ip):
            dic = self.create_dictionary(d_msg)
            row = int(dic['New-Move'][1])
            col = int(dic['New-Move'][3])
            loc = row * 3 + col

            if self.board[loc] != 0 :
                self.quit()

            #Send message to peer
            self.socket.send(d_msg.encode())

            #Get ack
            ack = self.socket.recv(SIZE).decode()
            if not(check_msg(ack, self.recv_ip)) :
                self.quit()
        else: # 받은 메시지가 올바른 형식이 아니면
            return

        ######################################################

        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc)

        if self.state == self.active:    # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    # 상대방에게 클릭한 좌표를 메시지에 담아 보내는 함수 + ack 확인
    # ack형식 확인
    def send_move(self,selection):
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        row, col = divmod(selection, 3)
        ###################  Fill Out  #######################

        #row, col 값 메시지에 넣어서 보내기 + host 에 send_ip 넣어서 보내기
        send_msg = "SEND ETTTP/1.0\r\nHost:"+str(self.send_ip)+"\r\nNew-Move:("+str(row)+","+str(col)+")\r\n\r\n"
        self.socket.send(send_msg.encode())

        ack = self.socket.recv(SIZE).decode()
        if check_msg(ack, self.recv_ip):
            return True
        else :
            return False
        ######################################################


    # 승자를 이중 체크하는 함수.
    # winner가 클릭한 사용자이고(ME), get이 false이면 메시지 전송
    # winner가 YOU, get이 false이면 메시지를 받고 확인
    def check_result(self,winner,get=False):
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        # no skeleton
        ###################  Fill Out  #######################
        if winner == 'ME' and not get :
            send_msg = "SEND ETTTP/1.0\r\nHost:"+str(self.send_ip)+"\r\nWinner: ME\r\n\r\n"
            self.socket.send(send_msg.encode())

        elif winner == 'YOU' and get:
            msg = self.socket.recv(SIZE).decode()
            if not (check_msg(msg, self.recv_ip) and msg.endswith("ME\r\n\r\n")):
                self.quit()

        else:
            self.quit()

        return True

        ######################################################


    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv

    # 보드 업데이트
    def update_board(self, player, move, get=False):
        '''
        This function updates Board if is clicked

        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    # 게임이 끝났는지(승리자가 있는지) 확인하는 함수 ( check_result함수로 이중확인 )
    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    # 이긴 line에 하이라이트하는 함수
    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class

# 메시지가 ETTTP인지 + ip주소가 자신의 ip와 같은지 확인하는 함수
def check_msg(msg, recv_ip):
    '''
    Function that checks if received message is ETTTP format
    '''
    ###################  Fill Out  #######################
    # 문자열에서 첫 번 째 줄을 가져옵니다.
    first_line = msg.split('\r\n')[0]
    # 첫 번 째 줄에서 프로토콜 부분을 추출합니다.
    protocol = first_line.split(' ')[1]

    # 문자열에서 두 번 째 줄을 가져옵니다.
    second_line = msg.split('\r\n')[1]
    # 두 번 째 줄에서 host 부분을 추출합니다.
    host = second_line.split(':')[1]

    # 프로토콜이 ETTTP/1.0인지, Host가 recv_ip인지 확인합니다.
    if (protocol == "ETTTP/1.0" and host == recv_ip) :
        return True
    else :
        return False
    ######################################################