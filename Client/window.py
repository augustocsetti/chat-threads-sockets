import sys
from config import*
from windowClient import Client

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

# Classe de sinais da janela do cliente 
class MySignal(QtCore.QObject):
	
	# Define sinais enviados pela thread_recv a janela principal
	listUser = QtCore.pyqtSignal(str) # ação sobre lista de usuários conectados
	chatLabel = QtCore.pyqtSignal(str) # ação sobre text browser do chat
	

# Classe da janela principal do cliente
# - cria interface principal do chat
# 	(chat, lista de usuários, caixa de texto, menu e labels)
# - gerencia lista de usuários conectados
# - mostra mensagens do servidor e dos clientes
# - cria interface e gerencia troca de username
# - cria janela sobre

class MainWindow(QMainWindow):

	# Inicializa janela principal
	def __init__(self, username, address, port):

		# Inicializando construtor da janela
		super(QMainWindow, self).__init__()

		# Define sinais e slots para mensagens do worker
		self.signal = MySignal()
		self.signal.listUser.connect(self.listUpdate)
		self.signal.chatLabel.connect(self.chatUpdate)

        # Iniciando worker e enviando parametros para conexão
		self.client = Client(username, address, port, self)

		# Carregando componentes da interface
		self.setupUi()

	# Cria elementos do Layout
	def setupUi(self):

		# WINDOW
		self.setWindowIcon(QtGui.QIcon(u"img\\miniLogo.png"))
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
		self.logo.setMaximumSize(QtCore.QSize(200, 200))
		self.logo.setSizeIncrement(QtCore.QSize(400, 400))
		self.logo.setBaseSize(QtCore.QSize(150, 151))
		self.logo.setStyleSheet("background-color: qlineargradient(spread:repeat, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(255, 255, 255, 0));")
		self.logo.setText("")
		self.logo.setPixmap(QtGui.QPixmap(u"img\\logo.png"))
		self.logo.setAlignment(QtCore.Qt.AlignCenter)
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

		# SPACERS
		spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem, 5, 2, 1, 1)
		spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem1, 4, 1, 1, 1)

		# LISTA USUÁRIOS CONECTADOS
		self.userList = QtWidgets.QTextBrowser(self.centralwidget)
		self.userList.setMinimumSize(QtCore.QSize(200, 100))
		self.userList.setMaximumSize(QtCore.QSize(250, 500))
		font = QtGui.QFont()
		font.setFamily("Calibri")
		font.setPointSize(12)
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
		self.chat.setMinimumSize(QtCore.QSize(300, 400))
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
		self.sendBtn.clicked.connect(self.newMsg)

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
		self.menuSobre = QtWidgets.QAction(self.menubar)
		self.menuSobre.setObjectName("menuSobre")

		# Define ações ao acessar a barra de menu
		self.menuOptions.addAction(self.actionChangeName)
		self.menuOptions.addAction(self.actionEncerrarConn)
		self.menuOptions.addAction(self.actionLimpar)
		self.menuOptions.addSeparator() # separador
		self.menuOptions.addAction(self.actionQuit)
		self.menubar.addAction(self.menuOptions.menuAction())
		self.menubar.addAction(self.menuSobre)

		# Posiciona grid na janela
		self.setCentralWidget(self.centralwidget) 
		
		# Chama função para finalizar interface
		self.translateUi()
		
		# Conecta slots a todos objetos filhos da janela principal
		# permitindo que eles emitam sinais
		QtCore.QMetaObject.connectSlotsByName(self)

	# Seta triggers do menu, nomeia elementos e cria atalhos na janela
	def translateUi(self):
		
		# Variável que ajuda a definir o escopo de objeto referenciado
		_translate = QtCore.QCoreApplication.translate
		
		# Seta placeholder da caixa de mensagem, para que o usuário digite
		self.msg.setPlaceholderText(QtCore.QCoreApplication.translate("self", u"Escreva uma mensagem", None))

		# Setando títulos das abas do menu e das labels da janela
		self.setWindowTitle(_translate("MainWindow", "Abachat App"))
		self.titulo.setText(_translate("MainWindow", "Abachat"))
		self.menuOptions.setTitle(_translate("MainWindow", "Menu"))
		self.actionChangeName.setText(_translate("MainWindow", "Alterar Nome"))
		self.actionEncerrarConn.setText(_translate("MainWindow", "Encerrar Conexão"))
		self.actionLimpar.setText(_translate("MainWindow", "Limpar Chat"))
		self.actionQuit.setText(_translate("MainWindow", "Quit"))
		self.menuSobre.setText(_translate("MainWindow", "Sobre"))
		self.label.setText(_translate("MainWindow", "Usuários Conectados"))
		self.sendBtn.setText(_translate("MainWindow", "Enviar"))

		# Setando atalhos das abas
		self.actionChangeName.setShortcut(_translate("MainWindow", "Ctrl+N"))
		self.actionEncerrarConn.setShortcut(_translate("MainWindow", "Ctrl+F"))
		self.actionLimpar.setShortcut(_translate("MainWindow", "Escape"))
		self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))

		# Definindo rotinas (triggers) para quando uma das abas for acessada
		self.actionChangeName.triggered.connect(self.changeNameWin)
		self.actionEncerrarConn.triggered.connect(self.client.disconnect)
		self.actionLimpar.triggered.connect(self.chat.clear)
		self.actionQuit.triggered.connect(self.closeEvent)
		self.menuSobre.triggered.connect(self.sobreWin)

	# Envia mensagem
	def newMsg(self):

		msg = self.msg.text() # recebe texto da caixa de msgm
		if(msg): # se houver alguma coisa

			# Chama função de envio de nova msgm no worker 
			self.client.sendMsg(msg, NEW_MESSAGE) # envia TAG de nova msgm
			self.msg.setText('') # reseta texto

		return

	# Troca de username - JANELA
	def changeNameWin(self):

		# WINDOW NAME inicializando
		self.nameWin = QMainWindow()
		self.nameWin.setWindowIcon(QtGui.QIcon(u"img\\miniLogo.png"))
		self.nameWin.setWindowTitle("Novo nome")
		self.nameWin.setStyleSheet("background-color: qlineargradient(spread:repeat, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(223, 144, 138, 255), stop:0.971591 rgba(57, 255, 136, 255));")
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.nameWin.sizePolicy().hasHeightForWidth())
		self.nameWin.setSizePolicy(sizePolicy)
		self.nameWin.setMinimumSize(QtCore.QSize(250, 140))
		self.nameWin.setMaximumSize(QtCore.QSize(250, 140))

		# LINE EDIT P/ NOVO USERNAME
		self.newName = QtWidgets.QLineEdit(self.nameWin)
		self.newName.setGeometry(QtCore.QRect(30, 30, 181, 31))
		font = QtGui.QFont()
		font.setFamily("Calibri")
		font.setPointSize(12)
		self.newName.setFont(font)
		self.newName.setStyleSheet("background-color: rgb(255, 255, 255);\n"
		"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 115));\n"
		"color: rgb(135, 97, 88);")

		# BOTÃO DE ENVIO
		self.sendName = QtWidgets.QPushButton(self.nameWin)
		self.sendName.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.sendName.setMaximumSize(QtCore.QSize(80, 40))
		self.sendName.setGeometry(QtCore.QRect(30, 90, 75, 23))
		self.sendName.setText("Aceitar")
		self.sendName.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 0));\n")

		# BOTÃO DE CANCELAMENTO
		self.cancelName = QtWidgets.QPushButton(self.nameWin)
		self.cancelName.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
		self.cancelName.setGeometry(QtCore.QRect(130, 90, 75, 23))
		self.cancelName.setText("Cancelar")
		self.cancelName.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 0));\n")

		# SINAIS - envio e cancelamento
		self.sendName.clicked.connect(self.changeName)
		self.cancelName.clicked.connect(self.nameWin.close)

		# Mostrar janela
		self.nameWin.show()

	# Troca de username - FUNÇÃO
	def changeName(self):
		name = self.newName.text()
		if(name):
			self.client.sendMsg(name, CHANGE_NAME)
			self.nameWin.close()
		return

	# Sobre - JANELA
	def sobreWin(self):

		# WINDOW inicialização
		self.sobreWin = QMainWindow()
		self.sobreWin.setWindowTitle("Sobre")
		self.sobreWin.setWindowIcon(QtGui.QIcon(u"img\\miniLogo.png"))
		self.sobreWin.setStyleSheet("background-color: qlineargradient(spread:repeat, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(223, 144, 138, 255), stop:0.971591 rgba(57, 255, 136, 255));")
		self.sobreWin.setMinimumSize(QtCore.QSize(240, 300))
		self.sobreWin.setMaximumSize(QtCore.QSize(240, 300))

		# LABEL texto
		self.label = QtWidgets.QLabel(self.sobreWin)
		self.label.setGeometry(QtCore.QRect(0, 0, 240, 300))
		font = QtGui.QFont()
		font.setFamily("Calibri")
		font.setPointSize(12)
		self.label.setFont(font)
		self.label.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 0));\n"
		"color: rgb(255, 255, 255);")
		self.label.setText(u"<html><head/><body><p align=\"center\">Projeto desenvolvido por:</p><p align=\"center\"><br/></p><p align=\"center\">Augusto Cardoso Setti</p><p align=\"center\"><br/><br/></p><p align=\"center\">2021</p><p align=\"center\">Todos os direitos Reservados</p></body></html>")
		
		# Mostra janela
		self.sobreWin.show()

	# Adiciona mensagem ao Text Browser do chat
	def chatUpdate(self, str):

		# Adiciona mensagem ao text browser do chat
		self.chat.append(str)

	# Atualizando lista de usuários conectados
	def listUpdate(self, str):

		# Se o sinal recebido for vazio reseta a lista
		if(str == ''):
			self.userList.clear()
		
		# Se não adiciona o nome enviado
		else:
			self.userList.append(str)

	# Detecta a tecla Enter para enviar mensagem
	def keyPressEvent(self, event):

		# Se um tecla for precionada ela é salva
		key = event.key()
		# Se for a tecla enter chama-se a função de envio
		if key == QtCore.Qt.Key_Return:
			self.sendBtn.click()

	# Capta o evento de fechamento da janela para encerrar conexão
	def closeEvent(self, event):

			# Se o evento de fechamento for chamado e cliente estiver online
			if(self.client.online):
				# Chama rotina para encerrar o cliente
				self.client.disconnect()
			self.close() # fecha janela


if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = MainWindow("User", ADDR, PORT)

	win.show()
	app.exec_()