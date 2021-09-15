import socket

# MSG CONFIG
HEADER = 64
FORMAT = "utf-8"

#Variáveis de teste
USERNAME = "Test"
ADDR = "localhost"
PORT = 5001

# SOCKET CONN
SERVER = socket.gethostbyname(socket.gethostname())
USERNAME = "TEST"
PORT = 5001
ADDR = (SERVER, PORT)

# SYSTEM MSGM
DISCONNECT_MESSAGE = "[DISCONNECT]"

NEW_MESSAGE = '0'
NAME_LIST = '1'
CLEAR_LIST = '2'

DEFINE_NAME = 1
PROBLEM_NAME = 2



