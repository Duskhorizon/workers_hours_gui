

from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import pandas
from functools import partial
from baza import connect
from agent import Ui_AgentWindow
from projekt import Ui_ProjektWindow
from agentable import Ui_AgentTableForm




class Ui_MainWindow(object):

    def updateAgentTable(self):
        agent = self.agentcomboBox.currentData()
        miesiac = self.miesiaccomboBox.currentData()
        rok = self.rokcomboBox.currentText()
        projekt = self.projektcomboBox.currentData()
        if agent is not None and miesiac is not None:
            if agent > 0 and miesiac > 0:
                conn = sqlite3.connect("baza.db")
                cur = conn.cursor()
                cur.execute("SELECT DISTINCT nazwa FROM wpisy INNER JOIN projekt ON projekt.id = wpisy.wpisprojekt WHERE wpisagent = ? AND wpismiesiac = ? AND rok = ?",(agent,miesiac,rok))
                projekty = []
                for row in cur:
                    projekty.append(row[0])
                header_labels = ['Projekt', 'Godziny',]
                if len(projekty) > 0:       
                    self.tableWidget1.setColumnCount(2)
                    self.tableWidget1.setRowCount(len(projekty)+1)
                    for projekt in projekty:
                        inx = projekty.index(projekt)
                        self.tableWidget1.setItem(inx,0,QtWidgets.QTableWidgetItem(str(projekt)))
                        cur.execute("SELECT id FROM projekt WHERE nazwa = ?",(projekt,))
                        idprojektu = cur.fetchone()[0]       
                        cur.execute("SELECT SUM(godziny) from wpisy WHERE wpisprojekt = ? AND wpismiesiac = ? AND wpisagent= ? AND rok = ?",(idprojektu,miesiac,agent,rok))
                        self.tableWidget1.setItem(inx,1,QtWidgets.QTableWidgetItem(str(cur.fetchone()[0])))
                    self.tableWidget1.setItem(inx+1,0,QtWidgets.QTableWidgetItem("SUMA:"))
                    self.tableWidget1.item(inx+1,0).setBackground(QtGui.QColor(100,100,150))
                    cur.execute("SELECT SUM(godziny) FROM wpisy WHERE wpismiesiac =? AND wpisagent=? AND rok=?",(miesiac,agent,rok))
                    self.tableWidget1.setItem(inx+1,1,QtWidgets.QTableWidgetItem(str(cur.fetchone()[0])))
                    self.tableWidget1.item(inx+1,1).setBackground(QtGui.QColor(100,100,150)) 
                else:
                    self.tableWidget1.setColumnCount(1)
                    self.tableWidget1.setRowCount(1)
                    self.tableWidget1.setItem(0,0,QtWidgets.QTableWidgetItem("BRAK"))
                conn.close
            self.tableWidget1.setHorizontalHeaderLabels(header_labels)
            agentlabel = self.agentcomboBox.currentText()
            projektlabel = self.projektcomboBox.currentText()
            miesiaclabel = self.miesiaccomboBox.currentText()
            self.label1.setText("Godziny agenta %s w miesiącu %s"%(agentlabel,miesiaclabel))
        agent = self.agentcomboBox.currentData()
        miesiac = self.miesiaccomboBox.currentData()
        rok = self.rokcomboBox.currentText()
        projekt = self.projektcomboBox.currentData()            
        if projekt is not None and miesiac is not None:
            if projekt > 0 and miesiac > 0:
                conn = sqlite3.connect("baza.db")
                cur = conn.cursor()
                cur.execute("SELECT DISTINCT nazwisko FROM wpisy INNER JOIN agent ON agent.id = wpisy.wpisagent WHERE wpisprojekt = ? AND wpismiesiac = ? AND rok = ?",(projekt,miesiac,rok))
                agenci = []
                for row in cur:
                    agenci.append(row[0])
                header_labels = ['Agent', 'Godziny',]
                if len(agenci) > 0:       
                    self.tableWidget2.setColumnCount(2)
                    self.tableWidget2.setRowCount(len(agenci)+1)
                    for agent in agenci:
                        inx = agenci.index(agent)
                        self.tableWidget2.setItem(inx,0,QtWidgets.QTableWidgetItem(str(agent)))
                        cur.execute("SELECT id FROM agent WHERE nazwisko = ?",(agent,))
                        idagenta = cur.fetchone()[0]       
                        cur.execute("SELECT SUM(godziny) from wpisy WHERE wpisagent = ? AND wpismiesiac = ? AND wpisprojekt= ? AND rok = ?",(idagenta,miesiac,projekt,rok))
                        self.tableWidget2.setItem(inx,1,QtWidgets.QTableWidgetItem(str(cur.fetchone()[0])))
                    self.tableWidget2.setItem(inx+1,0,QtWidgets.QTableWidgetItem("SUMA:"))
                    self.tableWidget2.item(inx+1,0).setBackground(QtGui.QColor(100,100,150))
                    cur.execute("SELECT SUM(godziny) FROM wpisy WHERE wpismiesiac =? AND wpisprojekt=? AND rok=?",(miesiac,projekt,rok))
                    self.tableWidget2.setItem(inx+1,1,QtWidgets.QTableWidgetItem(str(cur.fetchone()[0])))
                    self.tableWidget2.item(inx+1,1).setBackground(QtGui.QColor(100,100,150)) 
                else:
                    self.tableWidget2.setColumnCount(1)
                    self.tableWidget2.setRowCount(1)
                    self.tableWidget2.setItem(0,0,QtWidgets.QTableWidgetItem("BRAK"))
                conn.close
            self.tableWidget2.setHorizontalHeaderLabels(header_labels)
            agentlabel = self.agentcomboBox.currentText()
            projektlabel = self.projektcomboBox.currentText()
            miesiaclabel = self.miesiaccomboBox.currentText()
            self.label2.setText("Godziny agentów na projekcie %s w miesiącu %s"%(projektlabel,miesiaclabel))


    def generateExcel(self):
        miesiac = self.miesiaccomboBox.currentData()
        rok = self.rokcomboBox.currentText() 
        if miesiac is not None:
            if miesiac > 0:
                framedata = []
                conn = sqlite3.connect("baza.db")
                cur = conn.cursor()
                cur.execute("SELECT DISTINCT nazwisko FROM wpisy INNER JOIN agent ON agent.id = wpisy.wpisagent WHERE wpismiesiac = ? AND rok = ?",(miesiac,rok))
                agencinazwiska = []
                agenciimiona = []
                for row in cur:
                    agencinazwiska.append(row[0])
                for nazwisko in agencinazwiska:                                    
                    cur.execute("SELECT imie FROM agent WHERE nazwisko = ?",(nazwisko,))
                    for row in cur:
                        agenciimiona.append(row[0])                    
                cur.execute("SELECT DISTINCT nazwa FROM wpisy INNER JOIN projekt ON projekt.id = wpisy.wpisprojekt WHERE wpismiesiac = ? AND rok = ?",(miesiac,rok))
                projekty =[]
                for row in cur:
                    projekty.append(row[0])
                print(agencinazwiska)
                print(agenciimiona)
                print(projekty)
                for nazwisko in agencinazwiska:
                    inx = agencinazwiska.index(nazwisko)
                    for projekt in projekty:
                        tempdata=[]
                        tempdata.append(nazwisko)
                        tempdata.append(agenciimiona[inx])
                        tempdata.append(projekt)                     
                        cur.execute("SELECT id FROM agent WHERE nazwisko = ?",(nazwisko,))
                        idagenta = cur.fetchone()[0]
                        cur.execute("SELECT id FROM projekt WHERE nazwa = ?",(projekt,))
                        idprojektu = cur.fetchone()[0]
                        cur.execute("SELECT SUM(godziny) from wpisy WHERE wpisprojekt = ? AND wpismiesiac = ? AND wpisagent= ? AND rok = ?",(idprojektu,miesiac,idagenta,rok))
                        tempdata.append(cur.fetchone()[0])
                        if tempdata[3] is not None:                        
                            framedata.append(tempdata)                        
                print(framedata)
                df = pandas.DataFrame(framedata,columns =['nazwisko','imie','projekt','RBH pracy na projekcie'])
                print(df)
                df.to_excel('export.xlsx')
        
    def delwpis(self):
        conn = sqlite3.connect("baza.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM wpisy WHERE id = (SELECT MAX(id) FROM wpisy)")
        conn.commit()
        conn.close
        self.updateAgentTable()           


    def openAgentWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_AgentWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def openProjektWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ProjektWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def updateAgentList(self):
        conn = sqlite3.connect("baza.db")
        cur = conn.cursor()
        cur.execute('SELECT * FROM agent ORDER BY nazwisko')
        self.agentcomboBox.clear()
        self.agentcomboBox.addItem("Wybierz agenta:")
        for row in cur:
            self.agentcomboBox.addItem(row[2]+ " " + row[1],row[0])

    def updateProjektList(self):
        conn = sqlite3.connect("baza.db")
        cur = conn.cursor()
        cur.execute('SELECT * FROM projekt ORDER BY nazwa')
        self.projektcomboBox.clear()
        self.projektcomboBox.addItem("Wybierz projekt:")
        for row in cur:
            self.projektcomboBox.addItem(row[1],row[0])

    def updateMiesiacList(self):
        conn = sqlite3.connect("baza.db")
        cur = conn.cursor()
        cur.execute('SELECT * FROM miesiac')
        self.miesiaccomboBox.clear()
        self.miesiaccomboBox.addItem("Wybierz miesiac:")
        for row in cur:
            self.miesiaccomboBox.addItem(row[1],row[0])

    def refresh(self):
        self.updateAgentList()
        self.updateProjektList()
        self.updateAgentTable()

    def addwpis(self):
        conn = sqlite3.connect("baza.db")
        cur = conn.cursor()
        godziny = self.godzinylineEdit.text()
        godziny = godziny.replace(",",".")
        agentid = self.agentcomboBox.currentData()
        projektid = self.projektcomboBox.currentData()
        miesiacid = self.miesiaccomboBox.currentData()
        if agentid is not None and projektid is not None and miesiacid is not None:
            if agentid > 0 and projektid > 0 and miesiacid > 0:
                rok = self.rokcomboBox.currentText()
                cur.execute("INSERT INTO wpisy (godziny,data,wpisagent,wpisprojekt,wpismiesiac,rok) VALUES (?,datetime('now'),?,?,?,?)", (godziny,agentid,projektid,miesiacid,rok))
                conn.commit()
                conn.close
                self.godzinylineEdit.setText("")
                self.updateAgentTable()

    def setupUi(self, MainWindow):
        connect()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # dodaj agenta
        self.agentButton = QtWidgets.QPushButton(self.centralwidget)
        self.agentButton.setGeometry(QtCore.QRect(800, 10, 211, 71))
        self.agentButton.setObjectName("agentButton")
        self.agentButton.clicked.connect(self.openAgentWindow)
        # dodaj projekt
        self.projektButton = QtWidgets.QPushButton(self.centralwidget)
        self.projektButton.setGeometry(QtCore.QRect(800, 90, 211, 71))
        self.projektButton.setObjectName("projektButton")
        self.projektButton.clicked.connect(self.openProjektWindow)
        # refresh
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(800, 170, 211, 71))
        self.refreshButton.setObjectName("refreshButton")
        self.refreshButton.clicked.connect(self.refresh)
        # excel
        self.excelButton = QtWidgets.QPushButton(self.centralwidget)
        self.excelButton.setGeometry(QtCore.QRect(800, 250, 211, 71))
        self.excelButton.setObjectName("excelButton")
        self.excelButton.clicked.connect(self.generateExcel)        
        # dodaj wpis
        self.addgodzinyButton = QtWidgets.QPushButton(self.centralwidget)
        self.addgodzinyButton.setGeometry(QtCore.QRect(235, 10, 71, 71))
        self.addgodzinyButton.setObjectName("addgodzinyButton")
        self.addgodzinyButton.clicked.connect(self.addwpis)

        # usuń ostatni  wpis
        self.delwpisButton = QtWidgets.QPushButton(self.centralwidget)
        self.delwpisButton.setGeometry(QtCore.QRect(310, 10, 71, 71))
        self.delwpisButton.setObjectName("delwpisButton")
        self.delwpisButton.clicked.connect(self.delwpis)


        # agent combo          
        self.agentcomboBox = QtWidgets.QComboBox(self.centralwidget)
        self.agentcomboBox.setGeometry(QtCore.QRect(10, 10, 221, 38))
        self.agentcomboBox.setObjectName("agentcomboBox")
        self.agentcomboBox.activated.connect(self.updateAgentTable)
        # projekt combo
        self.projektcomboBox = QtWidgets.QComboBox(self.centralwidget)
        self.projektcomboBox.setGeometry(QtCore.QRect(10, 50, 221, 38))
        self.projektcomboBox.setObjectName("projektcomboBox")
        self.projektcomboBox.activated.connect(self.updateAgentTable)   
        # miesiac combo
        self.miesiaccomboBox = QtWidgets.QComboBox(self.centralwidget)
        self.miesiaccomboBox.setGeometry(QtCore.QRect(10, 90, 221, 38))
        self.miesiaccomboBox.setObjectName("miesiaccomboBox")
        self.miesiaccomboBox.activated.connect(self.updateAgentTable)
        # ROK combo
        self.rokcomboBox = QtWidgets.QComboBox(self.centralwidget)
        self.rokcomboBox.setGeometry(QtCore.QRect(10, 130, 221, 38))
        self.rokcomboBox.setObjectName("rokcomboBox")
        self.rokcomboBox.activated.connect(self.updateAgentTable)
        lata = ["2019","2020","2021"]
        self.rokcomboBox.addItems(lata)



        # wpis godziny
        self.godzinylineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.godzinylineEdit.setGeometry(QtCore.QRect(235, 90, 71, 38))
        self.godzinylineEdit.setObjectName("lineEdit")
        self.godzinylineEdit.setPlaceholderText("ilość")
        self.godzinylineEdit.setFocus() 
        self.godzinylineEdit.returnPressed.connect(self.addwpis)    
        self.updateAgentList()
        self.updateProjektList()
        self.updateMiesiacList()

        # tabelka1

        self.tableWidget1 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget1.setGeometry(QtCore.QRect(5, 350, 270, 418))
        self.tableWidget1.setObjectName("tableWidget1")

        # tabelka2

        self.tableWidget2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget2.setGeometry(QtCore.QRect(280, 350, 270, 418))
        self.tableWidget2.setObjectName("tableWidget2")

    #label1

        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(10, 280, 261, 61))
        self.label1.setWordWrap(True)
        self.label1.setObjectName("label")

    #label2

        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(280, 280, 261, 61))
        self.label2.setWordWrap(True)
        self.label2.setObjectName("label")   


    #MAIN 
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Godziny Agentów"))
        self.agentButton.setText(_translate("MainWindow", "Dodaj Agentów"))
        self.projektButton.setText(_translate("MainWindow", "Dodaj Projekty"))
        self.refreshButton.setText(_translate("MainWindow", "Odśwież"))
        self.excelButton.setText(_translate("MainWindow", "Generuj excela"))
        self.addgodzinyButton.setText(_translate("MainWindow", "+"))
        self.delwpisButton.setText(_translate("MainWindow", "usuń"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
