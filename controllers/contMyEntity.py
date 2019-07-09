import utilityClasses.loggingSetup
logger = utilityClasses.loggingSetup.Logger.getLogger(__file__)

from PyQt5 import QtWidgets, QtCore
import models.modelMyEntity
import views.viewInterface_Main  
import views.viewMyEntity

class ContMyEntity(QtWidgets.QMainWindow):
    def __init__(self, parent):
        logger.debug("starting, parent: " + str(parent))
        super(ContMyEntity, self).__init__(parent)
        self.__dirty = False
        
        #setup the two interfaces (__uiInterfaceMain & __uiMyEntity)
        subWindowEntity = QtWidgets.QMainWindow(self)
        self.__uiInterfaceMain = views.viewInterface_Main.Ui_MainWindow()
        self.__uiInterfaceMain.setupUi(self)
        self.__uiInterfaceMain.lblTitle.setText("My Entities")
        self.__uiInterfaceMain.scrollArea_InsertEdit.setWidget(subWindowEntity)
        self.__uiMyEntity = views.viewMyEntity.Ui_MainWindow()
        self.__uiMyEntity.setupUi(subWindowEntity)
        self.__uiMyEntity.btnSaveUpdate.hide()
        subWindowEntity.show()
        
        #create entity object & load models
        self.__modelSource = models.modelMyEntity.MyEntity.getModel()
        self.__modelSortFilterProxy = QtCore.QSortFilterProxyModel()
        self.__modelSortFilterProxy.setSourceModel(self.__modelSource)
        self.__modelSortFilterProxy.sort(1, QtCore.Qt.AscendingOrder);
        self.__modelSortFilterProxy.setSortRole(QtCore.Qt.DisplayRole)
        self.__uiInterfaceMain.tableView.horizontalHeader().setSortIndicator(1, QtCore.Qt.AscendingOrder)
        self.__uiInterfaceMain.tableView.setSortingEnabled(True)
        self.__uiInterfaceMain.tableView.setModel(self.__modelSortFilterProxy)
        self.__tableSelectionModel = self.__uiInterfaceMain.tableView.selectionModel()

        #create mapper
        self.__mapper = QtWidgets.QDataWidgetMapper()
        self.__mapper.setModel(self.__modelSortFilterProxy)
        self.__mapper.addMapping(self.__uiMyEntity.txtName, 1)
        self.__mapper.setSubmitPolicy(QtWidgets.QDataWidgetMapper.ManualSubmit)

        #setup search combo
        self.__uiInterfaceMain.cmbColSearch.addItems(models.modelMyEntity.MyEntity.getHeaderLst())
        self.__uiInterfaceMain.cmbColSearch.setCurrentIndex(1)
    
        #connect signals & slots
        self.__tableSelectionModel.selectionChanged.connect(self.__currentRowChanged)
        self.__uiMyEntity.txtName.textEdited.connect(self.setDirty)
        self.__uiMyEntity.txtName.returnPressed.connect(self.save)
        self.__uiMyEntity.txtUserName.textEdited.connect(self.setDirty)
        self.__uiMyEntity.txtUserName.returnPressed.connect(self.save)
        self.__uiMyEntity.btnNew.clicked.connect(self.newBlankRecord)
        self.__uiMyEntity.btnSaveInsert.clicked.connect(self.saveInsertRecord)
        self.__uiMyEntity.btnSaveUpdate.clicked.connect(self.saveUpdateRecord)
        self.__uiInterfaceMain.tableView.clicked.connect(self.tableClicked)
        self.__uiInterfaceMain.btnInsertEdit.clicked.connect(self.btnInsertEdit_Clicked)
        self.__uiInterfaceMain.btnRecords.clicked.connect(self.btnRecords_Clicked)
        self.__uiInterfaceMain.actionFirst.triggered.connect(self.actionFirst)
        self.__uiInterfaceMain.actionPrev.triggered.connect(self.actionPrev)
        self.__uiInterfaceMain.actionNext.triggered.connect(self.actionNext)
        self.__uiInterfaceMain.actionLast.triggered.connect(self.actionLast)
        self.__uiInterfaceMain.actionNewRecord.triggered.connect(self.newBlankRecord)
        self.__uiInterfaceMain.btnSearch.clicked.connect(self.search)
        self.__uiInterfaceMain.txtSearch.textChanged.connect(self.searchTxtChanged)
        self.__uiInterfaceMain.txtSearch.returnPressed.connect(self.search)
        self.__uiInterfaceMain.tableView.horizontalHeader().sectionClicked.connect(self.refreshTableView)
        self.__uiInterfaceMain.tableView.installEventFilter(self)  # install event filter to catch delete events
        #self.actionFirst()
        self.newBlankRecord()
        
        logger.info("object instantiated")
        logger.debug("completed")
    
    def tableClicked(self):
        logger.debug("starting")
        self.__mapper.setCurrentIndex(self.__mapper.currentIndex())
        logger.debug("completed")
    
    def refreshTableView(self):
        logger.debug("starting")
        indexTopLeft = self.__uiInterfaceMain.tableView.indexAt(QtCore.QPoint(0, 0))
        indexBottomRight =  self.__uiInterfaceMain.tableView.indexAt(QtCore.QPoint(self.__modelSource.rowCount(), self.__modelSource.columnCount()))
        self.__uiInterfaceMain.tableView.dataChanged(indexTopLeft, indexBottomRight)
        logger.debug("completed")
    
    def save(self, newBlankRow = True, focusModelIndex = None):
        logger.debug("starting")
        if self.__uiMyEntity.btnSaveInsert.isVisible():
            self.saveInsertRecord(newBlankRow, focusModelIndex)
        elif self.__uiMyEntity.btnSaveUpdate.isVisible():
            self.saveUpdateRecord(newBlankRow, focusModelIndex)
        else:
            raise Exception("Cant determine if the data should update or insert")
            logger.exception()
        logger.debug("completed")
    
    def setDirty(self):
        self.__dirty = True
        logger.debug("dirty: " + str(self.__dirty))
    
    def displayStatus(self, text):
        logger.debug("starting, text: " + str(text))
        self.__uiMyEntity.lblStatus.setText(text)
        #self.__uiInterfaceMain.lblStatus.setText(text)
        self.__timer = QtCore.QTimer(self)
        self.__timer.singleShot(6000, lambda: self.__uiMyEntity.lblStatus.clear())
        #self.__timer.singleShot(5000, lambda: self.__uiInterfaceMain.lblStatus.clear())
        logger.debug("completed")
        
    def searchTxtChanged(self):
        logger.debug("starting")
        if not self.__uiInterfaceMain.txtSearch.text():
            self.search()
        logger.debug("completed")
            
    def search(self):
        logger.debug("Starting Search")
        s = "*" + self.__uiInterfaceMain.txtSearch.text() + "*"
        rx = QtCore.QRegExp(s)
        rx.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        rx.setPatternSyntax(QtCore.QRegExp.Wildcard)
        self.__modelSortFilterProxy.setFilterRegExp(rx)
        
        cmbVal = self.__uiInterfaceMain.cmbColSearch.itemText(self.__uiInterfaceMain.cmbColSearch.currentIndex())
        cmbValPos = models.modelMyEntity.MyEntity.getHeaderLst().index(cmbVal)
        self.__modelSortFilterProxy.setFilterKeyColumn(cmbValPos)

        self.refreshTableView()
        logger.info("Searched " + str(s) + " in column " + str(cmbVal))
        logger.debug("completed")
        
    def actionFirst(self):
        logger.debug("starting")
        self.__mapper.toFirst()
        newRowTableIndex = self.__uiInterfaceMain.tableView.model().index(self.__mapper.currentIndex(), 1)
        self.__uiInterfaceMain.tableView.setCurrentIndex(newRowTableIndex)
        logger.debug("completed")

    def actionPrev(self):
        logger.debug("starting")
        self.__mapper.toPrevious()
        newRowTableIndex = self.__uiInterfaceMain.tableView.model().index(self.__mapper.currentIndex(), 1)
        self.__uiInterfaceMain.tableView.setCurrentIndex(newRowTableIndex)
        logger.debug("completed")

    def actionNext(self):
        logger.debug("starting")
        self.__mapper.toNext()
        newRowTableIndex = self.__uiInterfaceMain.tableView.model().index(self.__mapper.currentIndex (), 1)
        self.__uiInterfaceMain.tableView.setCurrentIndex(newRowTableIndex)

    def actionLast(self):
        logger.debug("starting")
        self.__mapper.toLast()
        newRowTableIndex = self.__uiInterfaceMain.tableView.model().index(self.__mapper.currentIndex(), 1)
        self.__uiInterfaceMain.tableView.setCurrentIndex(newRowTableIndex)
        logger.debug("completed")

    def newBlankRecord(self, clearSelection = True):
        logger.debug("starting")
        if clearSelection:
            self.__uiInterfaceMain.tableView.clearSelection()
        self.__uiMyEntity.btnSaveUpdate.hide()
        self.__uiMyEntity.btnSaveInsert.show()
        self.__uiMyEntity.btnNew.hide()
        self.__uiMyEntity.txtUserName.clear()
        self.__uiMyEntity.txtName.clear()
        self.__uiMyEntity.txtName.setFocus()
        logger.debug("completed")

    def saveInsertRecord(self,  newBlankRow = True, focusModelIndex = None):
        logger.debug("starting, newBlankRow:" + str(newBlankRow) + ", focusModelIndex:" + str(focusModelIndex))
        name = self.__uiMyEntity.txtName.text()
        lastInsertedIdLst = models.modelMyEntity.MyEntity.insertRecord(name)
        if focusModelIndex != None:
            newPk = focusModelIndex.data(QtCore.Qt.DisplayRole)
            print("newPk:", newPk)
        if lastInsertedIdLst[0] >= 0:
            #record inserted
            self.__dirty = False
            models.modelMyEntity.MyEntity.refreshModel()            
            self.displayStatus("*A new record have been inserted: " + name)
            if focusModelIndex == None:
                self.__uiInterfaceMain.tableView.setCurrentIndex(self.findModelValue(lastInsertedIdLst[0]))
            else:
                self.__uiInterfaceMain.tableView.setCurrentIndex(self.findModelValue(newPk))
            if newBlankRow:
                self.newBlankRecord(False)
            self.__uiMyEntity.txtName.setFocus()
        else:
            #failed to insert
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, 
                                  "Could not save", "Could not save: " + str(lastInsertedIdLst[1]), 
                                  QtWidgets.QMessageBox.Ok).exec()
        logger.debug("completed")

    def saveUpdateRecord(self, newBlankRow = True, focusModelIndex = None):
        logger.debug("starting, newBlankRow:" + str(newBlankRow) + ", focusModelIndex:" + str(focusModelIndex))
        row = self.__mapper.currentIndex()
        qModelIndex = self.__uiInterfaceMain.tableView.model().index(row, 0);
        pk = qModelIndex.data(QtCore.Qt.DisplayRole)
        name = self.__uiMyEntity.txtName.text()
        if focusModelIndex != None:
            newPk = focusModelIndex.data(QtCore.Qt.DisplayRole)
        lastUpdatedId = models.modelMyEntity.MyEntity.updateRecord(pk, name)
        if lastUpdatedId[0] >= 0:
            #record updated
            self.__dirty = False        
            models.modelMyEntity.MyEntity.refreshModel()
            self.displayStatus("*The record have been updated to: " + name)
            if focusModelIndex == None:
                self.__uiInterfaceMain.tableView.setCurrentIndex(self.findModelValue(pk))
            else:
                self.__uiInterfaceMain.tableView.setCurrentIndex(self.findModelValue(newPk))
            if newBlankRow:
                self.newBlankRecord(False)
            self.__uiMyEntity.txtName.setFocus()
        else:
            #failed to update
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, 
                                  "Could not save", "Could not save: " + lastUpdatedId[1], 
                                  QtWidgets.QMessageBox.Ok).exec()
        logger.debug("completed")
    
    def findModelValue(self, val, row = 0, col = 0):
        logger.debug("starting, val:" + str(val) + ", row:" + str(row) + ", col:" + str(col))
        qModelIndexStart = self.__uiInterfaceMain.tableView.model().index(row, col)
        match = self.__uiInterfaceMain.tableView.model().match(qModelIndexStart, QtCore.Qt.DisplayRole, val, 1, QtCore.Qt.MatchExactly)
        logger.debug("completed, match: {0}, matchRow: {1}, matchColumn: {2}, matchData:{3}".format(str(match), 
                     str(match[0].row()), str(match[0].column()), str(match[0].data(QtCore.Qt.DisplayRole))))
        return match[0]

    #Detect row Change
    def __currentRowChanged(self, current, previous):
        logger.debug("starting. current: " + str(current) + " previous: " + str(previous))
        if self.__dirty == True:
            reply = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Confirm Save",
                               "Do you wish to Save the changes?",
                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, self).exec()
            if reply == QtWidgets.QMessageBox.Yes:
                logger.info("Save on RowChange: Yes")
                print(current.indexes()[0].data(QtCore.Qt.DisplayRole))
                self.save(False, current.indexes()[0])
            elif reply == QtWidgets.QMessageBox.No:
                logger.warning("Save on RowChange: No")
                self.__dirty = False
            else:
                logger.info("Save on RowChange: Canceled")
                return

        qModelIndexList = current.indexes()
        try:
            currentRow = qModelIndexList[0].row()
            #pk = (qModelIndexList[0].data(QtCore.Qt.DisplayRole))
            #name = (qModelIndexList[1].data(QtCore.Qt.DisplayRole))
            self.__mapper.setCurrentIndex(currentRow)
            self.__uiMyEntity.btnSaveUpdate.show()
            self.__uiMyEntity.btnSaveInsert.hide()
            self.__uiMyEntity.btnNew.show()
            selectedRowNo = self.__tableSelectionModel.selectedRows()[0].row() + 1
            self.__uiInterfaceMain.actionRecordNr.setText("Record " + str(selectedRowNo) + 
                                                           " of " + str(self.__modelSortFilterProxy.rowCount()))
        except IndexError:
            pass #if the user select invalid indexes don't terminate the code
        logger.debug("completed")
        
    #show hide InsertEdit section
    def btnInsertEdit_Clicked(self):
        logger.debug("starting")
        if self.__uiInterfaceMain.btnInsertEdit.isChecked():
            self.__uiInterfaceMain.btnInsertEdit.setChecked(True)
            self.__uiInterfaceMain.scrollArea_InsertEdit.setMaximumHeight(16777215)
        else:
            self.__uiInterfaceMain.btnInsertEdit.setChecked(False)
            self.__uiInterfaceMain.scrollArea_InsertEdit.setMaximumHeight(0)
        logger.debug("completed")
        
    #show hide CapturedRecords
    def btnRecords_Clicked(self):
        logger.debug("starting")
        if self.__uiInterfaceMain.btnRecords.isChecked():
            self.__uiInterfaceMain.btnRecords.setChecked(True)
            self.__uiInterfaceMain.scrollArea_CapturedRecords.setMaximumHeight(16777215)
        else:
            self.__uiInterfaceMain.btnRecords.setChecked(False)
            self.__uiInterfaceMain.scrollArea_CapturedRecords.setMaximumHeight(0)
        logger.debug("completed")
    
    def eventFilter(self, obj, event):
        #delete
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Delete:
            #"Delete Key Pressed"
            selectedRows = self.__tableSelectionModel.selectedRows()
            logger.debug("starting, obj: " + str(obj) + " event: " + str(event) + " selectedRows: " + str(selectedRows))
            msgbox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Confirm Deletion",
                                           "You are about to delete " + str(len(selectedRows)) + " record(s). Are you sure you wish to delete the selected item(s)?",
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel, self)
            ret = msgbox.exec()
            if ret == QtWidgets.QMessageBox.Yes:
                logger.debug("User about to delete selected records")
                self.deleteRecords(selectedRows)
            logger.debug("completed")
            return True
        return False
    
    def deleteRecords(self, selectedRows):
        logger.debug("starting")
        pkLst = []
        for i in range(len(selectedRows)):
            row = selectedRows[i].row()
            pk = selectedRows[i].data(QtCore.Qt.DisplayRole)
            pkLst.append(pk)
        deletedRecordsLenght =  len(models.modelMyEntity.MyEntity.deleteRecords(pkLst))
        if deletedRecordsLenght >=0:
            models.modelMyEntity.MyEntity.refreshModel()
            
            #select next row (if next row < than max/last rows then move to last row)
            if (row < self.__modelSortFilterProxy.rowCount()):
                qModelIndex = self.__uiInterfaceMain.tableView.model().index(row, 0);
                self.__uiInterfaceMain.tableView.setCurrentIndex(qModelIndex)
            else:
                self.actionLast()
            self.displayStatus("*" + str(deletedRecordsLenght) + " Record(s) have been deleted")
        logger.debug("completed")
        
    def closeEvent(self, event):
        """On dirty save else just confirm exit"""
        logger.debug("starting, event: " + str(event))
        if self.__dirty:
            reply = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Confirm Save on Exit",
                                           "Do you wish to Save before you exit?",
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, self).exec()
            if reply == QtWidgets.QMessageBox.Yes:
                logger.info("Save on Exit: Yes")
                self.save()
                event.accept()
            elif reply == QtWidgets.QMessageBox.No:
                logger.warning("Save on Exit: No")
                event.accept()
            else:
                logger.info("Save on Exit: Canceled")
                event.ignore()
                
        else:
            #no need to save confirm exit
            reply = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, "Confirm Exit",
                                          "Are you sure you wish to close this window?", 
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel, self).exec()
            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
                logger.info("Exit: Yes")
            else:
                event.ignore()
                                        
        logger.debug("completed")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    p = QtWidgets.QWidget()
    c = ContMyEntity(p)
    c.show()

    sys.exit(app.exec_())