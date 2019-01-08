from PyQt5 import QtSql
import models._databaseConnection

class ModelMyEntity(models._databaseConnection.DBConnection):
    def getModel(self):
        try:
            self.__model = QtSql.QSqlQueryModel()
            self.__model.setQuery("SELECT entity.Name \
                                  FROM myentity LEFT JOIN entity \
                                  ON myentity.Pk_MyEntityID = entity.Pk_EntityID")
            return self.__model

        except:
            print(self.__db.lastError().text())
            print(self.__query.lastError().text())
            print(self.__model.lastError().text())

if __name__ == "__main__":
    from PyQt5 import QtWidgets
    import sys
    app = QtWidgets.QApplication(sys.argv)

    p = QtWidgets.QWidget()
    clsModel = ModelMyEntity(p)
    try:
        clsModel.connect()
        model = clsModel.getModel()
    finally:
        clsModel.closeConnection()
        print(model.lastError().text())

    sys.exit(app.exec_())