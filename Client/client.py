import socket
import threading
from config import*

class Client():

    def __init__(self, username, address, port, win):

        # Iniciando conexão com servidor
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ADDR = (address, int(port))
        
        self.client.connect(ADDR)

        self.username = username
        self.win = win
        self.online = True

        # Criando e enviando nome do usuário
        message, send_length = encodeMsg(self.username)
        self.client.send(send_length)
        self.client.send(message)

		# Criando Thread para receber mensagens
        self.thread_recv = threading.Thread(target=self.recvMsg, args=())
        self.thread_recv.start()
    

    def sendMsg(self, msg):

        if(self.online):
            try:
                msg = '0' + msg
                message, send_length = encodeMsg(msg)
                self.client.send(send_length)
                self.client.send(message)

            except:
                #print("ERRO no servidor")
                self.disconnect()


    def recvMsg(self):

        # Loop de recebimento de msgm
        while self.online:
            try:
                # Recebe a mensagem
                msg_lenght = self.client.recv(HEADER).decode(FORMAT)
                if msg_lenght:
                    msg_lenght = int(msg_lenght)
                    msg = self.client.recv(msg_lenght).decode(FORMAT)

                    self.handleMsg(msg)
                    msg_lenght = ''

            except:
                self.online = False
                #self.win.signal.chatLabel.emit("Erro na conexão") #Não sei
                #self.disconnect()


    def handleMsg(self, msg):

        op = msg[0]
        msg_list = list(msg)
        msg_list.pop(0)
        message = "".join(msg_list)

        # Recebe mensagem
        if (op == NEW_MESSAGE):	
            self.win.signal.chatLabel.emit(message)

        # # Recebe lista de usuários conectados
        elif (op == CLEAR_LIST):
            self.win.signal.listUser.emit('')

        # Limpa lista de conexão
        elif (op == NAME_LIST):
            self.win.signal.listUser.emit(message)


    def disconnect(self):

        if(self.online):
            self.win.signal.chatLabel.emit("<p><i>Você está se desconectando...</i><p>")

            message, send_length = encodeMsg(DISCONNECT_MESSAGE)
            self.client.send(send_length)
            self.client.send(message)
            
            self.online = False
            self.client.close()
            self.win.signal.chatLabel.emit("<p><i><b>[CONEXÃO ENCERRADA]</i></p>")


# FUNÇÕES DE SUPORTE
def encodeMsg(msg):
    message = str(msg).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    return message, send_length