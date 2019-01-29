from PyQt5 import QtSql, QtWidgets, QtCore, QtGui
import utilityClasses.dataStructures

class TransactionSqlQueryModel(QtSql.QSqlQueryModel):
    def __init__(self, sqlQueryCRUDObject, parent):
        super(TransactionSqlQueryModel, self).__init__(parent)
        self.__sqlQueryCRUDObject = sqlQueryCRUDObject
        self.__dirty = False
        self.__newRowCount = 1
        self.__dirtyRecord = QtSql.QSqlRecord()
        self.__currentRow = -1
        self.__currentRowIndex = 0
        self.__llOrderBy = utilityClasses.dataStructures.LinkedListOfListsNoDuplicates()
        self.setQuery(self.__sqlQueryCRUDObject.selectQ)

    def fieldIndex(self, colName):
        return self.__sqlQueryCRUDObject.headersLst.index(colName)

    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            #return cell contents on edit
            if self.__dirty == True:
                #f = self.__dirtyRecord.field(index.column())
                return self.__dirtyRecord.field(index.column()).value()
            else:
                return super(TransactionSqlQueryModel, self).data(index, role)

        if role == QtCore.Qt.DisplayRole:
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
                if self.__sqlQueryCRUDObject.headersLstLen == self.columnCount():
                    return self.__sqlQueryCRUDObject.headersLst[pos]
                else:
                    raise Exception("Incorrect header count, there should be " + str(self.columnCount() + " headers"))
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
        #self.__dirtyRecord = self.record(currentRow)
        self.updateDirtyRecord(currentRow)
        self.__currentRowIndex = currentRow
        return self.save(previousRow)

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
                rowLst = self.insertRow()
                if rowLst[0] == True:   #test for any errors
                    self.__dirty = False
            else:
                #print("Editing")
                rowLst = self.editRow()
                if rowLst[0] == True:   #test for any errors
                    self.__dirty = False
            #self.__dirtyRecord = self.record()
            #self.updateDirtyRecord()
            return rowLst
        else:
            return [True]

    def editRow(self):
        self.__sqlQueryCRUDObject.db.transaction()
        q = utilityClasses.dataStructures.QSqlQueryExt(self.__sqlQueryCRUDObject.db)
        q.prepareNBindLst(self.__sqlQueryCRUDObject.updateQ, self.__sqlQueryCRUDObject.updateQBindLst , self.__dirtyRecord)
        q.exec()
        self.__sqlQueryCRUDObject.db.commit()
        #print(q.lastQuery())
        self.requery()
        q.getLastExecutedQuery()

        if q.lastError().number() > 0:
            self.__sqlQueryCRUDObject.db.rollback()
            print("SQL Model removeRows Error")
            print(q.getLastExecutedQuery ())
            err = q.lastError().text()
            print(err)
            return [False, err]
        return [True]

    def insertRow(self, parent = QtCore.QModelIndex()):
        rows = 1
        pos = self.rowCount()

        self.beginInsertRows(parent, pos, pos + rows - 1)
        self.__sqlQueryCRUDObject.db.transaction()
        q = utilityClasses.dataStructures.QSqlQueryExt(self.__sqlQueryCRUDObject.db)
        q.prepareNBindLst(self.__sqlQueryCRUDObject.appendQ, self.__sqlQueryCRUDObject.appendQBindLst, self.__dirtyRecord)
        q.exec()
        self.__sqlQueryCRUDObject.db.commit()
        self.endInsertRows()
        self.requery()
        print(q.getLastExecutedQuery())
        if q.lastError().number() > 0:
            self.__sqlQueryCRUDObject.db.rollback()
            print("SQL Model insertRow Error")
            print(q.getLastExecutedQuery())
            err = q.lastError().text()
            print(err)
            return [False, err]
        return [True]

    def updateDirtyRecord(self, row = -1):
        if row != -1:
            self.__dirtyRecord = self.record(row)
        else:
            self.__dirtyRecord = self.record()

    def removeRows(self, pos, rows, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, pos, pos + rows - 1)
        for i in range(rows):
            #self.__dirtyRecord = self.record(pos + i)
            self.updateDirtyRecord(pos + i)
            self.__sqlQueryCRUDObject.db.transaction()
            q = utilityClasses.dataStructures.QSqlQueryExt(self.__sqlQueryCRUDObject.db)
            q.prepareNBindLst(self.__sqlQueryCRUDObject.deleteQ, self.__sqlQueryCRUDObject.deleteQBindLst, self.__dirtyRecord)
            q.exec()
            self.__sqlQueryCRUDObject.db.commit()
        self.updateDirtyRecord()
        self.endRemoveRows()
        self.requery()

        if q.lastError().number() > 0:
            self.__sqlQueryCRUDObject.db.rollback()
            print("SQL Model removeRows Error")
            print(q.getLastExecutedQuery())
            err = q.lastError().text()
            print(err)
            return [False, err]
        return [True]

    def rowCount(self, parent = None):
        #return extra row count + 1 if inserting a row
        return self.rowCountActual() + self.__newRowCount

    def rowCountActual(self):
        return super(TransactionSqlQueryModel, self).rowCount()

    def searchSQL(self, searchSQL):
        self.setQuery(searchSQL)
        '''q = utilityClasses.dataStructures.QSqlQueryExt(self.__sqlQueryCRUDObject.db)
        q.prepare(searchSQL)
        q.exec()
        print(q.getLastExecutedQuery())'''

    def __printDirtyRecord(self):
        print("Printing dirty Record")
        for i in range(len(self.__dirtyRecord)):
            field = self.__dirtyRecord.field(i)
            print("---------- field", i, field.name(), "--------")
            print("default value", field.defaultValue())
            print("is auto value", field.isAutoValue())
            print("is generated", field.isGenerated())
            print("is null", field.isNull())
            print("is read only", field.isReadOnly())
            print("is valid", field.isValid())
            print("length", field.length())
            print("precision", field.precision())
            print("required status", field.requiredStatus())
            print("type", field.type())
            print("type id", field.typeID())
            print("value", field.value())

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

            strOrder = strOrder + self.__sqlQueryCRUDObject.headersLst[column] + order
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

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
