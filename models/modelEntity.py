from PyQt5 import QtSql
import models._databaseConnection
import utilityClasses.TransactionSqlQueryModel

class ModelEntity(models._databaseConnection.DBConnection):
    def __init__(self):
        self.headers = ["Pk_EntityID", "Name", "Surname", "Initials", "UserName", "MonthlyStatement"]

    def getModel(self):
        try:
            self.__model = utilityClasses.TransactionSqlQueryModel.TransactionSqlQueryModel(self.headers, self._db)
            self.__model.setSelectQuery("""SELECT entity.Pk_EntityID, entity.Name, entity.Surname, entity.Initials, entity.UserName, entity.MonthlyStatement
                                      FROM entity""")

            '''
            #QueryBindListExample
            [["query1", "qBoundItem1", "qBoundItem2", "qBoundItem3", "qBoundItem4"]
             ["query2", "qBoundItem1", "qBoundItem2", "qBoundItem3", "qBoundItem4"]
             ["query3", "qBoundItem1", "qBoundItem2", "qBoundItem3", "qBoundItem4"]]
            '''

            appQueryAndBindingLst = [["""INSERT INTO entity(Name, Surname, Initials, UserName, MonthlyStatement) 
                                         VALUES(:Name, :Surname, :Initials, :UserName, :MonthlyStatement);""",
                                          ":Name", ":Surname", ":Initials", ":UserName", ":MonthlyStatement"]]
            self.__model.setAppendQuery(appQueryAndBindingLst)

            updateQueryAndBindingLst = [["""UPDATE entity 
                                            SET Name = :Name, Surname = :Surname, Initials = :Initials, UserName = :UserName, MonthlyStatement = :MonthlyStatement
                                            WHERE Pk_EntityID = :Pk_EntityID;""",
                                             ":Name", ":Surname", ":Initials", ":UserName", ":MonthlyStatement", ":Pk_EntityID"]]
            self.__model.setUpdateQuery(updateQueryAndBindingLst)

            deleteQueryAndBindingLst = [["""DELETE FROM entity WHERE entity.Pk_EntityID = :Pk_EntityID;""",
                                             ":Pk_EntityID"]]
            self.__model.setDeleteQuery(deleteQueryAndBindingLst)

            '''
            self.__model = QtSql.QSqlTableModel()
            self.__model.setTable("entity")
            self.__model.setEditStrategy(QtSql.QSqlTableModel.OnRowChange)
            self.__model.select()
            '''
            return self.__model

        except Exception as e:
            raise Exception("ModelEntity - getModel: " + self.__model.lastError().text())

    def getModelNewRecord(self):
        __modelNewRecord = utilityClasses.TransactionSqlQueryModel.TransactionSqlQueryModel_NewRecord(self.headers, self._db)
        __modelNewRecord.setSelectQuery("""SELECT entity.Pk_EntityID, entity.Name, entity.Surname, entity.Initials, entity.UserName, entity.MonthlyStatement
                                           FROM entity
                                           WHERE entity.Pk_EntityID = 0""")
        return __modelNewRecord

    def search(self, searchVal):
        self.__model.searchSQL("""SELECT entity.Pk_EntityID, entity.Name, entity.Surname, entity.Initials, entity.UserName, entity.MonthlyStatement
                                  FROM entity
                                  WHERE entity.Name Like '%""" + searchVal + """%' OR entity.Surname Like '%""" + searchVal + """%' OR entity.Initials Like '%""" + searchVal + """%' OR entity.UserName Like '%""" + searchVal + """%'""")

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)

    clsModel = ModelEntity()
    #try:
    clsModel.connect()
    model = clsModel.getModel()
    print(clsModel.connect())
    print(model.lastError().text())
    '''
    except:
            print(__model.lastError().text())
    finally:
        clsModel.closeConnection()
    '''
    sys.exit(app.exec_())