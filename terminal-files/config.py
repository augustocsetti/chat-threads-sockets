import socket

HEADER = 64
FORMAT = "utf-8"

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5001
ADDR = (SERVER, PORT)

# Códigos para mensagem do sistema
DISCONNECT_MESSAGE = "[DISCONNECT]"
NEW_MESSAGE = '0'

#DEFINE_NAME = '1'
#PROBLEM_NAME = '2'
