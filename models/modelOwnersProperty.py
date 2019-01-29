from PyQt5 import QtSql
import models._databaseConnection
import utilityClasses.TransactionSqlQueryModel
import utilityClasses.dataStructures

class ModelOwnersPropertyInterface(models._databaseConnection.DBConnection):
    def __init__(self, parent):
        super(ModelOwnersPropertyInterface, self).__init__(parent)
        self.connect()

        headers = ["Pk_PropertyOwnerID", "Pk_PropertyID"]
        sqlQueryCRUDObject = utilityClasses.dataStructures.SQLQueryCRUDObject(headers, self._db, self)

        #selectQ = """SELECT entity.Pk_EntityID, entity.Name
        #                            FROM entity
        #                            ORDER BY entity.Name;"""
        selectQ = """SELECT ownersproperty.Pk_PropertyOwnerID, ownersproperty.Pk_PropertyID
                     FROM ownersproperty;"""
        sqlQueryCRUDObject.setSelectQ(selectQ)

        appQ = """INSERT INTO ownersproperty(ownersproperty.Pk_PropertyOwnerID, ownersproperty.Pk_PropertyID) 
                    VALUES(:Pk_PropertyOwnerID, :Pk_PropertyID);"""
        appBindLst = ["Pk_PropertyOwnerID", "Pk_PropertyID"]
        appDefaultValueLst = []
        sqlQueryCRUDObject.setAppendQ(appQ, appBindLst, appDefaultValueLst)

        updQ = """UPDATE ownersproperty SET ownersproperty.Pk_PropertyOwnerID = :Pk_PropertyOwnerID, 
                                            ownersproperty.Pk_PropertyID = :Pk_PropertyID 
                    WHERE ownersproperty.Pk_PropertyOwnerID = :Pk_PropertyOwnerID;"""
        updQBindLst = ["Pk_PropertyOwnerID", "Pk_PropertyID"]
        updDefaultValueLst = []
        sqlQueryCRUDObject.setUpdateQ(updQ, updQBindLst, updDefaultValueLst)

        delQ = """DELETE FROM ownersproperty 
                    WHERE ownersproperty.Pk_PropertyOwnerID = :Pk_PropertyOwnerID AND ownersproperty.Pk_PropertyID = :Pk_PropertyID;"""
        delQBindLst = ["Pk_PropertyOwnerID", "Pk_PropertyID"]
        sqlQueryCRUDObject.setDeleteQ(delQ, delQBindLst)

        self.__model = utilityClasses.TransactionSqlQueryModel.TransactionSqlQueryModel(sqlQueryCRUDObject, parent)

    def getModel(self):
        return self.__model

    def getCmdSearchModel(self):
        self.__model.setQuery('''SELECT property.Pk_PropertyID, property.Street, property.StreetNr, property.Complex, property.ComplexNr, property.Address, 
                                   property.Town, property.Suburb, property.Fk_StreetNrID, property.Fk_ComplexNrID, CONCAT(Address, ", ", Suburb, ", ", Town) AS SearchPoperty
                                   FROM property
                                   ORDER BY SearchPoperty;''')


        #model = QtSql.QSqlQueryModel()
        #model.setQuery("""SELECT Pk_PropertyID, CONCAT(Address, ", ", Suburb, ", ", Town) AS SearchPoperty
        #                    FROM property
        #                    ORDER BY Address;""")
        return self.__model

    def filter(self, filterVal):
        self.__model.searchSQL("""SELECT property.Pk_PropertyID, property.Street, property.StreetNr, property.Complex, property.ComplexNr, property.Address, 
                                    property.Town, property.Suburb, property.Fk_StreetNrID, property.Fk_ComplexNrID
                                  FROM property
                                  WHERE Address Like '%""" + filterVal + """%' OR Town Like '%""" + filterVal + """%' OR Suburb Like '%""" + filterVal + """%;'""")

    def getCmbPk_PropertyOwnerID(self):
        model = QtSql.QSqlQueryModel(self)
        model.setQuery("""SELECT entity.Pk_EntityID, entity.Name 
                            FROM entity
                            ORDER BY entity.Name;""")
        return model

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    p = QtWidgets.QWidget()
    clsModel = ModelOwnersPropertyInterface(p)
    #try:
    clsModel.connect()
    model = clsModel.getModel()
    print(clsModel.connect())
    print(model.lastError().text())
    sys.exit(app.exec_())