from PyQt5 import QtSql, QtWidgets, QtCore, QtGui
import utilityClasses.dataStructures

"""
def runTransactionQueries(queryAndBindLst, db, record):
    # this code can be optimized by using a record class to replace the __dirtyRecord dict
    try:
        # begin transaction
        db.transaction()

        # setup transaction queries and run each query
        query = QtSql.QSqlQuery(db)
        for q, qry in enumerate(queryAndBindLst):  # for each query
            for b, bind in enumerate(queryAndBindLst[q]):  # for each binding(b(0) contains the query the rest bindings)
                if b == 0:
                    # first list value contains the query
                    query.prepare(queryAndBindLst[q][0])
                else:
                    # binding bind query values
                    # print("Bind:", bind, "b:", b)
                    f = record.field(record.indexOf(bind.strip(':')))
                    # print("bind value f:", f.value())
                    query.bindValue(bind, f.value())
            # print("SQL:", query.executedQuery())
            query.exec()
        # end transaction
        db.commit()
        return True

        if query.lastError().number() > 0:
            print("Save SQL Error")
            print(query.executedQuery())
            print(query.lastError().text())
            return False

    except:
        __db.rollback()
        return False


class TransactionSqlQueryModel(QtSql.QSqlQueryModel):
    def __init__(self, headersLst, db, parent = None):
        QtSql.QSqlQueryModel.__init__(self, parent)
        self.__dictOrderBy = dict()
        self.__dirtyRecord = QtSql.QSqlRecord()
        self.__dirty = False    #used to flag record as dirty
        self.__currentRowIndex = 0
        self.__prevRowIndex = 0
        self.__extraRowCount = 1 #insert new record line
        self.__llOrderBy = utilityClasses.dataStructures.LinkedListOfListsNoDuplicates()
        self.__headers = headersLst
        self.__db = db

        #multiple queries/transactions can be stored to be run for appends or updates
        self.__strAppQueryAndBindingLst = [[]]
        self.__strUpdateQueryAndBindingLst = [[]]
        self.__strDelQueryAndBindingLst = [[]]

    def searchSQL(self, searchSQL):
        super(TransactionSqlQueryModel, self).setQuery(searchSQL)

    def orderBy(self, colIndex, order):
        # remove the curent orderby, determine the new order then build sql & execute (sort)

        # Col, Order(A/D = 0/1)
        self.__llOrderBy.addFront([colIndex, order], 0)

        #remove orderby
        currentQuery = self.query().lastQuery()
        pOrderBy = currentQuery.find(" ORDER BY")
        #test for not found
        if pOrderBy == -1:
            pOrderBy = 0

        #fix negative lenghts
        lenCurrentQueryNoOrder = len(currentQuery) - (len(currentQuery) - pOrderBy)
        if lenCurrentQueryNoOrder <= 0:
            lenCurrentQueryNoOrder = len(currentQuery)

        currentQueryNoOrder = str(currentQuery[0:(lenCurrentQueryNoOrder)])

        #build & execute
        #for i in range(self.__llOrderBy.length):
        itr = self.__llOrderBy.root
        i = 0
        strOrder = ""
        while True:
        #while itr.next != None:
            column = itr.data[0]
            order = itr.data[1]

            # determine new sort order
            if order == 0:
                order = ""
            else:
                order = " DESC"

            if strOrder != "":
                strOrder = strOrder + ", "

            strOrder = strOrder + self.__headers[column] + order
            itr = itr.next
            i += 1

            if itr == None: #do while loop exit
                break

        if strOrder == "":
            orderBy = ""
        else:
            orderBy = " ORDER BY "

        strQ = currentQueryNoOrder + orderBy + strOrder
        super(TransactionSqlQueryModel, self).setQuery(strQ)
        #print(strQ)

    def escapePressed(self, currentRow):
        #print("currentRow:", currentRow)
        #print("rowCountActual:", self.rowCountActual())
        if currentRow == self.rowCountActual():
            print("run")
            self.removeRows(currentRow, 1)

    def insertRow(self, currentRow):
        #insert a blank row
        #print("index.row():", index.row(), "self.rowCountActual():", self.rowCountActual())
        if currentRow == self.rowCountActual():
            self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount() + 1)
            if self.__extraRowCount <= 1:
                #prevent multiple rows to be added
                self.__extraRowCount += 1
            #self.layoutChanged.emit()
            self.endInsertRows()
            self.layoutChanged.emit()
            return True
        else:
            return False

    def rowCount(self, parent = None):
        #return extra row count + 1 if inserting a row
        return self.rowCountActual() + self.__extraRowCount

    def rowCountActual(self):
        return super(TransactionSqlQueryModel, self).rowCount()

    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            #return cell contents on edit
            if self.__dirty == True and self.__currentRowIndex == index.row():
                return self.__dirtyRecord.field(index.column()).value()
            else:
                return super(TransactionSqlQueryModel, self).data(index, role)

        if role == QtCore.Qt.DisplayRole:
            #displayed data for each cell & return the keyword New for newly added records
            if self.__dirty == True and self.__currentRowIndex == index.row():
                return self.__dirtyRecord.field(index.column()).value()
            elif index.row() == self.rowCountActual() and index.column() == 1:
                return "*(New)"
            else:
                return super(TransactionSqlQueryModel, self).data(index, role)

    def setData(self, index, value, role=None):
        #cach any user changes to self.__dirtyRecord & mark as dirty
        if role == QtCore.Qt.EditRole:
            self.__dirty = True
            self.__dirtyRecord.setValue(index.column(), value)
        return False

    def flags(self, qModelIndex):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def requery(self):
        super(TransactionSqlQueryModel, self).setQuery(self.query().lastQuery())

    def save(self):
        #if dirty save, either append new records or edit old records
        if self.__dirty == True:
            print("'Saving'...")
            #print("self.__currentRowIndex:", self.__currentRowIndex)
            #print("self.rowCount() - 1", self.rowCount() - 1)
            if self.__prevRowIndex == self.rowCountActual():
                #New Row Append
                print("Appending")
                runTransactionQueries(self.__strAppQueryAndBindingLst, self.__db, self.__dirtyRecord)
                self.__insertNextNewRow = False
                self.layoutChanged.emit()   #new empty row to be removed

            else:
                #Old Row Update
                print("editing")
                if runTransactionQueries(self.__strUpdateQueryAndBindingLst, self.__db, self.__dirtyRecord) == True:
                    msg = QtWidgets.QMessageBox()
                    msg.setText("Save Error")
                    self.layoutChanged.emit()
            self.__dirty = False

            #update
            self.requery()
        else:
            print("There was no changes and thus no need to save")



    def setUpdateQuery(self, strQueryAndBindList):
        #setter used to update existings rows
        self.__strUpdateQueryAndBindingLst = strQueryAndBindList

    def setAppendQuery(self, strQueryAndBindList):
        #setter used to append/insert into a new row
        self.__strAppQueryAndBindingLst = strQueryAndBindList

    def setDeleteQuery(self, strQueryAndBindList):
        #setter used to append/insert into a new row
        self.__strDelQueryAndBindingLst = strQueryAndBindList

    def setColumns(self, strBindColumns):
        #setter used to connect both the update & append queries with the view's values
        self.__queryBindColumns = strBindColumns

    def setTableView(self, tableView):
        tableView.selectionModel().currentRowChanged.connect(self.rowChanged)
        tableView.itemDelegate().commitData.connect(self.__delegateCommit)

    def __delegateCommit(self):
        #mark record as dirty after edit & before save
        self.__dirtyRecord["Dirty"] = True

    def rowChanged(self, newRowIndex):
        #save record & record nr/index on rowchange, controllers need to connect their models to the rowChanged method
        #print("newRowIndex:", newRowIndex)
        self.__prevRowIndex = self.__currentRowIndex
        self.__currentRowIndex = newRowIndex
        self.__updateDirtyRecord(newRowIndex)
        self.save()
        if self.__extraRowCount > 1:
            self.__extraRowCount = 1

    def __updateDirtyRecord(self, index):
        #save a copy for the current index record into a temp record called __dirtyRecord
        self.__dirtyRecord = self.record(index)
        #for r in range(self.__dirtyRecord.count()):
        #    f = self.__dirtyRecord.field(r)
        #    print("f:", f.value())

    def headerData(self, pos, qt_Orientation, role=None):
        if role == QtCore.Qt.DisplayRole:
            if qt_Orientation == QtCore.Qt.Horizontal:
                # column lables
                if len(self.__headers) == self.columnCount():
                    return self.__headers[pos]
                else:
                    return "Incorrect header count, there should be " + str(self.columnCount() + " headers")
            else:
                # rows labels
                return pos + 1

    def columnCount(self, parent=None):
        return super(TransactionSqlQueryModel, self).columnCount()

    def removeRows(self, pos, rows, parent = QtCore.QModelIndex()):
        try:
            self.beginRemoveRows(parent, pos, pos + rows-1)
            for i in range(rows):
                self.__updateDirtyRecord(pos + i)
                #print("pos", pos + i)
                runTransactionQueries(self.__strDelQueryAndBindingLst, self.__db, self.__dirtyRecord)
            self.endRemoveRows()
            self.requery()
            return True
        except:
            return False

    def setSelectQuery(self, query):
        super(TransactionSqlQueryModel, self).setQuery(query)

    def setQuery(self, doNotUse):
        # disable setQuery
        raise Exception("setQuery can not be directly whilst using this model, use setSelectQuery, setAppendQuery, setUpdateQuery or setDeleteQuery instead")
"""

