import sqlite3
import xlrd

def connect():
    conn = sqlite3.connect("baza.db")
    cur = conn.cursor()
    miesiace = ["Styczeń","Luty","Marzec","Kwiecień","Maj","Czerwiec","Lipiec","Sierpień","Wrzesień","Październik","Listopad","Grudzień"]
    cur.execute("CREATE TABLE IF NOT EXISTS agent (id INTEGER PRIMARY KEY AUTOINCREMENT, imie text, nazwisko text)")
    cur.execute("CREATE TABLE IF NOT EXISTS projekt (id INTEGER PRIMARY KEY AUTOINCREMENT, nazwa text)")
    cur.execute("CREATE TABLE IF NOT EXISTS miesiac (id INTEGER PRIMARY KEY AUTOINCREMENT, nazwa text)")
    for miesiac in miesiace:
        cur.execute("INSERT INTO miesiac (nazwa) VALUES (?)",(miesiac,))
    cur.execute("DELETE FROM miesiac WHERE  id > 12")
    cur.execute("CREATE TABLE IF NOT EXISTS wpisy (\
        id INTEGER PRIMARY KEY AUTOINCREMENT,\
        godziny real, \
        rok text, \
        data text, \
        wpisagent integer,\
        wpisprojekt integer,\
        wpismiesiac integer,\
        FOREIGN KEY(wpisagent) REFERENCES agent(id),\
        FOREIGN KEY(wpisprojekt) REFERENCES projekt(id),\
        FOREIGN KEY(wpismiesiac) REFERENCES miesiac(id))")
    conn.commit()
    conn.close
