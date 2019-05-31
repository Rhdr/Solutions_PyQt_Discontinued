from PyQt5 import QtWidgets, QtCore
import views.viewTestTable
import models.modelTestTable

class ContEntity(QtWidgets.QMainWindow):
    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.__ui = views.viewTestTable.Ui_MainWindow()
        self.__ui.setupUi(self)

        #app.aboutToQuit.connect(self.closeEvent)
        self.__clsModelEntity = models.modelTestTable.ModelEntity()
        self.__clsModelEntity.connect()     #ensure db connection is created
        self.__model = self.__clsModelEntity.getModel()

        #setup tableView & hide pk
        self.__ui.tableView.setModel(self.__model)

        self.__tableViewSelectionModel = self.__ui.tableView.selectionModel()
        self.__tableViewSelectionModel.currentRowChanged.connect(lambda: self.__model.rowChanged(self.__tableViewSelectionModel.currentIndex().row()))

        self.__tableViewSelectionModel.currentRowChanged.connect(self.rowChanged)
        self.__ui.tableView.installEventFilter(self) #install event filter to catch on focus event
        self.__ui.tableView.hideColumn(0)

        #connect crud
        self.__ui.actionNewRecord.triggered.connect(self.__model.insertRow)
        self.__ui.actionSave.triggered.connect(self.actionSave)

        #connect nav
        self.__ui.actionFirst.triggered.connect(self.actionFirst)
        self.__ui.actionPrev.triggered.connect(self.actionPrev)
        self.__ui.actionNext.triggered.connect(self.actionNext)
        self.__ui.actionLast.triggered.connect(self.actionLast)

    """
    def eventFilter(self, object, event):
        #print(event.type())
        if event.type() == QtCore.QEvent.FocusOut:
            #catch the on focus event
            # on editing the new row have the model insert another new row
            self.__model.insertRow(self.__ui.tableView.currentIndex().row())
            return True
    """

    def rowChanged(self, current = None, previous = None):
        #update view recordNr
        currentRow = str(self.__tableViewSelectionModel.currentIndex().row() + 1)
        rowCount = str(self.__model.rowCount())
        self.__ui.actionRecordNr.setText("Record " + currentRow + " of " + rowCount)

    def actionAdd(self):
        pass

    def actionSave(self):
        self.__model.save()

    def actionFirst(self):
        self.__ui.tableView.selectRow(0)

    def actionPrev(self):
        self.__ui.tableView.selectRow(self.__ui.tableView.currentIndex().row() - 1)

    def actionNext(self):
        self.__ui.tableView.selectRow(self.__ui.tableView.currentIndex().row() + 1)

    def actionLast(self):
        #last record may be blank used to add more records
        self.__ui.tableView.selectRow(self.__model.rowCount() - 2)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
    #logging.basicConfig(level = 'INFO', propagate = True)

    app = QtWidgets.QApplication(sys.argv)
    p = QtWidgets.QWidget()
    c = ContEntity(p)
    c.show()

    sys.exit(app.exec_())



