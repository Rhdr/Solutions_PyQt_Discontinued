from PyQt5 import QtSql
import models._databaseConnection
import utilityClasses.TransactionSqlQueryModel
import utilityClasses.dataStructures

class ModelPropertyOwnerInterface(models._databaseConnection.DBConnection):
    def __init__(self, parent):
        super(ModelPropertyOwnerInterface, self).__init__(parent)
        self.connect()
        headers = ["Pk_EntityID", "Name", "Surname", "Initials", "UserName", "MonthlyStatement"]
        sqlQueryCRUDObject = utilityClasses.dataStructures.SQLQueryCRUDObject(headers, self._db, self)

        selectQ = """SELECT entity.Pk_EntityID, entity.Name, entity.Surname, entity.Initials, entity.UserName, entity.MonthlyStatement
                     FROM propertyowner LEFT JOIN entity ON propertyowner.Pk_PropertOwnerID = entity.Pk_EntityID;"""
        sqlQueryCRUDObject.setSelectQ(selectQ)

        appQ = """INSERT INTO entity(Import_OldPk, Import_OldType, Name, Surname, Initials, UserName, MonthlyStatement) 
                    VALUES(0, 0, :Name, :Surname, :Initials, :UserName, :MonthlyStatement);
                  INSERt INTO propertyowner(propertyowner.Pk_PropertOwnerID, propertyowner.Import_OldPk_PropertOwnerID)
                    VALUES(LAST_INSERT_ID(), 0);"""
        appBindLst = ["Name", "Surname", "Initials", "UserName", "MonthlyStatement"]
        appDefaultValueLst = []
        sqlQueryCRUDObject.setAppendQ(appQ, appBindLst, appDefaultValueLst)

        updQ = """UPDATE entity
                    SET Name = :Name, Surname = :Surname, Initials = :Initials, UserName = :UserName, MonthlyStatement = :MonthlyStatement
                    WHERE Pk_EntityID = :Pk_EntityID;"""
        updQBindLst = ["Name", "Surname", "Initials", "UserName", "MonthlyStatement", "Pk_EntityID"]
        updDefaultValueLst = []
        sqlQueryCRUDObject.setUpdateQ(updQ, updQBindLst, updDefaultValueLst)

        delQ = """DELETE FROM propertyowner
                    WHERE propertyowner.Pk_PropertOwnerID = :Pk_EntityID;
                  DELETE FROM entity 
                    WHERE entity.Pk_EntityID = :Pk_EntityID;"""
        delQBindLst = ["Pk_EntityID"]
        sqlQueryCRUDObject.setDeleteQ(delQ, delQBindLst)

        self.__model = utilityClasses.TransactionSqlQueryModel.TransactionSqlQueryModel(sqlQueryCRUDObject, parent)

    def getModel(self):
        return self.__model

    def search(self, searchVal):
        self.__model.searchSQL("""SELECT entity.Pk_EntityID, entity.Name, entity.Surname, entity.Initials, entity.UserName, entity.MonthlyStatement
                                  FROM entity
                                  WHERE entity.Name Like '%""" + searchVal + """%' OR entity.Surname Like '%""" + searchVal + """%' OR entity.Initials Like '%""" + searchVal + """%' OR entity.UserName Like '%""" + searchVal + """%';""")

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)

    clsModel = ModelPropertyOwnerInterface()
    #try:
    clsModel.connect()
    model = clsModel.getModel()
    print(clsModel.connect())
    print(model.lastError().text())
    sys.exit(app.exec_())