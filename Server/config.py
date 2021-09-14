import socket

HEADER = 64
FORMAT = "utf-8"

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5001
ADDR = (SERVER, PORT)

# Códigos para mensagem do sistema
DISCONNECT_MESSAGE = "[DISCONNECT]"
ADD = 1
OUT = 0
NEW_MSG = 0
DEFINE_NAME = 1
PROBLEM_NAME = 2
NAME_LIST = 3
NAME_LIST_END = -1