from config import *
import threading

# Classe worker
# - recebe msgns do cliente
# - lida com solicitações e se comunica com a classe principal

class Client():

    # Inicializa a instância do cliente no server
    def __init__(self, server, username, conn):

        # Armazena a referência ao servidor para realizar comunicação
        self.s = server

        # Recebe informações do cliente
        self.username = username # recebe nome de usuário do cliente
        self.conn = conn # recebe o socket do cliente

        # Define cliente como online para loop principal
        self.clientOnline = True

        # Cria thread para receber msgns do cliente
        thread = threading.Thread(target=self.start, args=())
        thread.start()

    # Aguarda o recebimento de uma mensagem do cliente
    def start(self):
        
        # Enquanto o cliente estiver online recebe mensagem dele
        while self.clientOnline and self.s.online:
            try:
                # Recebe o tamanha da mensagem a ler
                msg_lenght = self.conn.recv(HEADER).decode(FORMAT) # recebendo e decodificando (em utf-8) tamanho do nome
                if msg_lenght: # se tam for recebido
                    msg_lenght = int(msg_lenght) # armazena valor em int
                    msg = self.conn.recv(msg_lenght).decode(FORMAT) # recebe e decodifica msgm
                    
                    # Chama função para lidar com mensagem
                    self.handleMsg(msg)
                
            except: # Se houver erro ou falha de conexão
                # Desconecta cliente
                self.s.unsubscribe(self)
                self.clientOnline = False
                return
    
    # Lida com mensagem recebida
    def handleMsg(self, msg):

        # Separa TAG da mensagem
        op = msg[0] # salva primeiro caractere
        msg_list = list(msg) # converte em lista
        msg_list.pop(0) # apaga TAG
        msg = "".join(msg_list) # armazena em string

        # Define operação a ser realizada
        if (op == NEW_MESSAGE): # se é TAG de nova msgm
            self.s.globalMsg(msg, self) # envia a usuários conectados
        
        elif (op == CHANGE_NAME): # se é TAG de alteração de nome
            # Comunica a usuários conectados troca de nome
            notify = f"{NEW_MESSAGE}<p><i>***<b>{self.username}</b> alterou seu nome para <b>{msg}</b>.***</i></p>"
            self.s.serverMsg(notify)

            # Altera atributo de username
            self.username = msg
            self.s.userListUpdate() # atualiza lista dos clientes

        elif (op == DISCONNECT_MESSAGE): # se é TAG de desconexão
            self.clientOnline = False # seta cliente como offline
            self.s.unsubscribe() # solicia desconexão ao servidor
