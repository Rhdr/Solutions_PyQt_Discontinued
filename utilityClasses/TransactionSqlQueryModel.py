from PyQt5 import QtSql, QtWidgets, QtCore, QtGui
import utilityClasses.dataStructures

class TransactionSqlQueryModel(QtSql.QSqlQueryModel):
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
        self.__llOrderBy = utilityClasses.dataStructures.LinkedListOfListsNoDuplicates()

        self.setQuery(selectQ)


    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            #return cell contents on edit
            if self.__dirty == True:
                return self.__dirtyRecord.field(index.column()).value()
            else:
                return super(TransactionSqlQueryModel, self).data(index, role)

        if role == QtCore.Qt.DisplayRole:
            #displayed data for each cell
            #if self.rowCountActual() == index.row() and self.__currentRowIndex == index.row():
            #    return self.__dirtyRecord.field(index.column()).value()
            #else:
            #    return super(TransactionSqlQueryModel, self).data(index, role)

            #displayed data for each cell & return the keyword New for newly added records
            if self.__dirty == True and self.__currentRowIndex == index.row():
                return self.__dirtyRecord.field(index.column()).value()
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
        super(TransactionSqlQueryModel, self).setQuery(self.query().lastQuery())

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

        #if still dirty notify user that the record could not be saved
        if self.__dirty:
            print("The record could not be saved")

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
            self.__dirtyRecord = self.record()
            self.requery()
            self.endRemoveRows()
            return True

            if query.lastError().number() > 0:
                print("SQL Append Error")
                print(query.executedQuery())
                print(query.lastError().text())
                raise Exception
                return False

        except Exception as e:
            self.__db.rollback()
            print("removeRows:", str(e))
            return False

    def rowCount(self, parent = None):
        #return extra row count + 1 if inserting a row
        return self.rowCountActual() + self.__newRowCount

    def rowCountActual(self):
        return super(TransactionSqlQueryModel, self).rowCount()

    def searchSQL(self, searchSQL):
        self.setQuery(searchSQL)

    def __printDirtyRecord(self):
        print("Printing dirty Record")
        for i in range(self.__dirtyRecord.count()):
            f = self.__dirtyRecord.field(i)
            print(f.name(), ":", f.value())

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
