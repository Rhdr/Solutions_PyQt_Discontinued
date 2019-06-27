from PyQt5 import QtSql

import models._databaseConnection


class MyEntity(models._databaseConnection.DBConnection):
    def __init__(self):
        super(MyEntity, self).__init__()
        self.connect()
        self.__selectQ = """SELECT Pk_MyEntityID, Name 
                            FROM MyEntity LEFT JOIN
                            Entity ON MyEntity.Pk_MyEntityID = Entity.Pk_EntityID;"""
        self.__model = QtSql.QSqlQueryModel()
        try:
            self.__model.setQuery(self.__selectQ)
        except Exception as e:
            print(self.__model.lastError().text())
            raise Exception(e)

    def getModel(self):
        return self.__model

    def refreshModel(self):
        #self.connect()
        self.__model.clear()
        self.__model.setQuery(self.__selectQ)

    def insertRecord(self, name):
        #self.connect()
        try:
            q = QtSql.QSqlQuery()
            q.prepare("""BEGIN TRANSACTION;
                            INSERT INTO Entity(Import_OldPk, Import_OldType, Name)
                            SELECT 0, 0, :name AS Name;
                            INSERT INTO MyEntity(Pk_MyEntityID)
                            SELECT SCOPE_IDENTITY();
                         COMMIT;""")
            q.bindValue(":name", name)
            q.exec()
        except Exception as e:
            print(q.lastError().text())
            raise Exception(e)

    def updateRecord(self, pk, name):
        try:
            q = QtSql.QSqlQuery()
            q.prepare("""UPDATE Entity
                         SET Name = :name
                         WHERE Pk_EntityID = :pk""")
            q.bindValue(":pk", pk)
            q.bindValue(":name", name)
            q.exec()
        except Exception as e:
            print(q.lastError().text())
            raise Exception(e)

    def deleteRecord(self, id):
        try:
            q = QtSql.QSqlQuery()
            q.prepare("""BEGIN TRANSACTION; 
                             DELETE FROM MyEntity  
                             WHERE Pk_MyEntityID = :id;
                             DELETE FROM MyEntity
                             WHERE Pk_MyEntityID = :id;
                         COMMIT;""")
            q.bindValue(":id", id)
            q.exec()
        except Exception as e:
            print(q.lastError().text())
            raise Exception(e)



if __name__ == "__main__":
    from PyQt5 import QtWidgets
    import sys
    app = QtWidgets.QApplication(sys.argv)

    p = QtWidgets.QWidget()
    myEntity = MyEntity()
    try:
        model = myEntity.getModel()
    except:
        print(model.lastError().text())
    finally:
        myEntity.closeConnection()

    sys.exit(app.exec_())