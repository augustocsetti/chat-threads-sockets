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

        print("Inicializando servidor...")
        # Inicia o servidor AQUI
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

                self.username.append(username)
                self.connected.append(conn)

                # Criando Thread para novo cliente
                thread = threading.Thread(target=self.update, args=(conn, username))
                thread.start()

                # Aviso de nova conexão
                msg = f"{username} entrou no chat. Conexões ativas {len(self.connected)}."
                self.serverMsg(msg)
                print(msg)
                
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
        print(msg)

    def update(self, conn, username):
        client_online = True
        while client_online:
            try:
                msg_lenght = conn.recv(HEADER).decode(FORMAT) #wait
                if msg_lenght:
                    msg_lenght = int(msg_lenght)
                    msg = conn.recv(msg_lenght).decode(FORMAT)

                    # Mensagem de desconexão
                    if msg == DISCONNECT_MESSAGE:
                        self.unsubscribe(conn, username)
                        client_online = False
                        return
                    
                    # Loop de envio a outros usuários
                    self.globalMsg(conn, username, msg)

            except: # Falha de conexão
                self.unsubscribe(conn, username)
                client_online = False
                return

    # def systemMsg(self, conn, op):
    #     if(op == 1):
    #         continue
    #     message = msg.encode(FORMAT)
    #     msg_length = len(message)
    #     send_length = str(msg_length).encode(FORMAT)
    #     send_length += b' ' * (HEADER - len(send_length))

    def serverMsg(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))

        for client in self.connected:
            client.send(send_length)
            client.send(message)

    def globalMsg(self, conn, username, msg):
        _date = date()
        msg = (f"{username} ({_date}): {msg}")
        print(msg)

        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))

        for client in self.connected:
            if(client != conn):
                client.send(send_length)
                client.send(message)
            else:
                continue

def date():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return(f"{now.day}/{now.month}/{now.year} - {current_time}")

if ("__main__" == __name__):
    s = Server()