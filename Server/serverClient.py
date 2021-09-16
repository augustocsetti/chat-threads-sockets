import threading
from config import *

class Client():

    def __init__(self, server, username, conn):

        self.s = server
        self.username = username
        self.conn = conn

        thread = threading.Thread(target=self.start, args=())
        thread.start()


    def start(self):
        client_online = True
        while client_online:
            try:
                msg_lenght = self.conn.recv(HEADER).decode(FORMAT)
                if msg_lenght:
                    msg_lenght = int(msg_lenght)
                    msg = self.conn.recv(msg_lenght).decode(FORMAT)

                    # Mensagem de desconexão
                    if msg == DISCONNECT_MESSAGE:
                        self.s.unsubscribe(self)
                        client_online = False
                        return
                
                    # Loop de envio a outros usuários
                    self.handleMsg(msg)
                    msg = ''
                
            except: # Falha de conexão
                self.s.unsubscribe(self)
                client_online = False
                return
    
    
    def handleMsg(self, msg):

        op = msg[0]
        msg_list = list(msg)
        msg_list.pop(0)
        msg = "".join(msg_list)

        if (op == NEW_MESSAGE):
            self.s.globalMsg(msg, self)
            
        elif (op == 1):
            pass