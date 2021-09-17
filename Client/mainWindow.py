import sys
import socket
import threading
from config import*
from client import Client, encodeMsg
from main import start

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextBrowser


# Classe para definir sinais enviados pela thread_recv a janela principal 
class MySignal(QtCore.QObject):
	listUser = QtCore.pyqtSignal(str) # ação sobre lista de usuários conectados
	chatLabel = QtCore.pyqtSignal(str) # ação sobre text browser do chat
	
# Janela principal do cliente
class MainWindow(QMainWindow):

	def __init__(self, username, address, port):
		# Inicializando construtor da janela
		super(QMainWindow, self).__init__()

		
		self.signal = MySignal()
		self.signal.listUser.connect(self.listUpdate)
		self.signal.chatLabel.connect(self.chatUpdate)

        # Iniciando 
		self.client = Client(username, address, port, self)

		# Carregando componentes da interface
		self.setupUi()

	# Cria elementos do Layout e 
	def setupUi(self):

		# WINDOW
		self.setObjectName("MainWindow")
		self.resize(850, 600)
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
		self.chat.setMinimumSize(QtCore.QSize(500, 500))
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
		self.sendBtn.clicked.connect(self.client.sendMsg)

		# MENU BAR
		self.menubar = QtWidgets.QMenuBar(self)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 783, 21))
		self.menubar.setStyleSheet("background-color: rgb(255, 255, 255);")
		self.menubar.setObjectName("menubar")
		self.setMenuBar(self.menubar)
		self.menuOptions = QtWidgets.QMenu(self.menubar)
		self.menuOptions.setObjectName("menuOptions")
		self.actionChangeName = QtWidgets.QAction(self) # cria menu
		self.actionChangeName.setObjectName("actionChangeName")
		self.actionLimpar = QtWidgets.QAction(self)
		self.actionLimpar.setObjectName("actionLimpar")
		self.actionEncerrarConn = QtWidgets.QAction(self)
		self.actionEncerrarConn.setObjectName("closeConn")
		self.actionQuit = QtWidgets.QAction(self)
		self.actionQuit.setObjectName("actionQuit")
		self.menuSobre = QtWidgets.QMenu(self.menubar)
		self.menuSobre.setObjectName("menuSobre")

		# Define ações e objetos ao acessar a barra de menu
		self.menuOptions.addAction(self.actionChangeName)
		self.menuOptions.addAction(self.actionEncerrarConn)
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
		self.actionChangeName.setText(_translate("MainWindow", "Alterar Nome"))
		self.actionEncerrarConn.setText(_translate("MainWindow", "Encerrar Conexão"))
		self.actionLimpar.setText(_translate("MainWindow", "Limpar Chat"))
		self.actionQuit.setText(_translate("MainWindow", "Quit"))
		self.menuSobre.setTitle(_translate("MainWindow", "Sobre"))
		self.label.setText(_translate("MainWindow", "Usuários Conectados"))
		self.sendBtn.setText(_translate("MainWindow", "Enviar"))

		# Setando atalhos das abas
		self.actionChangeName.setShortcut(_translate("MainWindow", "Ctrl+N"))
		self.actionEncerrarConn.setShortcut(_translate("MainWindow", "Ctrl+F"))
		self.actionLimpar.setShortcut(_translate("MainWindow", "Escape"))
		self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))

		# Definindo rotinas (triggers) para quando uma das abas for acessada
		self.actionChangeName.triggered.connect(self.changeName)
		self.actionEncerrarConn.triggered.connect(self.client.disconnect)
		self.actionLimpar.triggered.connect(self.chat.clear)
		self.actionQuit.triggered.connect(self.closeEvent)
		self.menuSobre.triggered.connect(self.sobreWin)


	def changeName(self):
		pass


	def sobreWin(self):
		pass

	# Detecta a tecla Enter para enviar mensagem
	def keyPressEvent(self, event):
		# Se um tecla for precionada ela é salva
		key = event.key()
		# Se for a tecla enter chama-se a função de envio
		if key == QtCore.Qt.Key_Return:
			msg = self.msg.text()
			if(msg):
				self.client.sendMsg(msg)
				self.msg.setText('')
			
			else:
				return
	
	# Capta o evendo de fechamento da janela para encerrar conexão
	def closeEvent(self, event):
			# Se o evento de fechamento for chamado e cliente estiver online
			if(self.client.online):
				# Chama rotina para encerrar o cliente
				self.client.disconnect()
			self.close()

	# Adiciona mensagem ao Text Browser do chat
	def chatUpdate(self, str):
		self.chat.append(str)

	# Atualizando lista de usuários conectados
	def listUpdate(self, str):
		# Se o sinal emitido for vazio reseta a lista
		if(str == ''):
			self.userList.clear()
		else:
		# Se não adiciona o nome enviado
			self.userList.append(str)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = MainWindow("User", ADDR, PORT)

	win.show()
	app.exec_()