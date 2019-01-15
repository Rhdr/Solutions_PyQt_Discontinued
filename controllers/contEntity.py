from PyQt5 import QtWidgets, QtCore
import views.viewEntitySearch
import views.viewEntity
import controllers.conInsertRecord
import models.modelEntity
import models.modelTestTable
import utilityClasses.delegates

class ContEntity(QtWidgets.QMainWindow):
    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.__ui = views.viewEntity.Ui_MainWindow()
        self.__ui.setupUi(self)
        self.__dirtyRow = -1

        #app.aboutToQuit.connect(self.closeEvent)
        self.__modelInterface = models.modelTestTable.ModelEntityInterface()
        self.__model = self.__modelInterface.getModel()
        self.__ui.toolbCrud.addWidget(self.__ui.txtSearch)
        self.__ui.toolbCrud.addAction(self.__ui.actionFind)
        self.__ui.toolbCrud.addAction(self.__ui.actionDelete)
        #self.__ui.tableView.horizontalHeader().sortIndicatorChanged.connect(self.__model.orderBy)

        self.__ui.txtSearch.returnPressed.connect(lambda: self.__modelInterface.search(self.__ui.txtSearch.text()))
        self.__ui.actionFind.triggered.connect(lambda: self.__modelInterface.search(self.__ui.txtSearch.text()))

        #setup tableView & hide pk
        self.__ui.tableView.setModel(self.__model)

        self.__tableViewSelectionModel = self.__ui.tableView.selectionModel()
        self.__tableViewSelectionModel.currentRowChanged.connect(self.rowChanged)
        self.__ui.tableView.installEventFilter(self)
        self.__ui.tableView.hideColumn(0)

        #setup & link delegates
        lineEditDelegate = utilityClasses.delegates.LineEditDelegate(self.__ui.tableView)
        spinBoxDelegate = utilityClasses.delegates.SpinBoxDelegate(self.__ui.tableView)
        self.__ui.tableView.setItemDelegateForColumn(1, lineEditDelegate)
        self.__ui.tableView.setItemDelegateForColumn(2, lineEditDelegate)
        self.__ui.tableView.setItemDelegateForColumn(3, lineEditDelegate)
        self.__ui.tableView.setItemDelegateForColumn(4, lineEditDelegate)
        self.__ui.tableView.setItemDelegateForColumn(5, spinBoxDelegate)

        spinBoxDelegate.commitData.connect(self.delegateCommitData)
        lineEditDelegate.commitData.connect(self.delegateCommitData)

        #connect crud
        self.__ui.actionNewRecord.triggered.connect(self.actionAdd)
        self.__ui.actionDelete.triggered.connect(self.actionDelete)

        #connect nav
        self.__ui.actionFirst.triggered.connect(self.actionFirst)
        self.__ui.actionPrev.triggered.connect(self.actionPrev)
        self.__ui.actionNext.triggered.connect(self.actionNext)
        self.__ui.actionLast.triggered.connect(self.actionLast)

        #self.__addedBlankRow = False

    def delegateCommitData(self):
        print("delegateCommitData")
        if self.__tableViewSelectionModel.currentIndex().row() == self.__model.rowCountActual(): # and self.__addedBlankRow == False:
            self.__model.insertNewBlankRows()
            self.__addedBlankRow = True

    def rowChanged(self, current = None, previous = None):
        #signal model on rowchange to initiate a save
        #update view recordNr lable
        #on last row add new blank row
        print("RowChanged")
        #signal model that the row changed
        r = self.__tableViewSelectionModel.currentIndex().row()
        self.__model.rowChanged(r)
        self.__ui.tableView.selectRow(r)

        #update recordNr
        currentRow = str(self.__tableViewSelectionModel.currentIndex().row() + 1)
        rowCount = str(self.__model.rowCount())
        self.__ui.actionRecordNr.setText("Record " + currentRow + " of " + rowCount)

        #add new blank row
        #if r == self.__model.rowCount() - 1:
        #if r < self.__model.rowCountActual():
        self.__model.resetNewBlankRows()
        #self.__addedBlankRow = False

    def actionAdd(self):
        #add new row to bottom of table
        self.__model.insertNewBlankRows()
        self.actionLast()
        self.__ui.tableView.scrollToBottom()

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

    def actionFirst(self):
        self.__ui.tableView.selectRow(0)

    def actionPrev(self):
        self.__ui.tableView.selectRow(self.__ui.tableView.currentIndex().row() - 1)

    def actionNext(self):
        self.__ui.tableView.selectRow(self.__ui.tableView.currentIndex().row() + 1)

    def actionLast(self):
        #last record may be blank used to add more records
        self.__ui.tableView.selectRow(self.__model.rowCount() - 1)

    def closeEvent(self, event):
        print("closing")
        self.__model.save(self.__tableViewSelectionModel.currentIndex().row())
        #event.iqnore()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook

    app = QtWidgets.QApplication(sys.argv)
    p = QtWidgets.QWidget()
    c = ContEntity(p)
    c.show()

    sys.exit(app.exec_())