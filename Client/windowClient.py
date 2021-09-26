import socket
import threading
from config import*

# Classe worker do cliente
# - gerencia conexão socket
# - gerencia recebimento e manipulação de mensagens
# - gerencia envio de mensagens

class Client():

    # Inicilizando cliente socket
    def __init__(self, username, address, port, win):

        # Define família e tipo da conexão (AF_INET -> IPV4 | SOCK_STREAM -> TCP)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Conecta com servidor socket
        ADDR = (address, int(port))
        self.client.connect(ADDR)

        # Recebe parâmetros
        self.username = username # define username da instância
        self.win = win # salva referência da janela p comunicação
        self.online = True # seta cliente como online

        # Enviando nome do usuário ao servidor
        message, send_length = encodeMsg(self.username)
        self.client.send(send_length) # tamanho
        self.client.send(message) # msg

		# Criando Thread para receber mensagens
        self.thread_recv = threading.Thread(target=self.recvMsg, args=())
        self.thread_recv.start()
    
    # Recebe mensagem
    def recvMsg(self):

        # Loop de recebimento de msgm
        while self.online: # enquanto cliente está online
            try:
                # espera receber mensagem do servidor
                msg_lenght = self.client.recv(HEADER).decode(FORMAT) # recebendo e decodificando (em utf-8) tamanho do nome
                if msg_lenght: # se tam for recebido
                    msg_lenght = int(msg_lenght) # armazena valor em int
                    msg = self.client.recv(msg_lenght).decode(FORMAT) # recebe e decodifica msgm

                    # Chama função para lidar com mensagem
                    self.handleMsg(msg)

            except: # Se houver erro ou falha de conexão
                # seta cliente como offline
                self.online = False

    # Lida com mensagem
    def handleMsg(self, msg):

        # Separa TAG da mensagem
        op = msg[0] # salva primeiro caractere
        msg_list = list(msg) # converte em lista
        msg_list.pop(0) # apaga TAG
        msg = "".join(msg_list) # armazena em string

        # Define operação a ser realizada
        if (op == NEW_MESSAGE):	# se é TAG de nova msgm
            self.win.signal.chatLabel.emit(msg) # envia sinal a interface para imprimir msg

        elif (op == CLEAR_LIST): # se é TAG de limpar lista
            self.win.signal.listUser.emit('') # envia sinal vazio para janela limpar lista de usuários conectados

        elif (op == NAME_LIST): # se é TAG de lista de nomes
            self.win.signal.listUser.emit(msg) # envia nome para a janela adicionar a lista de usuários conectados

    # Envia mensagem
    def sendMsg(self, msg, op):

        if(self.online): # se o usuário estiver online
            try:
                msg = op + msg # junta TAG a msg
                message, send_length = encodeMsg(msg) # decodifica
                self.client.send(send_length) # envia tamanho
                self.client.send(message) # envia msgm

            except: # se falha na comunicação
                self.disconnect() # desconecta worker

    # Desconecta cliente
    def disconnect(self):

        if(self.online): # se estiver online
            # manda sinal com msgm de desconexão a janela
            self.win.signal.chatLabel.emit("<p><i>Você está se desconectando...</i><p>")

            # envia mensagem de desconexão ao servidor
            message, send_length = encodeMsg(DISCONNECT_MESSAGE)
            self.client.send(send_length) # tamanho
            self.client.send(message) # msgm
            
            # seta cliente como offline, encerra conexão e envia sinal a janela
            self.online = False
            self.client.close()
            self.win.signal.chatLabel.emit("<p><i><b>[CONEXÃO ENCERRADA]</i></p>")


# FUNÇÕES DE SUPORTE

# codifica a mensagem para enviar via socket
def encodeMsg(msg):
    message = str(msg).encode(FORMAT) # codifica o texto da mensagem no formato utf-8
    msg_length = len(message) # armazena tamanho da mensagem codificada
    send_length = str(msg_length).encode(FORMAT) # codifica tamanho de msg_length eno formato utf-8
    send_length += b' ' * (HEADER - len(send_length))# completa a mensagem de tamanho com espaços em branco até ser igual ao HEADER definido
    return message, send_length