class TransactionSqlQueryModel_NewRecord(QtSql.QSqlQueryModel):
    def __init__(self, headersLst, selectQ, appQueryNBindList, updQueryNBindList, deleteQueryNBindLst, db, parent = None):
        QtSql.QSqlQueryModel.__init__(self, parent)
        self.__headers = headersLst
        self.__db = db
        self.__dirty = False
        self.__newRowCount = 1
        self.__dirtyRecord = QtSql.QSqlRecord()
        self.__appQueryNBindList = appQueryNBindList
        self.__updQueryNBindList = updQueryNBindList
        self.__deleteQueryNBindLst = deleteQueryNBindLst
        self.__currentRowIndex = 0

        self.setQuery(selectQ)


    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            #return cell contents on edit
            if self.__dirty == True:
                return self.__dirtyRecord.field(index.column()).value()
            else:
                return super(TransactionSqlQueryModel_NewRecord, self).data(index, role)

        if role == QtCore.Qt.DisplayRole:
            #displayed data for each cell
            #if self.rowCountActual() == index.row() and self.__currentRowIndex == index.row():
            #    return self.__dirtyRecord.field(index.column()).value()
            #else:
            #    return super(TransactionSqlQueryModel_NewRecord, self).data(index, role)

            #displayed data for each cell & return the keyword New for newly added records
            if self.__dirty == True and self.__currentRowIndex == index.row():
                return self.__dirtyRecord.field(index.column()).value()
            else:
                return super(TransactionSqlQueryModel_NewRecord, self).data(index, role)

    def setData(self, index, value, role=None):
        #cach any user changes to self.__dirtyRecord & mark as dirty
        if role == QtCore.Qt.EditRole:
            self.__dirty = True
            self.__dirtyRecord.setValue(index.column(), value)
        return False

    def flags(self, qModelIndex):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, pos, qt_Orientation, role=None):
        if role == QtCore.Qt.DisplayRole:
            if qt_Orientation == QtCore.Qt.Horizontal:
                # column lables
                if len(self.__headers) == self.columnCount():
                    return self.__headers[pos]
                else:
                    return "Incorrect header count, there should be " + str(self.columnCount() + " headers")
            else:
                # rows labels
                if pos <= self.rowCountActual() - 1:
                    return pos + 1
                elif pos == self.rowCountActual():
                    return "..."
                else:
                    return "*"

    def rowChanged(self, currentRow, previousRow):
        #save record & record nr/index on rowchange, controllers need to connect their views to the rowChanged method
        self.__dirtyRecord = self.record(currentRow)
        self.__currentRowIndex = currentRow
        self.save(previousRow)

    def requery(self):
        super(TransactionSqlQueryModel_NewRecord, self).setQuery(self.query().lastQuery())

    def insertNewBlankRows(self):
        self.__newRowCount += 1
        if self.__newRowCount > 2:
            self.__newRowCount = 2
        self.layoutChanged.emit()

    def resetNewBlankRows(self):
        #self.__newRowCount -= 1
        #if self.__newRowCount < 0:
        self.__newRowCount = 1
        self.layoutChanged.emit()

    def save(self, previousRow = True):
        #print("Save action recevied")
        if self.__dirty == True:
            if previousRow + 1 >= self.rowCountActual() + 1:
                #print("Appending")
                if self.insertRow() == True:
                    self.__dirty = False
            else:
                #print("Editing")
                if self.editRow() == True:
                    self.__dirty = False
            self.__dirtyRecord = self.record()
        else:
            print("row not dirty no need to save")

    def editRow(self):
        try:
            self.__db.transaction()
            q = utilityClasses.dataStructures.QSqlQueryExt(self.__db)
            q.prepareNBindLst(self.__updQueryNBindList, self.__dirtyRecord)
            q.exec()
            self.__db.commit()
            self.requery()
            return True

            if query.lastError().number() > 0:
                print("SQL Append Error")
                print(query.executedQuery())
                print(query.lastError().text())
                raise Exception
                return False
        except Exception as e:
            self.__db.rollback()
            print(str(e))
            return False

    def insertRow(self, parent = QtCore.QModelIndex()):
        rows = 1
        pos = self.rowCount()
        try:
            self.beginInsertRows(parent, pos, pos + rows - 1)
            self.__db.transaction()
            q = utilityClasses.dataStructures.QSqlQueryExt(self.__db)
            q.prepareNBindLst(self.__appQueryNBindList, self.__dirtyRecord)
            q.exec()
            self.__db.commit()
            self.endInsertRows()
            self.requery()
            return True

            if query.lastError().number() > 0:
                print("SQL Append Error")
                print(query.executedQuery())
                print(query.lastError().text())
                raise Exception
                return False
        except Exception as e:
            self.__db.rollback()
            print(str(e))
            return False

    def removeRows(self, pos, rows, parent = QtCore.QModelIndex()):
        try:
            self.beginRemoveRows(parent, pos, pos + rows - 1)
            for i in range(rows):
                self.__dirtyRecord = self.record(pos + i)
                self.__db.transaction()
                q = utilityClasses.dataStructures.QSqlQueryExt(self.__db)
                q.prepareNBindLst(self.__deleteQueryNBindLst, self.__dirtyRecord)
                q.exec()
                self.__db.commit()
            self.endRemoveRows()
            self.__dirtyRecord = self.record()
            self.requery()
            return True

            if query.lastError().number() > 0:
                print("SQL Append Error")
                print(query.executedQuery())
                print(query.lastError().text())
                raise Exception
                return False

        except Exception as e:
            self.__db.rollback()
            print(str(e))
            return False

    def rowCount(self, parent = None):
        #return extra row count + 1 if inserting a row
        return self.rowCountActual() + self.__newRowCount

    def rowCountActual(self):
        return super(TransactionSqlQueryModel_NewRecord, self).rowCount()

    def __printDirtyRecord(self):
        print("Printing dirty Record")
        for i in range(self.__dirtyRecord.count()):
            f = self.__dirtyRecord.field(i)
            print(f.name(), ":", f.value())


"""
Edit Row
        rows = 1
        pos = self.rowCount()
        self.beginInsertRows(parent, pos, pos + rows - 1)
        try:
            self.__db.transaction()
            q = QtSql.QSqlQuery()
            q.prepare(appQueryAndBindingLst[0])
            for i in range(len(appQueryAndBindingLst - 1))  #-1 because first value is the query
                q.bindValue(appQueryAndBindingLst[i], ":")
            q.exec()
            self.endInsertRows()

            self.__db.commit()
            return True

            if query.lastError().number() > 0:
                print("SQL Error")
                print(query.executedQuery())
                print(query.lastError().text())
                return False
        except:
            __db.rollback()
            return False
"""


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
