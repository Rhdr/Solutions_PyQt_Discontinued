from PyQt5 import QtSql, QtCore
import mysql.connector
class DBConnection(object):
    '''
    def connect(self):
        self._connName = "SolutionsDB_Conn"
        if(QtSql.QSqlDatabase.contains(self._connName)):
            # connection found
            print("DB Connection Exist:", self._db.open())
            return self._db.open()
        else:
            #connection not found
            self._db = QtSql.QSqlDatabase.addDatabase("QODBC3", self._connName)
            self._db.setHostName("127.0.0.1")  #192.168.2.5
            self._db.setDatabaseName("SolutionsDB")
            self._db.setUserName("sa")
            self._db.setPassword("766Prop667")
            try:
                print("DB Connection Created:", self._db.open())
                return self._db.open()
            except Exception as e:
                print("DB Connection Error:", self._db.lastError().text())
                return False

            #example Query
            #q = QtSql.QSqlQuery("SELECT * FROM MyEntity", self._db)
            #q.exec(self._connName)

    def closeConnection(self):
        try:
            print("Clossing DB Connection")
            self._db.close()
        except:
            #intentionally left blank
            pass

    def __del__(self):
        try:
            print("Deleting DB Connection")
            self._db.close()
        except:
            #intentionally left blank
            pass

    '''
    _db = None
    def connect(self):
        try:
            if DBConnection._db == None or (DBConnection._db.open() == False):
                DBConnection._db = QtSql.QSqlDatabase.addDatabase("QODBC")
                DBConnection._db.setHostName("127.0.0.1")  #192.168.2.5
                DBConnection._db.setDatabaseName("SolutionsDB")
                #DBConnection._db.setUserName("root")
                #DBConnection._db.setPassword("12345") #766Prop667
                print("DB Connection Created:", DBConnection._db.open())
            return DBConnection._db.open()

        except Exception as e:
            print("DB Connection Error:", self._db.lastError().text())
            return False

    def closeConnection(self):
        try:
            print("DB Connection: Closing")
            DBConnection._db.close()
        except:
            #intentionally left blank
            pass

    def __del__(self):
        try:
            print("DB Connection: Deleting")
            DBConnection._db.close()
        except:
            #intentionally left blank
            pass


if __name__ == "__main__":
    from PyQt5 import QtWidgets
    import sys
    app = QtWidgets.QApplication(sys.argv)

    conn = DBConnection()
    conn.connect()
    conn.closeConnection()

    sys.exit(app.exec_())