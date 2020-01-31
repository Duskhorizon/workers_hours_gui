
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3


class Ui_AgentTableForm(object):
    def setupUi(self, Form,agent,miesiac):
        print(agent)
        print(miesiac)
        Form.setObjectName("Form")
        Form.resize(942, 709)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 60, 921, 641))
        self.tableWidget.setObjectName("tableWidget")
        conn = sqlite3.connect("baza.db")
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT nazwa FROM wpisy INNER JOIN projekt ON projekt.id = wpisy.wpisprojekt WHERE wpisagent = ? AND wpismiesiac = ?",(agent,miesiac,))
        projekty = []
        for row in cur:
            projekty.append(row[0])
        header_labels = ['Projekt', 'Liczba godzin',]         
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(len(projekty)+1)
        for projekt in projekty:
            inx = projekty.index(projekt)
            self.tableWidget.setItem(inx,0,QtWidgets.QTableWidgetItem(str(projekt)))
            cur.execute("SELECT id FROM projekt WHERE nazwa = ?",(projekt,))
            idprojektu = cur.fetchone()[0]       
            cur.execute("SELECT SUM(godziny) from wpisy WHERE wpisprojekt = ? AND wpismiesiac = ? AND wpisagent= ?",(idprojektu,miesiac,agent))
            self.tableWidget.setItem(inx,1,QtWidgets.QTableWidgetItem(str(cur.fetchone()[0])))
        self.tableWidget.setItem(inx+1,0,QtWidgets.QTableWidgetItem("SUMA:"))
        cur.execute("SELECT SUM(godziny) FROM wpisy WHERE wpismiesiac =? AND wpisagent=?",(miesiac,agent))
        self.tableWidget.setItem(inx+1,1,QtWidgets.QTableWidgetItem(str(cur.fetchone()[0])))        
        self.tableWidget.setHorizontalHeaderLabels(header_labels)                
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 1351, 41))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.retranslateUi(Form)
        cur.execute("SELECT imie, nazwisko FROM agent WHERE id=?",(agent,))
        dane = cur.fetchone()
        cur.execute("SELECT nazwa FROM miesiac WHERE id=?",(miesiac,))
        label_miesiac = cur.fetchone()[0]
        self.label.setText("Godziny agenta %s %s w miesiącu %s z podziałem na projekty :" % (dane[0],dane[1],label_miesiac))        
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Tabela Agent"))
      






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_AgentTableForm()
    ui.setupUi(Form,3,3)
    Form.show()
    sys.exit(app.exec_())
