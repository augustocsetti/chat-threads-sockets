import threading
import socket

HEADER = 64

FORMAT = "utf-8"
DISCONNECT_MESSAGE = "[DISCONNECT]"
SERVER = "192.168.1.113"
PORT = 5000


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
        self.thread = threading.Thread(target=self.recvMsg, args=())
        self.thread.start()
               
        self.main_loop()

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
            except: # Se o programa for interrompido a conexão é encerrada
                self.disconnect()

    def sendMsg(self, msg):
        # Codifica a mensagem e envia tamanho
        try:
            message = str(msg).encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            self.client.send(send_length)
            self.client.send(message)
        except:
            print("ERRO! Falha na conexão")
            self.online = False

    def recvMsg(self):
        # Loop de recebimento de msgm
        while self.online:
            try:
                msg_lenght = self.client.recv(HEADER).decode(FORMAT)
                if msg_lenght:
                    msg_lenght = int(msg_lenght)
                    msg = self.client.recv(msg_lenght).decode(FORMAT)
                    print(msg)
            except:
                self.online = False

    def disconnect(self):
        # Msgm de desconexão
        print("Você está se desconectando...")
        self.sendMsg(DISCONNECT_MESSAGE)
        self.client.close()
        self.online = False
        print("[CONEXÃO ENCERRADA]")


def createClient(username, server, port):
    c = Client(username, server, port)


if(__name__ == "__main__"):
    createClient(input("Insira seu nome: "), SERVER, PORT)