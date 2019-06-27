from PyQt5 import QtWidgets, QtCore

import models.modelMyEntity
import utilityClasses.delegates  
import views.viewInterface_Main  
import views.viewMyEntity 


class ContMyEntity(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super(ContMyEntity, self).__init__(parent)

        #setup the two interfaces (__uiInterfaceMain & __uiMyEntity)
        self.__uiInterfaceMain = views.viewInterface_Main.Ui_MainWindow()
        self.__uiInterfaceMain.setupUi(self)
        self.__uiInterfaceMain.lblTitle.setText("My Entities")
        subWindowEntity = QtWidgets.QMainWindow(self)
        self.__uiMyEntity = views.viewMyEntity.Ui_MainWindow()
        self.__uiMyEntity.setupUi(subWindowEntity)
        self.__uiMyEntity.btnSaveUpdate.hide()
        self.__uiInterfaceMain.scrollArea_InsertEdit.setWidget(subWindowEntity)
        subWindowEntity.show()

        #create entity object & load models
        self.__myEntity = models.modelMyEntity.MyEntity()
        self.__modelSource = self.__myEntity.getModel()
        self.__modelSortFilterProxy = QtCore.QSortFilterProxyModel()
        self.__modelSortFilterProxy.setSourceModel(self.__modelSource)
        self.__modelSortFilterProxy.sort(1, QtCore.Qt.AscendingOrder);
        #self.__modelSortFilterProxy.setDynamicSortFilter(True)
        self.__modelSortFilterProxy.setSortRole(QtCore.Qt.DisplayRole)
        self.__uiInterfaceMain.tableView.setSortingEnabled(True)
        self.__uiInterfaceMain.tableView.setModel(self.__modelSortFilterProxy)
        self.__tableSelectionModel = self.__uiInterfaceMain.tableView.selectionModel()

        #create mapper
        self.__mapper = QtWidgets.QDataWidgetMapper()
        self.__mapper.setModel(self.__modelSortFilterProxy)
        self.__mapper.addMapping(self.__uiMyEntity.txtName, 1)
        self.__mapper.setSubmitPolicy(QtWidgets.QDataWidgetMapper.ManualSubmit)

        #connect signals & slots
        self.__uiInterfaceMain.btnInsertEdit.clicked.connect(self.btnInsertEdit_Clicked)
        self.__uiInterfaceMain.btnCapturedRecords.clicked.connect(self.btnCapturedRecords_Clicked)
        self.__tableSelectionModel.selectionChanged.connect(self.__currentRowChanged)
        self.__uiMyEntity.btnNew.clicked.connect(self.newBlankRecord)
        self.__uiMyEntity.btnSaveInsert.clicked.connect(self.saveInsertRecord)
        self.__uiMyEntity.btnSaveUpdate.clicked.connect(self.saveUpdateRecord)
        self.__uiInterfaceMain.actionFirst.triggered.connect(self.actionFirst)
        self.__uiInterfaceMain.actionPrev.triggered.connect(self.actionPrev)
        self.__uiInterfaceMain.actionNext.triggered.connect(self.actionNext)
        self.__uiInterfaceMain.actionLast.triggered.connect(self.actionLast)
        self.__uiInterfaceMain.tableView.installEventFilter(self)  # install event filter to catch delete events
        
        self.actionFirst()

    def actionFirst(self):
        self.__mapper.toFirst()
        newRowTableIndex = self.__uiInterfaceMain.tableView.model().index(self.__mapper.currentIndex(), 1)
        self.__uiInterfaceMain.tableView.setCurrentIndex(newRowTableIndex)

    def actionPrev(self):
        self.__mapper.toPrevious()
        newRowTableIndex = self.__uiInterfaceMain.tableView.model().index(self.__mapper.currentIndex(), 1)
        self.__uiInterfaceMain.tableView.setCurrentIndex(newRowTableIndex)

    def actionNext(self):
        self.__mapper.toNext()
        newRowTableIndex = self.__uiInterfaceMain.tableView.model().index(self.__mapper.currentIndex (), 1)
        #print(newRowTableIndex.row())
        #print(newRowTableIndex.column())
        #print(newRowTableIndex.data(QtCore.Qt.DisplayRole))
        self.__uiInterfaceMain.tableView.setCurrentIndex(newRowTableIndex)

    def actionLast(self):
        self.__mapper.toLast()
        newRowTableIndex = self.__uiInterfaceMain.tableView.model().index(self.__mapper.currentIndex(), 1)
        self.__uiInterfaceMain.tableView.setCurrentIndex(newRowTableIndex)

    def newBlankRecord(self):
        self.__uiMyEntity.txtName.clear()
        self.__uiMyEntity.btnSaveUpdate.hide()
        self.__uiMyEntity.btnSaveInsert.show()
        self.__uiMyEntity.btnNew.hide()

    def saveInsertRecord(self):
        name = self.__uiMyEntity.txtName.text()
        self.__myEntity.insertRecord(name)
        self.__myEntity.refreshModel()
        self.actionLast()
        self.newBlankRecord()
        self.__uiMyEntity.txtName.setFocus()

    def saveUpdateRecord(self):
        row = self.__mapper.currentIndex()
        qModelIndex = self.__uiInterfaceMain.tableView.model().index(row, 0);
        pk = qModelIndex.data(QtCore.Qt.DisplayRole)
        name = self.__uiMyEntity.txtName.text()
        self.__myEntity.updateRecord(pk, name)
        self.__myEntity.refreshModel()
        self.__uiInterfaceMain.tableView.setCurrentIndex(qModelIndex)

    #Detect row Change
    def __currentRowChanged(self, current, previous):
        qModelIndexList = current.indexes()
        try:
            currentRow = qModelIndexList[0].row()
            pk = (qModelIndexList[0].data(QtCore.Qt.DisplayRole))
            name = (qModelIndexList[1].data(QtCore.Qt.DisplayRole))
            self.__mapper.setCurrentIndex(currentRow)
            self.__uiMyEntity.btnSaveUpdate.show()
            self.__uiMyEntity.btnSaveInsert.hide()
            self.__uiMyEntity.btnNew.show()
            selectedRowNo = self.__tableSelectionModel.selectedRows()[0].row() + 1
            #selectedRowNo = selectedRows
            self.__uiInterfaceMain.actionRecordNr.setText("Record " + str(selectedRowNo) + 
                                                           " of " + str(self.__modelSortFilterProxy.rowCount()))
            #print(currentRow, pk, name)
        except IndexError:
            pass #if the user select invalid indexes dont exec the code

    #show hide InsertEdit section
    def btnInsertEdit_Clicked(self):
        if self.__uiInterfaceMain.btnInsertEdit.isChecked():
            self.__uiInterfaceMain.btnInsertEdit.setChecked(True)
            self.__uiInterfaceMain.scrollArea_InsertEdit.setMaximumHeight(16777215)
        else:
            self.__uiInterfaceMain.btnInsertEdit.setChecked(False)
            self.__uiInterfaceMain.scrollArea_InsertEdit.setMaximumHeight(0)

    #show hide CapturedRecords
    def btnCapturedRecords_Clicked(self):
        if self.__uiInterfaceMain.btnCapturedRecords.isChecked():
            self.__uiInterfaceMain.btnCapturedRecords.setChecked(True)
            self.__uiInterfaceMain.scrollArea_CapturedRecords.setMaximumHeight(16777215)
        else:
            self.__uiInterfaceMain.btnCapturedRecords.setChecked(False)
            self.__uiInterfaceMain.scrollArea_CapturedRecords.setMaximumHeight(0)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Delete:
            #print("Delete Key Pressed")
            selectedRows = self.__tableSelectionModel.selectedRows()
            for i in range(len(selectedRows)):
                row = selectedRows[i].row()
                pk = selectedRows[i].data(QtCore.Qt.DisplayRole)
                self.__myEntity.deleteRecord(pk)
            self.__myEntity.refreshModel()

            #select next row (if next row < than max/last rows then move to last row)
            if (row < self.__modelSortFilterProxy.rowCount()):
                qModelIndex = self.__uiInterfaceMain.tableView.model().index(row, 0);
                self.__uiInterfaceMain.tableView.setCurrentIndex(qModelIndex)
            else:
                self.actionLast()
            return False
        return True

    def closeEvent(self, event):
        print("closing")
        #event.iqnore()

    '''
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

    def rowChanged(self, current = None, previous = None):
        #update view recordNr
        currentRow = str(self.__tableViewSelectionModel.currentIndex().row() + 1)
        rowCount = str(self.__model.rowCount())
        self.__ui.actionRecordNr.setText("Record " + currentRow + " of " + rowCount)


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



    '''

if __name__ == "__main__":
    import sys
    #logging.basicConfig(level = 'INFO', propagate = True)

    app = QtWidgets.QApplication(sys.argv)
    p = QtWidgets.QWidget()
    c = ContMyEntity(p)
    c.show()

    sys.exit(app.exec_())



