from PyQt5 import QtSql, QtCore
import mysql.connector

class DBConnection(QtCore.QObject):
    def __init__(self, parent):
        super(DBConnection, self).__init__(parent)

    __connectionOpen = False    #holds connection status open = True / closed = false
    _db = QtSql.QSqlDatabase()
    def connect(self):
        try:
            #open connection if not already open
            self.__isConnected() #refresh connection status & static conntionOpen variable
            if DBConnection.__connectionOpen == False:
                DBConnection._db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
                DBConnection._db.setHostName("localhost")  #192.168.2.5
                DBConnection._db.setDatabaseName("solutionsdb")
                DBConnection._db.setUserName("root")
                DBConnection._db.setPassword("12345") #766Prop667
                DBConnection.__connectionOpen = DBConnection._db.open()
            return DBConnection.__connectionOpen

        except:
            DBConnection.__connectionOpen = False
            print("Error:: An error occured handeling the __db object")
            try:
                print("LastError:", DBConnection._db.lastError().text())
            except:
                #intentionally left empty
                pass

    def closeConnection(self):
        try:
            print("Clossing DB Connection")
            DBConnection._db.close()
            DBConnection.__connectionOpen = False
        except:
            #intentionally left blank
            pass

    def __isConnected(self):
        # refresh connection status & return if connected or not
        try:
            DBConnection.__connectionOpen = DBConnection._db.open()
            return DBConnection.__connectionOpen
        except:
            DBConnection.__connectionOpen = False
            return False

    def __del__(self):
        try:
            DBConnection._db.close()
        except:
            #intentionally left blank
            pass

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
if __name__ == "__main__":
    from PyQt5 import QtWidgets
    import sys
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    p = QtWidgets.QWidget()
    conn = DBConnection(p)
    conn.connect()
    print("Connected: " + str(conn.connect()))
    conn.closeConnection()

    sys.exit(app.exec_())