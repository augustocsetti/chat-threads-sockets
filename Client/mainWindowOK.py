import threading
import socket
import sys
from config import*

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextBrowser


def createMainWindow(name, address, port):

	app = QApplication(sys.argv)
	win = MainWindow(name, address, port)

	win.show()
	app.exec_()


# Classe para definir sinais enviados pela thread_recv a janela principal 
class MySignal(QtCore.QObject):
	listUser = QtCore.pyqtSignal(str) # ação sobre lista de usuários conectados
	chatLabel = QtCore.pyqtSignal(str) # ação sobre text browser do chat
	
# Janela principal do cliente
class MainWindow(QMainWindow):

	def __init__(self, username, address, port):

		# Inicializando construtor da janela
		super(QMainWindow, self).__init__()

		# Carregando componentes da interface
		self.setupUi()

		# Conectando aos sinais
		self.signal = MySignal()
		self.signal.listUser.connect(self.listUpdate)
		self.signal.chatLabel.connect(self.chatUpdate)

        # Iniciando conexão com servidor
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ADDR = (address, int(port))

		try:
			self.client.connect(ADDR)

		except Exception as error:
			print(f"[PROBLEMA DE CONEXÃO]\n{error}")
			sys.exit()	

		self.online = True

        # Criando e enviando nome do usuário
		self.name = username
		message, send_length = encodeMsg(self.name)
		self.client.send(send_length)
		self.client.send(message)
		
		# Criando Thread para receber mensagens
		self.thread_recv = threading.Thread(target=self.recvMsg, args=[self])
		self.thread_recv.start()


	def send(self):
		try:
			msg = self.msg.text()
		
			if(msg == ''):
				return
			else:
				msg = '0' + msg
				message, send_length = encodeMsg(msg)
				self.client.send(send_length)
				self.client.send(message)

				if (msg == DISCONNECT_MESSAGE):
					self.disconnect()

				self.msg.setText('')
		except:
			print("ERRO no servidor")
			self.disconnect()


	def recvMsg(self, win):
		a = win
		# Loop de recebimento de msgm
		while self.online:
			try:
				# Recebe a mensagem
				msg_lenght = self.client.recv(HEADER).decode(FORMAT)
				if msg_lenght:
					msg_lenght = int(msg_lenght)
					msg = self.client.recv(msg_lenght).decode(FORMAT)
					
					self.handleMsg(msg, a)
					
					msg_lenght = ''
			except:
				self.online = False


	def handleMsg(self, msg, win):

		op = msg[0]
		msg_list = list(msg)
		msg_list.pop(0)
		message = "".join(msg_list)
		
		# Recebe mensagem
		if (op == NEW_MESSAGE):	
			win.signal.chatLabel.emit(message)
		
		# # Recebe lista de usuários conectados
		elif (op == CLEAR_LIST):
			win.signal.listUser.emit('')

		# Limpa lista de conexão
		elif (op == NAME_LIST):
			win.signal.listUser.emit(message)


	def disconnect(self):

		# Encerrando conexão socket
		self.chat.append("Você está se desconectando...")
		self.online = False
		self.client.close()
		self.chat.append("[CONEXÃO ENCERRADA]")
		self.close()


	def updateUserList(self, list):
		self.userList.clear()


	def setupUi(self):

		# WINDOW
		self.setObjectName("MainWindow")
		self.resize(800, 600)
		self.setStyleSheet("background-color: qlineargradient(spread:repeat, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(223, 144, 138, 255), stop:0.971591 rgba(57, 255, 136, 255));")

		# MAIN GRID
		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout.setContentsMargins(20, 20, 20, 20)
		self.gridLayout.setObjectName("gridLayout")

		# LOGO
		self.logo = QtWidgets.QLabel(self.centralwidget)
		self.logo.setEnabled(True)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
		self.logo.setSizePolicy(sizePolicy)
		self.logo.setMinimumSize(QtCore.QSize(200, 200))
		self.logo.setMaximumSize(QtCore.QSize(300, 300))
		self.logo.setSizeIncrement(QtCore.QSize(400, 400))
		self.logo.setBaseSize(QtCore.QSize(150, 151))
		self.logo.setStyleSheet("background-color: qlineargradient(spread:repeat, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(255, 255, 255, 0));")
		self.logo.setText("")
		self.logo.setPixmap(QtGui.QPixmap(u"img\\logo.png"))
		self.logo.setScaledContents(True)
		self.logo.setWordWrap(False)
		self.logo.setIndent(-2)
		self.logo.setObjectName("logo")
		self.gridLayout.addWidget(self.logo, 0, 0, 1, 1)

		# TÍTULO
		self.titulo = QtWidgets.QLabel(self.centralwidget)
		font = QtGui.QFont()
		font.setFamily("Ink Free")
		font.setPointSize(28)
		font.setBold(True)
		font.setUnderline(False)
		font.setWeight(75)
		self.titulo.setFont(font)
		self.titulo.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 0));\n"
		"color: rgb(255, 255, 255);")
		self.titulo.setAlignment(QtCore.Qt.AlignCenter)
		self.titulo.setObjectName("titulo")
		self.gridLayout.addWidget(self.titulo, 2, 0, 1, 1)
		
		# LABEL USUÁRIOS CONECTADOS
		self.label = QtWidgets.QLabel(self.centralwidget)    
		font = QtGui.QFont()
		font.setFamily("Calibri")
		font.setPointSize(12)
		self.label.setFont(font)
		self.label.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 0));\n"
		"color: rgb(255, 255, 255);")
		self.label.setObjectName("label")
		self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

		spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.gridLayout.addItem(spacerItem, 5, 2, 1, 1)
		spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem1, 4, 1, 1, 1)

		# LISTA USUÁRIOS CONECTADOS
		self.userList = QtWidgets.QTextBrowser(self.centralwidget)
		#QtCore.QMetaObject.connectSlotsByName(self.userList)
		self.userList.setMinimumSize(QtCore.QSize(250, 200))
		self.userList.setMaximumSize(QtCore.QSize(200, 500))
		font = QtGui.QFont()
		font.setFamily("Calibri")
		font.setPointSize(14)
		self.userList.setFont(font)
		self.userList.setStyleSheet("background-color: rgb(255, 255, 255);\n"
		"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 115));\n"
		"color: rgb(135, 97, 88);")
		self.userList.setObjectName("userList")
		self.gridLayout.addWidget(self.userList, 4, 0, 1, 1)

		# TEXT MENSAGEM
		self.msg = QtWidgets.QLineEdit(self.centralwidget)
		self.msg.setMinimumSize(QtCore.QSize(0, 40))
		font = QtGui.QFont()
		font.setFamily("Calibri")
		font.setPointSize(14)
		self.msg.setFont(font)
		self.msg.setStyleSheet("background-color: rgb(255, 255, 255);\n"
		"color: rgb(135, 97, 88);\n"
		"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 115));")
		self.msg.setObjectName("msg")
		self.gridLayout.addWidget(self.msg, 6, 2, 1, 1)

		# CAMPO PARA MENSAGENS
		self.chat = QtWidgets.QTextBrowser(self.centralwidget)
		self.chat.setMaximumSize(QtCore.QSize(4000, 4000))
		font = QtGui.QFont()
		font.setFamily("Calibri")
		font.setPointSize(12)
		self.chat.setFont(font)
		self.chat.setStyleSheet("background-color: rgb(255, 255, 255);\n"
		"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 115));\n"
		"color: rgb(135, 97, 88);")
		self.chat.setObjectName("chat")
		self.gridLayout.addWidget(self.chat, 0, 2, 5, 2)

		# SEND BUTTON
		self.sendBtn = QtWidgets.QPushButton(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.sendBtn.sizePolicy().hasHeightForWidth())
		self.sendBtn.setSizePolicy(sizePolicy)
		self.sendBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.sendBtn.setStyleSheet("background-color: rgb(255, 255, 255);\n"
		"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 115));")
		self.sendBtn.setObjectName("sendBtn")
		self.gridLayout.addWidget(self.sendBtn, 6, 3, 1, 1)
		self.sendBtn.clicked.connect(self.send)

		# MENU BAR
		self.menubar = QtWidgets.QMenuBar(self)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 783, 21))
		self.menubar.setStyleSheet("background-color: rgb(255, 255, 255);")
		self.menubar.setObjectName("menubar")
		self.menuOptions = QtWidgets.QMenu(self.menubar)
		self.menuOptions.setObjectName("menuOptions")
		self.menuSobre = QtWidgets.QMenu(self.menubar)
		self.menuSobre.setObjectName("menuSobre")
		self.setMenuBar(self.menubar)
		self.actionQuit = QtWidgets.QAction(self)
		self.actionQuit.setObjectName("actionQuit")
		self.actionLimpar = QtWidgets.QAction(self)
		self.actionLimpar.setObjectName("actionLimpar")

		# Define ações e objetos ao acessar a barra de menu
		self.actionNova_Conex_o = QtWidgets.QAction(self) # cria menu
		self.actionNova_Conex_o.setObjectName("actionNova_Conex_o") #
		self.menuOptions.addAction(self.actionNova_Conex_o)
		self.menuOptions.addAction(self.actionLimpar)
		self.menuOptions.addSeparator() # separador
		self.menuOptions.addAction(self.actionQuit)
		self.menubar.addAction(self.menuOptions.menuAction())
		self.menubar.addAction(self.menuSobre.menuAction())

		self.setCentralWidget(self.centralwidget) 
		
		# Chama função para finalizar interface
		self.completeUi()
		
		# Conecta slots a todos objetos filhos da janela principal
		# permitindo que eles emitam sinais
		QtCore.QMetaObject.connectSlotsByName(self)

	# MENU - Seta triggers do menu, nomenclatura e atalhos da janela
	def completeUi(self):
		
		# Variável que ajuda a definir o escopo de objeto referenciado
		_translate = QtCore.QCoreApplication.translate
		
		# Seta place holde da caixa de mensagem, para que o usuário digite
		self.msg.setPlaceholderText(QtCore.QCoreApplication.translate("self", u"Escreva uma mensagem", None))

		# Setando títulos das abas do menu e das labels da janela
		self.setWindowTitle(_translate("MainWindow", "Abachat App"))
		self.titulo.setText(_translate("MainWindow", "Abachat"))
		self.menuOptions.setTitle(_translate("MainWindow", "Menu"))
		self.actionNova_Conex_o.setText(_translate("MainWindow", "Nova Conexão"))
		self.actionLimpar.setText(_translate("MainWindow", "Limpar Chat"))
		self.actionQuit.setText(_translate("MainWindow", "Quit"))
		self.menuSobre.setTitle(_translate("MainWindow", "Sobre"))
		self.label.setText(_translate("MainWindow", "Usuários Conectados"))
		self.sendBtn.setText(_translate("MainWindow", "Enviar"))

		# Setando atalhos das abas
		self.actionNova_Conex_o.setShortcut(_translate("MainWindow", "Ctrl+N"))
		self.actionLimpar.setShortcut(_translate("MainWindow", "Escape"))
		self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))

		# Definindo rotinas (triggers) para quando uma das abas for acessada
		self.actionQuit.triggered.connect(self.close)
		self.actionLimpar.triggered.connect(self.clearChat)

	# Detecta a tecla Enter para enviar mensagem
	def keyPressEvent(self, event):
		# Se um tecla for precionada ela é salva
		key = event.key()
		# Se for a tecla enter chama-se a função de envio
		if key == QtCore.Qt.Key_Return:
			self.send()
	
	# Capta o evendo de fechamento da janela para encerrar conexão
	def closeEvent(self, event):
		try:
			# Se o evento de fechamento for chamado
			if(event):
				# Envia mensagem ao servidor para desconectar
				message, send_length = encodeMsg(DISCONNECT_MESSAGE)
				self.client.send(send_length)
				self.client.send(message)
				# Chama rotina para encerrar o cliente
				self.disconnect()
				
		except:
			# Se der erro significa que a desconexão já foi feita
			pass	

	# Adiciona mensagem ao Text Browser do chat
	def chatUpdate(self, str):
		self.chat.append(str)

	# Limpando o chat
	def clearChat(self):
		# Reseta o Text Browser do chat
		self.chat.clear()

	# Atualizando lista de usuários conectados
	def listUpdate(self, str):
		# Se o sinal emitido for vazio reseta a lista
		if(str == ''):
			self.userList.clear()
		else:
		# Se não adiciona o nome enviado
			self.userList.append(str)


# FUNÇÕES DE SUPORTE
def encodeMsg(msg):
    message = str(msg).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    return message, send_length


if __name__ == "__main__":
	createMainWindow("User", ADDR, PORT)