from logWindow import createLogWindow
from mainWindow import *


def start():
    # Iniciando janela de login e recebendo parâmetro
    name, addr, port = createLogWindow()

    # Iniciando Janela do chat, que inicia a classe client
    createMainWindow(name, addr, port)

if __name__ == "__main__":
    start()

