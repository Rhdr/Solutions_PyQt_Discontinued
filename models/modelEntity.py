from PyQt5 import QtSql
import models._databaseConnection
import utilityClasses.TransactionSqlQueryModel

class ModelEntityInterface(models._databaseConnection.DBConnection):
    def __init__(self):
        self.connect()
        headers = ["Pk_EntityID", "Name", "Surname", "Initials", "UserName", "MonthlyStatement"]
        selectQ = """SELECT entity.Pk_EntityID, entity.Name, entity.Surname, entity.Initials, entity.UserName, entity.MonthlyStatement
                                  FROM entity"""

        '''
        #QueryBindListExample (Transaction Support [commit & rollback]):
        Ex1: ["query1 :bindX query2 :bindX query3 :bindX", ":q1BoundItem1", ":q1BoundItem2", ":q2BoundItem1", ":q2BoundItem2", ":q3BoundItem1", ":q3BoundItem2"]
        Ex2: ["query1 :bindX", ":q1BoundItem1", ":q1BoundItem2"]
        '''
        appQueryNBindLst = ["""INSERT INTO entity(Name, Surname, Initials, UserName, MonthlyStatement) 
                               VALUES(:Name, :Surname, :Initials, :UserName, :MonthlyStatement);""",
                               "Name", "Surname", "Initials", "UserName", "MonthlyStatement"]
        updQueryNBindList = ["""UPDATE entity
                                SET Name = :Name, Surname = :Surname, Initials = :Initials, UserName = :UserName, MonthlyStatement = :MonthlyStatement
                                WHERE Pk_EntityID = :Pk_EntityID;""",
                                "Name", "Surname", "Initials", "UserName", "MonthlyStatement", "Pk_EntityID"]
        deleteQueryNBindLst = ["""DELETE FROM entity WHERE entity.Pk_EntityID = :Pk_EntityID;""",
                                  "Pk_EntityID"]
        self.__model = utilityClasses.TransactionSqlQueryModel.TransactionSqlQueryModel(headers, selectQ, appQueryNBindLst,
                                                                                        updQueryNBindList, deleteQueryNBindLst, self._db)

    def getModel(self):
        return self.__model

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

    clsModel = ModelEntityInterface()
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

    #testing version control