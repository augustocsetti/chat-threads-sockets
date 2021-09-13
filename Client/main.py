from logWindow import *
from mainWindow import *
from client import *

import threading



def start():

    name, addr, port = createLogWindow()

    # Iniciando Cliente
    Client = threading.Thread(target=createClient, args=(name, addr, port))
    Client.start()

    createMainWindow(name, addr, port)


if __name__ == "__main__":
    start()

