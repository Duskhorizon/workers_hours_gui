

import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from baza import connect
from functools import partial


class Ui_AgentWindow(object):
    def setupUi(self, AgentWindow):
        AgentWindow.setObjectName("AgentWindow")
        AgentWindow.resize(560, 121)
        self.centralwidget = QtWidgets.QWidget(AgentWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 30, 161, 32))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("Imie")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(190, 30, 171, 32))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("Nazwisko")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(400, 20, 99, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("DODAJ")
        self.pushButton.clicked.connect(self.insertAgent)
        AgentWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(AgentWindow)
        self.statusbar.setObjectName("statusbar")
        AgentWindow.setStatusBar(self.statusbar)
        self.retranslateUi(AgentWindow)
        QtCore.QMetaObject.connectSlotsByName(AgentWindow)

    def retranslateUi(self, AgentWindow):
        _translate = QtCore.QCoreApplication.translate
        AgentWindow.setWindowTitle(_translate("AgentWindow", "Dodawanie Agentów"))
        self.pushButton.setText(_translate("AgentWindow", "DODAJ"))

    def insertAgent(self):
        conn = sqlite3.connect("baza.db")
        cur = conn.cursor()
        imie = self.lineEdit.text()
        nazwisko = self.lineEdit_2.text()
        cur.execute("INSERT INTO agent (imie,nazwisko) VALUES (?,?)",(imie,nazwisko))
        conn.commit()
        conn.close
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AgentWindow = QtWidgets.QMainWindow()
    ui = Ui_AgentWindow()
    ui.setupUi(AgentWindow)
    AgentWindow.show()
    sys.exit(app.exec_())
