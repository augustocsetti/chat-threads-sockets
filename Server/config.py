import socket

HEADER = 64
FORMAT = "utf-8"

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5000
ADDR = (SERVER, PORT)

# Códigos para mensagem do sistema
NEW_MESSAGE = '0'
NAME_LIST = '1'
CLEAR_LIST = '2'
DISCONNECT_MESSAGE = '3'
