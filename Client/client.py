from config import *
import threading
import socket


class Client():

    def __init__(self, username, server, port):
        
        # Iniciando conexão com servidor
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ADDR = (server, int(port))
        self.client.connect(ADDR)
        self.online = True

        # Criando e enviando nome do usuário
        self.name = username
        self.sendMsg(self.name)

        # Criando Thread para receber mensagens
        self.thread_recv = threading.Thread(target=self.recvMsg, args=())
        self.thread_recv.start()
               
        # (PARA USAR NO TERMINAL) Iniciando Loop de envio de mensagens
        # self.thread_send = threading.Thread(target=self.main_loop, args=())
        # self.thread_send.start()
        # #self.main_loop()      


    def main_loop(self):
        # Esperando usuário enviar mensagem (msg em branco encerra conexão)
        while (self.online):
            try:
                msg = str(input())
                if (msg != "" and msg != DISCONNECT_MESSAGE):
                    self.sendMsg(msg)
                    msg = ""
                else:
                    self.disconnect()
                    self.online = False
            except: # Se o programa for interrompido a conexão é encerrada
                self.disconnect()


    def sendMsg(self, msg):
            try:
                message, send_length = encodeMsg(msg)
                self.client.send(send_length)
                self.client.send(message)

                if (msg == DISCONNECT_MESSAGE):
                    self.disconnect()

            except:
                print("Falha na conexão")
                self.online = False


    def recvMsg(self):
        # Loop de recebimento de msgm
        while self.online:
            try:
                msg_lenght = self.client.recv(HEADER).decode(FORMAT)
                if msg_lenght:
                    msg_lenght = int(msg_lenght)
                    msg = self.client.recv(msg_lenght).decode(FORMAT)
                    self.handleMsg(msg)
            except:
                self.online = False


    def disconnect(self):

        # Encerrando conexão socket
        print("Você está se desconectando...")
        self.client.close()
        self.online = False
        print("[CONEXÃO ENCERRADA]")


    def handleMsg(self, msg):
        print(f"OPM:{msg[OP]} NL:{NAME_LIST}")
        if (msg[OP] == NAME_LIST):
            print("LOOP")
            msg.pop(0)
            print(f"Mensagem tratada:")
            self.userList.append(msg)
                
# SUPORT FUNCTIONS
def encodeMsg(msg):
    message = str(msg).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    return message, send_length


def createClient(username, server, port):
    c = Client(username, server, port)

if(__name__ == "__main__"):
    createClient(input("Insira seu nome: "), SERVER, PORT)