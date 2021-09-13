from client import createClient
from mainWindow import createMainWindow

import threading
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def createLogWindow():
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    win = LogWindow()
    win.setupUi(Form)
    Form.show()
    app.exec_()
    return (win.name, str(win.addr), win.prt)


class LogWindow(object):

    def setupUi(self, Form):
        
        # WINDOW
        self.win = Form
        if not Form.objectName():
            Form.setObjectName(u"Form")
        
        Form.resize(470, 602)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setStyleSheet(u"background-color: qlineargradient(spread:repeat, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(223, 144, 138, 255), stop:0.971591 rgba(57, 255, 136, 255));")
        
        # FONTES
        font = QFont()
        font.setFamily(u"Calibri")
        font.setPointSize(14)
        font1 = QFont()
        font1.setPointSize(14)
        font2 = QFont()
        font2.setFamily(u"Calibri")
        font2.setPointSize(12)
        font3 = QFont()
        font3.setFamily(u"Calibri")
        font3.setPointSize(18)
        font4 = QFont()
        font4.setFamily(u"Ink Free")
        font4.setPointSize(30)
        font4.setBold(True)
        font4.setWeight(75)

        # MAIN GRID
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        
        # LOGO
        self.logo = QLabel(Form)
        self.logo.setObjectName(u"logo")
        self.logo.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy1)
        self.logo.setMaximumSize(QSize(200, 200))
        self.logo.setLayoutDirection(Qt.LeftToRight)
        self.logo.setAutoFillBackground(False)
        self.logo.setLocale(QLocale(QLocale.Portuguese, QLocale.Brazil))
        self.logo.setFrameShape(QFrame.NoFrame)
        self.logo.setFrameShadow(QFrame.Plain)
        self.logo.setPixmap(QPixmap(u"img\\logo.png"))        
        self.logo.setScaledContents(True)
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setWordWrap(False)
        self.logo.setStyleSheet(u"background-color: qlineargradient(spread:repeat, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(255, 255, 255, 0));")
        self.gridLayout.addWidget(self.logo, 1, 1, 1, 1, Qt.AlignHCenter)

        # TÍTULO
        self.titulo = QLabel(Form)
        self.titulo.setObjectName(u"titulo")
        self.titulo.setMaximumSize(QSize(16777215, 40))
        self.titulo.setFont(font4)
        self.titulo.setLayoutDirection(Qt.LeftToRight)
        self.titulo.setFrameShape(QFrame.NoFrame)
        self.titulo.setFrameShadow(QFrame.Plain)
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet(u"background-color: qlineargradient(spread:repeat, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(255, 255, 255, 0));\n color: white;")
        self.gridLayout.addWidget(self.titulo, 2, 1, 1, 1)

        # LABEL LOGIN
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 40))
        self.label_5.setFont(font3)
        self.label_5.setAlignment(Qt.AlignCenter)
        self.label_5.setStyleSheet(u"background-color: qlineargradient(spread:repeat, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(255, 255, 255, 0));\n color: white;")
        self.gridLayout.addWidget(self.label_5, 3, 1, 1, 1)

        # LABEL USERNAME
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"background-color: qlineargradient(spread:repeat, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(255, 255, 255, 0));\n color: white;")
        self.gridLayout.addWidget(self.label_2, 4, 1, 1, 1)

        # INPUT USERNAME
        self.username = QLineEdit(Form)
        self.username.setObjectName(u"username")
        self.username.setMaximumSize(QSize(400, 31))
        self.username.setFont(font2)
        self.username.setFocus()
        self.username.setStyleSheet(u"background-color: white;")
        self.gridLayout.addWidget(self.username, 6, 1, 1, 1)

        # LABEL ENDEREÇO
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"background-color: qlineargradient(spread:repeat, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(255, 255, 255, 0));\n color: white;")
        self.gridLayout.addWidget(self.label_3, 7, 1, 1, 1)

        # INPUT ENDEREÇO
        self.adress = QLineEdit(Form)
        self.adress.setObjectName(u"adress")
        self.adress.setMaximumSize(QSize(400, 31))
        self.adress.setFont(font2)
        self.adress.setStyleSheet(u"background-color: white")
        self.gridLayout.addWidget(self.adress, 9, 1, 1, 1)

        # LABEL PORTA
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"background-color: qlineargradient(spread:repeat, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(255, 255, 255, 0));\n color: white;")
        self.gridLayout.addWidget(self.label_4, 10, 1, 1, 1)

        # INPUT PORTA
        self.port = QLineEdit(Form)
        self.port.setObjectName(u"port")
        self.port.setMaximumSize(QSize(400, 31))
        self.port.setFont(font2)
        self.port.setStyleSheet(u"background-color: white")
        self.gridLayout.addWidget(self.port, 11, 1, 1, 1)

        # LABEL ERRO
        self.error = QLabel(Form)
        self.error.setObjectName(u"errorLabel")
        self.error.setFont(font)
        self.error.setStyleSheet(u"background-color: qlineargradient(spread:repeat, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(255, 255, 255, 0));\n color: Red;")
        self.gridLayout.addWidget(self.error, 12, 1, 1, 1)

        # BUTTON ENTRAR
        self.entrar = QPushButton(Form)
        self.entrar.setObjectName(u"entrar")
        self.entrar.setSizeIncrement(QSize(0, 0))
        self.entrar.setBaseSize(QSize(0, 0))
        self.entrar.setFont(font1)
        self.entrar.setCursor(QCursor(Qt.PointingHandCursor))
        # self.entrar.setStyleSheet(u"background-color: qlineargradient(spread:repeat, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(255, 255, 255, 0));\n color: white;")
        #self.entrar.setStyleSheet(u"background-color: rgb(85, 170, 0);")
        self.entrar.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 255, 255, 0));\n color: white;")
        self.gridLayout.addWidget(self.entrar, 13, 1, 1, 1)
        self.entrar.clicked.connect(self.login)

        # SPACERS
        # self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.gridLayout.addItem(self.verticalSpacer_3, 12, 1, 1, 1)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(self.verticalSpacer_2, 0, 1, 1, 1)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(self.verticalSpacer, 14, 1, 1, 1)
        self.completeUi(Form)

        QMetaObject.connectSlotsByName(Form)

    def completeUi(self, Form):
        # Nomes
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Abachat", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Porta", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Endere\u00e7o", None))
        self.entrar.setText(QCoreApplication.translate("Form", u"Entrar", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Login", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Username", None))
        self.titulo.setText(QCoreApplication.translate("Form", u"Abachat", None))
        self.logo.setText("")

        # Place Holders
        self.username.setPlaceholderText(QCoreApplication.translate("Form", u"Joana", None))
        self.adress.setPlaceholderText(QCoreApplication.translate("Form", u"123.456.7.890", None))
        self.port.setPlaceholderText(QCoreApplication.translate("Form", u"5000", None))

    def login(self, Form):
        self.name = self.username.text()
        self.addr = self.adress.text()
        self.prt = self.port.text()

        if len(self.name)==0:
            self.name = 'Test'
        if len(self.addr)==0:
            self.addr = '192.168.1.113'
        if len(self.prt)==0:
            self.prt = '5000'

        # if len(name) == 0 or len(address) == 0 or len(port) == 0:
        #     self.error.setText(QCoreApplication.translate("Form", u"Por favor, preencha todos os campos!", None))
        # else:

        # # Iniciando Cliente
        # Client = threading.Thread(target=createClient, args=(name, address, port))
        # Client.start()

        # # Iniciando Janela Principal
        # Chat = threading.Thread(target=createMainWindow, args=(name, address, port))
        # Chat.start()

        # Encerrando janela de login
        self.win.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    win = LogWindow()
    win.setupUi(Form)
    Form.show()
    app.exec_()
