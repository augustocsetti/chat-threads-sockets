import threading
import socket
from datetime import datetime

from serverClient import Client
from config import *

# Classe principal
# - realiza conexão e encerramento do servidor socket
# - recebe novas conexões
# - gerencia conexões e desconexões
# - gerencia envio de msgns aos cliente

class Server():

    # Inicializa servidor e threads de encerramento
    def __init__(self):
       
        # Define família e tipo da conexão (AF_INET -> IPV4 | SOCK_STREAM -> TCP)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

        # Atrela conexão a server e port definidos
        self.s.bind(ADDR)

        # Armazena lista de usuários conectados 
        self.clients = []

        # Seta o servidor como ligado
        self.online = True

        print("========== AbachaT Terminal ==========\n")
        print("Inicializando servidor...")
        
        # Abre o servidor ao recebimento de novas conexões e msgns
        self.s.listen()

        print(f"[LISTENING] Server is listening on {SERVER} port {PORT}")

        # Inicializa thread que capta uma entrada para encerrar servidor
        exit = threading.Thread(target=self.closeServer, args=())
        exit.start()

        # Função de inicialização de inscrições via socket
        self.subscribe()

    # Recebe inscrição de novos usuários e inicializa worker
    def subscribe(self):
       
        # Enquando o servidor estiver ligado
        while self.online:
            try:
                # Aguarda a conexão de um novo cliente e salva as infos do socket
                conn, addr = self.s.accept()

                # Recebendo nome de usuário
                username_lenght = int(conn.recv(HEADER).decode(FORMAT)) # recebendo e decodificando tamanho do nome
                username = conn.recv(username_lenght).decode(FORMAT) # recebendo e decodificando nome

                # Adicionando à lista de clientes a instância do cliente aceita
                c = Client(self, username, conn) # envia dados da conexão ao construtor
                self.clients.append(c) # adiciona na lista de clientes conectados

                # Envia lista de usuários atualizada aos clientes
                self.userListUpdate()

                # Envia notificação da entrada aos clientes
                _date = date() # recebe data e hora
                msg = f"{NEW_MESSAGE}<p><i>***{username} entrou no chat ({_date}). Conexões ativas {len(self.clients)}.***</i></p>"
                self.serverMsg(msg)
 
            # Caso acontece algum erro com a conexão encerra-se o servidor
            except:
                print("[CLOSING] Server is closing.")
                self.s.close() # encerra socket
                self.online = False # offline
                return

    # Realiza desinscrição de um usuário
    def unsubscribe(self, client):
        
        # Remova usuário das listas de clientes conectados
        self.clients.remove(client)

        # Encerra socket do cliente
        client.conn.close()
 
        # Comunica saída aos clientes conectados
        _date = date()
        msg = (f"{NEW_MESSAGE}<p><i>***{client.username} saiu do chat ({_date}). Conexões ativas {len(self.clients)}.***</i></p>")
        self.serverMsg(msg)

        # Atualizando lista de conexão do cliente
        self.userListUpdate()

    # Func. de disparo de msgns servidor-stream
    def serverMsg(self, msg):

        # Recebendo variáveis já codificados para envio
        message, send_length = encodeMsg(msg)

        # Envia mensagem a todos clientes conectados
        for client in self.clients:       
            client.conn.send(send_length)
            client.conn.send(message)

    # Func. de disparo de msgns usuário-stream
    def globalMsg(self, msg, client):

        # Recebendo data e hora
        _date = date()

        # Modelando a mensagem para os clientes e para o remetente
        msgAll = (f"<p><u>{client.username}</u> ({_date}):<br>{msg}</p>")
        msgSelf = (f"<p><b>Eu ({_date}):</b><br>{msg}</p>")
        
        # Insere TAG de nova mensagem para enviar ao cliente
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

    # Envia lista de usuários conectados ao cliente
    def userListUpdate(self):

        # Para todos os clientes conectados
        for c in self.clients:
            # Limpando lista de conexão
            message, send_length = encodeMsg(f"{CLEAR_LIST}")            
            c.conn.send(send_length)
            c.conn.send(message)

            # Enviando nova lista de usuários
            for client in self.clients:
                # Adiciona-se a TAG para que o cliente lide com a msgm corretamente
                # se o cliente for receber seu nome adiciona-se "você" ao fim da msgm
                if(c.conn == client.conn):
                    message, send_length = encodeMsg(f"{NAME_LIST}{client.username} (Você)")
                else:# se não, envia TAG e nome
                    message, send_length = encodeMsg(f"{NAME_LIST}{client.username}")
                c.conn.send(send_length)
                c.conn.send(message)

    # Encerra o servidor
    def closeServer(self):
        
        # Espera input no terminal do servidor para encerrar aplicação
        input("Pressione [ENTER] para encerrar o servidor\n")

        # Ao receber, seta variável para offline, encerra o socket e fecha app
        self.online = False
        self.s.close()


# FUNÇÕES DE SUPORTE

# Retorna data e hora
def date():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return(f"{now.day}/{now.month}/{now.year} - {current_time}")

# codifica a mensagem para enviar via socket
def encodeMsg(msg):
    message = str(msg).encode(FORMAT) # codifica o texto da mensagem no formato utf-8
    msg_length = len(message) # armazena tamanho da mensagem codificada
    send_length = str(msg_length).encode(FORMAT) # codifica tamanho de msg_length eno formato utf-8
    send_length += b' ' * (HEADER - len(send_length))# completa a mensagem de tamanho com espaços em branco até ser igual ao HEADER definido
    return message, send_length


if ("__main__" == __name__):
    s = Server()