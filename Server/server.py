import threading
import socket
import sys
from datetime import datetime

from serverClient import Client
from config import *


class Server():

    def __init__(self):
        # Define família e tipo da conexão (AF_INET -> IPV4 | SOCK_STREAM -> TCP)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

        # Atrela conexão a server e port definidos
        self.s.bind(ADDR)

        # Lista de usuários conectados 
        self.clients = []

        # Variável do Loop principal
        self.online = True

        print("========== AbachaT Terminal ==========\n")
        print("Inicializando servidor...")
        
        # Inicia o servidor
        self.s.listen()

        print(f"[LISTENING] Server is listening on {SERVER} port {PORT}")

        exit = threading.Thread(target=self.closeServer, args=())
        exit.start()

        # Inicia inscrição
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

                # Adicionando à lista de clientes a classe do cliente aceita
                c = Client(self, username, conn)
                self.clients.append(c)

                # Atualizando lista de conexão do cliente
                self.userListUpdate()

                # Aviso de nova conexão
                _date = date()
                msg = f"{NEW_MESSAGE}<p><i>***{username} entrou no chat ({_date}). Conexões ativas {len(self.clients)}.***</i></p>"
                self.serverMsg(msg)
 
            except:
                print("[CLOSING] Server is closing.")
                self.s.close()
                self.online = False
                return


    def unsubscribe(self, client):
        # Remova usuário das listas e encerra comunicação
        self.clients.remove(client)

        client.conn.close()
 
        _date = date()
        msg = (f"{NEW_MESSAGE}<p><i>***{client.username} saiu do chat ({_date}). Conexões ativas {len(self.clients)}.***</i></p>")
        self.serverMsg(msg)

        # Atualizando lista de conexão do cliente
        self.userListUpdate()

    # Func. de disparo de msgns servidor-usuário
    def serverMsg(self, msg):

        #print(msg)

        # Recebendo variáveis já codificados para envio
        message, send_length = encodeMsg(msg)

        for client in self.clients:
            
            client.conn.send(send_length)
            client.conn.send(message)

    # Func. de disparo de msgns usuário-usuário
    def globalMsg(self, msg, client):

        # Recebendo data e hora
        _date = date()

        # Modelando a mensagem para os clientes e para o remetente
        msgAll = (f"<p><u>{client.username}</u> ({_date}):<br>{msg}</p>")
        msgSelf = (f"<p><b>Eu ({_date}):</b><br>{msg}</p>")

        #print(msgAll) 
        
        msgAll = (f"{NEW_MESSAGE}{msgAll}")
        msgSelf = (f"{NEW_MESSAGE}{msgSelf}")

        # Recebendo variáveis já codificados para envio
        message, send_length = encodeMsg(msgAll)
        messageSelf, send_lengthSelf = encodeMsg(msgSelf)

        # Enviando para todos os clientes conectados
        for c in self.clients:
            # Se o cliente a enviar não for remetente envia msg com nome do usuário
            if(c.conn != client.conn):
                c.conn.send(send_length)
                c.conn.send(message)
            # Se for envia modelo Self com você ao invés do nome
            else:
                c.conn.send(send_lengthSelf)
                c.conn.send(messageSelf)


    def userListUpdate(self):

        for c in self.clients:
            # Limpando lista de conexão
            message, send_length = encodeMsg(f"{CLEAR_LIST}")            
            c.conn.send(send_length)
            c.conn.send(message)

            # Enviando novos usuários
            for client in self.clients:
                if(c.conn == client.conn):
                    message, send_length = encodeMsg(f"{NAME_LIST}{client.username} (Você)")
                else:
                    message, send_length = encodeMsg(f"{NAME_LIST}{client.username}")
                c.conn.send(send_length)
                c.conn.send(message)


    def closeServer(self):
        input("Pressione [ENTER] para encerrar o servidor\n")
        self.online = False
        self.s.close()
        sys.exit()


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