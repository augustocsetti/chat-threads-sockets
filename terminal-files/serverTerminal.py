import threading
import socket
from datetime import datetime

from config import *


class Server():

    def __init__(self):
        # Define família e tipo da conexão (AF_INET -> IPV4 | SOCK_STREAM -> TCP)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

        # Atrela conexão a server e port definidos
        self.s.bind(ADDR)

        # Lista de usuários conectados
        self.connected = []
        self.username = []

        # Variável do Loop principal
        self.online = True

        print("========== AbachaT Terminal ==========\n")
        print("Inicializando servidor...")
        
        # Inicia o servidor
        self.s.listen()
        print(f"[LISTENING] Server is listening on {SERVER} port {PORT}")

        self.subscribe()
        

    def subscribe(self):
        while self.online:
            try:
                # Aceitando conexão
                conn, addr = self.s.accept()

                # Recebendo nome de usuário
                username = '' # resetando variável
                username_lenght = int(conn.recv(HEADER).decode(FORMAT)) # recebendo e decodificando tamanho do nome
                username = conn.recv(username_lenght).decode(FORMAT)

                # Adicionando às listas de clientes o nome e a conexão
                self.username.append(username)
                self.connected.append(conn)

                # Criando Thread para novo cliente
                thread = threading.Thread(target=self.update, args=(conn, username))
                thread.start()

                # Aviso de nova conexão
                msg = f"{username} entrou no chat. Conexões ativas {len(self.connected)}."
                self.serverMsg(msg)
 
            except:
                print("[CLOSING] Server is closing.")
                self.s.close()
                self.online = False
                return


    def unsubscribe(self, conn, username):
        # Remova usuário das listas e encerra comunicação
        index = self.connected.index(conn)
        self.username.pop(index)
        self.connected.remove(conn)
 
        conn.close()

        _date = date()
        msg = (f"{username} saiu da chat ({_date}).")
        self.serverMsg(msg)


    def update(self, conn, username):
        client_online = True
        while client_online:
            try:
                msg_lenght = conn.recv(HEADER).decode(FORMAT)
                if msg_lenght:
                    msg_lenght = int(msg_lenght)
                    msg = conn.recv(msg_lenght).decode(FORMAT)

                    # Mensagem de desconexão
                    if msg == DISCONNECT_MESSAGE:
                        self.unsubscribe(conn, username)
                        client_online = False
                        return
                
                    # Loop de envio a outros usuários
                    self.globalMsg(msg, conn, username)
                    msg = ''
                

            except: # Falha de conexão
                self.unsubscribe(conn, username)
                client_online = False
                return

    # Função de definição de operação
    def handleMsg(self, msg, conn, username):
        if ('op' == NEW_MESSAGE):
            self.globalMsg(msg, conn, username)
            
        elif ('op' == 1):
            pass


    # Func. de disparo de msgns servidor-usuário
    def serverMsg(self, msg):

        print(msg)       

        # Recebendo variáveis já codificados para envio
        message, send_length = encodeMsg(msg)

        for client in self.connected:
            client.send(send_length)
            client.send(message)


    # Func. de disparo de msgns usuário-usuário
    def globalMsg(self, msg, conn, username):

        # Recebendo data e hora
        _date = date()

        # Modelando a mensagem para os clientes e para o remetente
        msgAll = (f"{username} ({_date}): {msg}")
        msgSelf = (f"Eu ({_date}): {msg}")
        print(msgAll)       

        # Recebendo variáveis já codificados para envio
        message, send_length = encodeMsg(msgAll)
        messageSelf, send_lengthSelf = encodeMsg(msgSelf)

        # Enviando para todos os clientes conectados
        for client in self.connected:
            # Se o cliente a enviar não for remetente envia msg com nome do usuário
            if(client != conn):
                client.send(send_length)
                client.send(message)
            # Se for envia modelo Self com você ao invés do nome
            else:
                client.send(send_lengthSelf)
                client.send(messageSelf)


def date():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return(f"{now.day}/{now.month}/{now.year} - {current_time}")

def encodeMsg(msg):
    message = str(msg).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    return message, send_length

if ("__main__" == __name__):
    s = Server()