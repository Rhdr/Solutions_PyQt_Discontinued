from PyQt5 import QtWidgets, QtCore, QtSql
import views.viewInsertRecord
import models._databaseConnection

class ContInsertRecord(QtWidgets.QDialog):
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.__ui = views.viewInsertRecord.Ui_Dialog()
        self.__ui.setupUi(self)

        db = models._databaseConnection.DBConnection()
        db.connect()
        query = QtSql.QSqlQuery()
        query.prepare("""SELECT entity.Pk_EntityID, entity.Name, entity.Surname, entity.Initials, entity.UserName, entity.MonthlyStatement
                   FROM entity""")
        query.exec()
        tblModel = QtSql.QSqlTableModel()
        tblModel.setQuery(query)
        #tblModel.setTable("Entity")
        tblModel.select()
        tblModel.insertRow(tblModel.rowCount())

        self.__ui.tableView.setModel(tblModel)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook

    app = QtWidgets.QApplication(sys.argv)
    p = QtWidgets.QDialog()
    c = ContInsertRecord(p)
    c.show()

    sys.exit(app.exec_())
