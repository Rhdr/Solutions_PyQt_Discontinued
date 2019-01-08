from PyQt5 import QtWidgets, QtCore
import views.viewEntitySearch
import views.viewEntity
import models.modelEntity
import utilityClasses.delegates

class ContEntity(QtWidgets.QMainWindow):
    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.__ui = views.viewEntity.Ui_MainWindow()
        self.__ui.setupUi(self)

        #app.aboutToQuit.connect(self.closeEvent)
        self.__clsModelEntity = models.modelEntity.ModelEntity()
        self.__clsModelEntity.connect()     #ensure db connection is created
        self.__model = self.__clsModelEntity.getModel()
        self.__ui.toolbCrud.addWidget(self.__ui.txtSearch)
        self.__ui.toolbCrud.addAction(self.__ui.actionFind)
        self.__ui.toolbCrud.addAction(self.__ui.actionDelete)
        self.__ui.tableView.horizontalHeader().sortIndicatorChanged.connect(self.__model.orderBy)
        #self.__ui.txtSearch.textChanged.connect(self.__proxyModel.setFilterRegExp)

        self.__ui.txtSearch.returnPressed.connect(lambda: self.__clsModelEntity.search(self.__ui.txtSearch.text()))
        self.__ui.actionFind.triggered.connect(lambda: self.__clsModelEntity.search(self.__ui.txtSearch.text()))

        #setup tableView & hide pk
        self.__ui.tableView.setModel(self.__model)

        self.__tableViewSelectionModel = self.__ui.tableView.selectionModel()
        self.__tableViewSelectionModel.currentRowChanged.connect(lambda: self.__model.rowChanged(self.__tableViewSelectionModel.currentIndex().row()))

        self.__tableViewSelectionModel.currentRowChanged.connect(self.rowChanged)
        self.__ui.tableView.installEventFilter(self) #install event filter to catch on focus event
        self.__ui.tableView.hideColumn(0)

        #setup & link delegates
        lineEditDelegate = utilityClasses.delegates.LineEditDelegate(self.__ui.tableView)
        spinBoxDelegate = utilityClasses.delegates.SpinBoxDelegate(self.__ui.tableView)
        self.__ui.tableView.setItemDelegateForColumn(1, lineEditDelegate)
        self.__ui.tableView.setItemDelegateForColumn(5, spinBoxDelegate)

        #connect crud
        self.__ui.actionNewRecord.triggered.connect(self.actionAdd)
        self.__ui.actionDelete.triggered.connect(self.actionDelete)
        self.__ui.actionSave.triggered.connect(self.actionSave)

        #connect nav
        self.__ui.actionFirst.triggered.connect(self.actionFirst)
        self.__ui.actionPrev.triggered.connect(self.actionPrev)
        self.__ui.actionNext.triggered.connect(self.actionNext)
        self.__ui.actionLast.triggered.connect(self.actionLast)

    def eventFilter(self, object, event):
        #print(event.type())
        if event.type() == QtCore.QEvent.FocusOut:
            #catch the on focus event
            # on editing the new row have the model insert another new row
            self.__model.insertRow(self.__ui.tableView.currentIndex().row())
            return True

        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Escape:
            #print("Escape Pressed")
            self.__model.escapePressed(self.__ui.tableView.currentIndex().row())
            return True

        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Tab:
            #attempt to catch & handle the tab key (prevent tab from jumping to first record when adding new rows)
            currentRow = self.__ui.tableView.currentIndex().row()
            currentCol = self.__ui.tableView.currentIndex().column()

            modelRow = self.__model.rowCountActual()
            modelCol = self.__model.columnCount() - 1
            #print("currentRow:", currentRow, "currentCol:", currentCol)
            #print("modelRow:", modelRow, "modelCol:", modelCol)
            if currentRow == -1 or currentCol == -1:
                return True     #stop
            elif currentRow >= modelRow and currentCol >= modelCol:
                return True     #stop
            else:
                return False    #go ahead
        return False

    def rowChanged(self, current = None, previous = None):
        #update view recordNr
        currentRow = str(self.__tableViewSelectionModel.currentIndex().row() + 1)
        rowCount = str(self.__model.rowCount())
        self.__ui.actionRecordNr.setText("Record " + currentRow + " of " + rowCount)

    def actionAdd(self):
        #add new row to bottom of table
        self.actionPrev()
        #self.__model.insertRow()
        self.__ui.tableView.selectRow(self.__model.rowCount() - 1)

    def actionDelete(self):
        #check if there is a selection, get user confirmation & delete
        #check selection
        if self.__tableViewSelectionModel.hasSelection() == True:

            # check user confirmaiton
            msgbox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Confirm Deletion",
                                           "Are you sure you wish to delete the selected items?",
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, self)
            ret = msgbox.exec()
            if ret == QtWidgets.QMessageBox.Yes:
                #delete records
                selectionModel = self.__ui.tableView.selectionModel()
                selectedRowsList = selectionModel.selectedRows()
                delRowStartPos = selectedRowsList[0].row()
                delRowsCount = len(selectedRowsList)
                self.__model.removeRows(delRowStartPos, delRowsCount)

        else:
            #no selection
            msgbox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "No Selection",
                                           "Nothing is selected, please select a row and try again",
                                           QtWidgets.QMessageBox.Ok, self)
            msgbox.exec_()

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

    def closeEvent(self, event):
        print("closing")
        self.actionPrev()
        self.actionSave()
        #event.iqnore()


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



