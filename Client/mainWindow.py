from client import Client, DISCONNECT_MESSAGE

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

#Variáveis de teste
USERNAME = "Test"
ADDR = "localhost"
PORT = 5001

def createMainWindow(name, address, port):

	app = QApplication(sys.argv)
	win = MainWindow(name, address, port)
	win.show()

	app.exec_()


class MainWindow(QMainWindow):

	def __init__(self, name, address, port):
		# Inicializando construtor da janela
		super(QMainWindow, self).__init__()
        
		# Carregando componentes da interface
		self.setupUi()

		# Inicializando funções de comunicação do cliente
		self.client = Cli


	def closeEvent(self, event):
		self.client.sendMsg(DISCONNECT_MESSAGE)
		#event.accept()


	def keyPressEvent(self, event):
		key = event.key()
		if key == QtCore.Qt.Key_Return:
			self.send()


	def send(self):
		msg = self.msg.text()
		if(msg == ''):
			return
		else:
			self.client.sendMsg(msg)
			self.chat.append(f"Você: {msg}")
			self.msg.setText('')
			#print(msg)


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

		self.actionNova_Conex_o = QtWidgets.QAction(self)
		self.actionNova_Conex_o.setObjectName("actionNova_Conex_o")
		self.menuOptions.addAction(self.actionNova_Conex_o)
		self.menuOptions.addAction(self.actionLimpar)
		self.menuOptions.addSeparator()
		self.menuOptions.addAction(self.actionQuit)
		self.menubar.addAction(self.menuOptions.menuAction())
		self.menubar.addAction(self.menuSobre.menuAction())

		self.setCentralWidget(self.centralwidget) 
		
		self.completeUi()
		
		QtCore.QMetaObject.connectSlotsByName(self)
	

	def completeUi(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle(_translate("MainWindow", "Abachat App"))
		self.label.setText(_translate("MainWindow", "Usuários Conectados"))
		self.sendBtn.setText(_translate("MainWindow", "Enviar"))
		self.titulo.setText(_translate("MainWindow", "Abachat"))
		self.msg.setPlaceholderText(QtCore.QCoreApplication.translate("self", u"Escreva uma mensagem", None))
		
		# Menu
		self.menuOptions.setTitle(_translate("MainWindow", "Menu"))
		self.menuSobre.setTitle(_translate("MainWindow", "Sobre"))
		self.actionQuit.setText(_translate("MainWindow", "Quit"))
		self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
		#self.actionQuit.triggered.connect(self.close())
		self.actionLimpar.setText(_translate("MainWindow", "Limpar Chat"))
		self.actionLimpar.setShortcut(_translate("MainWindow", "Escape"))
		self.actionLimpar.triggered.connect(self.clearChat)
		self.actionNova_Conex_o.setText(_translate("MainWindow", "Nova Conexão"))
		self.actionNova_Conex_o.setShortcut(_translate("MainWindow", "Ctrl+N"))
		
	def clearChat(self):
		self.chat.clear()


if __name__ == "__main__":
	createMainWindow(USERNAME, ADDR, PORT)