

import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from baza import connect
from functools import partial


class Ui_ProjektWindow(object):
    def setupUi(self, ProjektWindow):
        ProjektWindow.setObjectName("ProjektWindow")
        ProjektWindow.resize(560, 121)
        self.centralwidget = QtWidgets.QWidget(ProjektWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 30, 161, 32))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("Projekt")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(400, 20, 99, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("DODAJ")
        self.pushButton.clicked.connect(self.insertProjekt)
        ProjektWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ProjektWindow)
        self.statusbar.setObjectName("statusbar")
        ProjektWindow.setStatusBar(self.statusbar)
        self.retranslateUi(ProjektWindow)
        QtCore.QMetaObject.connectSlotsByName(ProjektWindow)

    def retranslateUi(self, ProjektWindow):
        _translate = QtCore.QCoreApplication.translate
        ProjektWindow.setWindowTitle(_translate("ProjektWindow", "Dodawanie Projektów"))
        self.pushButton.setText(_translate("ProjektWindow", "DODAJ"))

    def insertProjekt(self):
        conn = sqlite3.connect("baza.db")
        cur = conn.cursor()
        projekt = self.lineEdit.text()
        cur.execute("INSERT INTO projekt (nazwa) VALUES (?)",(projekt,))
        conn.commit()
        conn.close
        self.lineEdit.setText("")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ProjektWindow = QtWidgets.QMainWindow()
    ui = Ui_ProjektWindow()
    ui.setupUi(ProjektWindow)
    ProjektWindow.show()
    sys.exit(app.exec_())
