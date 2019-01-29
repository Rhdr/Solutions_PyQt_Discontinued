from PyQt5 import QtSql
import models._databaseConnection
import utilityClasses.TransactionSqlQueryModel
import utilityClasses.dataStructures

class ModelPropertyInterface(models._databaseConnection.DBConnection):
    def __init__(self, parent):
        super(ModelPropertyInterface, self).__init__(parent)
        self.connect()

        headers = ["Pk_PropertyID", "Street", "StreetNr", "Complex", "ComplexNr", "Address", "Town", "Suburb", "Fk_StreetNrID", "Fk_ComplexNrID"]
        sqlQueryCRUDObject = utilityClasses.dataStructures.SQLQueryCRUDObject(headers, self._db, self)

        selectQ = """SELECT property.Pk_PropertyID, property.Street, property.StreetNr, property.Complex, property.ComplexNr, property.Address, 
                         property.Town, property.Suburb, property.Fk_StreetNrID, property.Fk_ComplexNrID
                       FROM property;"""
        sqlQueryCRUDObject.setSelectQ(selectQ)

        appQ = """INSERT INTO property(Import_OldPk_PropertyID, Street, StreetNr, Complex, ComplexNr, Address, Town, Suburb, Fk_StreetNrID, Fk_ComplexNrID) 
                    VALUES(0, :Street, :StreetNr, :Complex, :ComplexNr, :Address, :Town, :Suburb, :Fk_StreetNrID, :Fk_ComplexNrID);"""
        appBindLst = ["Street", "StreetNr", "Complex", "ComplexNr", "Address", "Town", "Suburb", "Fk_StreetNrID", "Fk_ComplexNrID"]
        appDefaultValueLst = []
        sqlQueryCRUDObject.setAppendQ(appQ, appBindLst, appDefaultValueLst)

        updQ = """UPDATE property SET Street = :Street, StreetNr = :StreetNr, Complex = :Complex, ComplexNr = :ComplexNr, Address = :Address, 
                      Town = :Town, Suburb = :Suburb, Fk_StreetNrID = :Fk_StreetNrID, Fk_ComplexNrID = :Fk_ComplexNrID 
                    WHERE Pk_PropertyID = :Pk_PropertyID;"""
        updQBindLst = ["Street", "StreetNr", "Complex", "ComplexNr", "Address", "Town", "Suburb", "Fk_StreetNrID", "Fk_ComplexNrID", "Pk_PropertyID"]
        updDefaultValueLst = []
        sqlQueryCRUDObject.setUpdateQ(updQ, updQBindLst, updDefaultValueLst)

        delQ = """DELETE FROM property 
                    WHERE property.Pk_PropertyID = :Pk_PropertyID;"""
        delQBindLst = ["Pk_PropertyID"]
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

    def getCmbStreetNrModel(self):
        '''
        model = QtSql.QSqlQueryModel(self)
        model.setQuery("""SELECT entity.Pk_EntityID, entity.Name 
                            FROM entity
                            ORDER BY entity.Name;""")
        '''
        model = QtSql.QSqlRelationalTableModel(self)
        model.setTable("property")
        model.setRelation(self.__model.fieldIndex("Fk_StreetNrID"), QtSql.QSqlRelation("entity", "Pk_EntityID", "Name"))
        model.select()
        return model

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    p = QtWidgets.QWidget()
    clsModel = ModelPropertyInterface(p)
    #try:
    clsModel.connect()
    model = clsModel.getModel()
    print(clsModel.connect())
    print(model.lastError().text())
    sys.exit(app.exec_())