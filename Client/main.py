from logWindow import *
from mainWindow import *
from client import *

import threading



def start():
    # Iniciando janela de login e recebendo parâmetro
    name, addr, port = createLogWindow()

    # Iniciando Cliente e Janela do chat
    createMainWindow(name, addr, port)

    # createMainWindow(name, addr, port)

if __name__ == "__main__":
    start()

