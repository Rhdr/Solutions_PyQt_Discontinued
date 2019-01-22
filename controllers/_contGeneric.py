from PyQt5 import QtWidgets, QtCore

class ContGeneric(QtCore.QObject):
    def __init__(self, ui, modelInterface, model, parent):
        #QtCore.QObject.__init__(self, parent)
        super(ContGeneric, self).__init__(parent)
        self.__ui = ui
        self.__modelInterface = modelInterface
        self.__model = model
        self.__parent = parent
        self.__ui.tableView.setModel(self.__model)
        self.__ui.tableView.horizontalHeader().sortIndicatorChanged.connect(self.__model.orderBy)
        self.__tableViewSelectionModel = self.__ui.tableView.selectionModel()
        self.__tableViewSelectionModel.currentRowChanged.connect(self.rowChanged)
        self.__ui.tableView.installEventFilter(self)

        #setup crud & navigation
        self.__ui.toolbCrud.addWidget(self.__ui.txtSearch)
        self.__ui.toolbCrud.addAction(self.__ui.actionFind)
        #self.__ui.toolbCrud.addAction(self.__ui.actionDelete)
        self.__ui.actionFind.triggered.connect(self.find)
        self.__ui.txtSearch.returnPressed.connect(self.find)
        self.__ui.txtSearch.textChanged.connect(lambda: self.find(True))
        self.__ui.actionNewRecord.triggered.connect(self.actionAdd)
        #self.__ui.actionDelete.triggered.connect(self.actionDelete)
        self.__ui.actionFirst.triggered.connect(self.actionFirst)
        self.__ui.actionPrev.triggered.connect(self.actionPrev)
        self.__ui.actionNext.triggered.connect(self.actionNext)
        self.__ui.actionLast.triggered.connect(self.actionLast)

        self.__previousRow = QtCore.QModelIndex()
        self.__counterWarnAppFailed = 0

    def eventFilter(self, QObject, QEvent):
        if QEvent.type() == QEvent.KeyPress:
            if QEvent.key() == QtCore.Qt.Key_Delete:
                self.actionDelete()
                return True
        return False

    def find(self, textChanged = False):
        # find text & update the rowCount lbl
        if textChanged == True and len(self.__ui.txtSearch.text()) == 0:
            self.__modelInterface.search(self.__ui.txtSearch.text())
            self.actionNext()

        elif textChanged == False: # textChanged == False:
            self.__modelInterface.search(self.__ui.txtSearch.text())
            self.actionNext()

        self.updateRowCountLbl()

    def delegateCommitData(self):
        # add a new blank row when the last one is used
        if self.__tableViewSelectionModel.currentIndex().row() == self.__model.rowCountActual():  # and self.__addedBlankRow == False:
            self.__model.insertNewBlankRows()

    def rowChanged(self, current=None, previous=None):
        # signal model that the row changed to iniate save & test save for errors
        #print(previous.row(), self.__previousRow.row(), self.__previousRow.isValid())

        if previous.row() == -1 and self.__previousRow.row() != -1 and self.__previousRow.isValid():
            prev = self.__previousRow
        else:
            prev = previous
            self.__previousRow = previous
        saveLst = self.__model.rowChanged(current.row(), prev.row())

        if saveLst[0] == False and self.__counterWarnAppFailed == 0:
            #Notfiy user of error & dont move away from the record
            msgbox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Add/Edit Error",
                                           saveLst[1], QtWidgets.QMessageBox.Ok, self.parent())
            msgbox.show()
            QtCore.QTimer.singleShot(0.00001, lambda: self.__ui.tableView.selectRow(previous.row()))
            QtCore.QTimer.singleShot(0.00001, lambda: self.__ui.tableView.edit(previous))

            self.__counterWarnAppFailed =+ 1

        elif saveLst[0] == False and self.__counterWarnAppFailed > 0:
            QtCore.QTimer.singleShot(0.00001, lambda: self.__ui.tableView.edit(previous))

        elif current.row() == self.__model.rowCountActual():
            # reselect the last row after insert so that the tab order work as expected
            self.__ui.tableView.selectRow(current.row())
            self.__counterWarnAppFailed = 0

        self.__model.resetNewBlankRows()
        self.updateRowCountLbl()

    def updateRowCountLbl(self):
        # update view recordNr lable
        currentRow = str(self.__tableViewSelectionModel.currentIndex().row() + 1)
        rowCount = str(self.__model.rowCountActual())
        self.__ui.actionRecordNr.setText("Record " + currentRow + " of " + rowCount)

    def actionAdd(self):
        # add new row to bottom of table
        self.__ui.tableView.selectRow(self.__model.rowCount() - 1)

    def actionDelete(self):
        # check if there is a selection, get user confirmation & delete
        # check selection
        if self.__tableViewSelectionModel.hasSelection() == True:

            # check user confirmaiton
            msgbox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Confirm Deletion", "Are you sure you wish to delete the selected items?",
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, self.parent())
            ret = msgbox.exec()
            if ret == QtWidgets.QMessageBox.Yes:
                # delete records
                selectionModel = self.__ui.tableView.selectionModel()
                selectedRowsList = selectionModel.selectedRows()
                delRowStartPos = selectedRowsList[0].row()
                delRowsCount = len(selectedRowsList)

                #test for any errors
                removeRowsLst = self.__model.removeRows(delRowStartPos, delRowsCount)
                if removeRowsLst[0] == True:
                    # select a row to refresh view
                    if delRowStartPos - 1 >= 0:
                        self.__ui.tableView.selectRow(delRowStartPos - 1)
                    else:
                        self.__ui.tableView.selectRow(delRowStartPos + 1)
                else:
                    #error - display it
                    msgbox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Delete Error", removeRowsLst[1],
                                                   QtWidgets.QMessageBox.Ok, self.parent())
                    msgbox.show()

        else:
            # no selection
            msgbox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "No Selection",
                                           "Nothing is selected, please select a row and try again",
                                           QtWidgets.QMessageBox.Ok, self.__parent)
            msgbox.show()

    def actionFirst(self):
        self.__ui.tableView.selectRow(0)

    def actionPrev(self):
        self.__ui.tableView.selectRow(self.__ui.tableView.currentIndex().row() - 1)

    def actionNext(self):
        self.__ui.tableView.selectRow(self.__ui.tableView.currentIndex().row() + 1)

    def actionLast(self):
        # last record may be blank used to add more records
        self.__ui.tableView.selectRow(self.__model.rowCountActual() - 1)

    def closeEvent(self, event):
        #print("closing")
        self.actionPrev()
        self.actionNext()
        self.__model.save(self.__tableViewSelectionModel.currentIndex().row())
        # event.iqnore()