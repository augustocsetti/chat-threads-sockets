import socket

# DEFINIÇÕES PARA SOCKET
HEADER = 64 # tamanho da msgm padrão (bytes)
FORMAT = "utf-8" # formato para codificação

SERVER = socket.gethostbyname(socket.gethostname()) # endereço de IP (local)
PORT = 5000 # porta para comunicação
ADDR = (SERVER, PORT) 

# TAGS PARA COMUNICAÇÕES DO SISTEMA
NEW_MESSAGE = '0'
NAME_LIST = '1'
CLEAR_LIST = '2'
DISCONNECT_MESSAGE = '3'
CHANGE_NAME = '4'