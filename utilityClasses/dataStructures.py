from PyQt5 import QtSql, QtCore, QtWidgets

class Node:
    def __init__(self, data = None, next = None):
        self.data = data
        self.next = next

class LinkedList(object):
    #create a normal linked list
    def __init__(self):
        self.root = Node()
        self.tail = Node()
        self.length = 0
        self._lastFindPtr = Node()
        self._lastFindPtrBack = Node()

    def addFront(self, data):
        newRoot = Node(data, self.root)
        self.root = newRoot
        self.length += 1

        if self.tail.data == None:
            #if only one node root == tail
            self.tail = self.root
            self.root.next = None

    def addBack(self, data):
        newNode = Node(data)
        self.tail.next = newNode
        self.tail = newNode
        self.length += 1

        if self.root.data == None:
            #if only one node root == tail
            self.root = self.tail

    def findValue(self, data):
        i = self.root
        index = 1
        if i.data == data:
            self._lastFindPtr = i
            self._lastFindPtrBack = i
            return index

        while i.next != None:
            index += 1
            self._lastFindPtrBack = i
            i = i.next

            if i.data == data:
                self._lastFindPtr= i
                return index

        return -1

    def removeNode(self, data):
        findPos = self.findValue(data)
        self._removeNodePos(findPos)

    def _removeNodePos(self, findPos):
        if findPos != -1:
            #test if value is found

            if self._lastFindPtr != self._lastFindPtrBack:
                #your deleting a value in the middel of the list
                self._lastFindPtrBack.next = self._lastFindPtr.next

            if self._lastFindPtr == self._lastFindPtrBack:
                #your deleting the root
                self.root = self.root.next

            if findPos == self.length:
                #your deleing the tail
                self.tail = self._lastFindPtrBack

            self.length -= 1
            del self._lastFindPtr

    def getList(self):
        #prevent empty list error
        try:
            i = self.root
            lst = []
            if i.data != None:
                lst.append(i.data)
            while i.next != None:
                i = i.next
                lst.append(i.data)
            return lst
        except:
            return []

class LinkedListOfLists(LinkedList):
    # create a linked list that compost of normal lists ex: [1,2] -> [3,2] -> [1,2] -> ...
    def __init__(self):
        super(LinkedListOfLists, self).__init__()

    def findValue(self, listData, listSearchColIndex):
        #search within a list stored in a linkedList
        try:
            i = self.root
            index = 1
            v = i.data

            if v is not None:
                if v[listSearchColIndex] == listData:
                    self._lastFindPtr= i
                    self._lastFindPtrBack = i
                    return index

                while i.next != None:
                    index += 1
                    self._lastFindPtrBack = i
                    i = i.next
                    v = i.data

                    if v[listSearchColIndex] == listData:
                        self._lastFindPtr= i
                        return index

            return -1
        except:
            return -1

    def removeNode(self, listData, listSearchColIndex):
        findPos = self.findValue(listData, listSearchColIndex)
        super(LinkedListOfLists, self)._removeNodePos(findPos)

class LinkedListOfListsNoDuplicates(LinkedListOfLists):
    # create a linked list that compost of normal lists with no duplicates on the indicated collumn ex: [1,2] -> [3,2] -> ...
    def __init__(self):
        super(LinkedListOfListsNoDuplicates, self).__init__()

    def addBack(self, data, dupplicateColCheck):
        print("LinkedListOfListsNoDuplicates.addBack not yet implemented")
        '''
        if self.findValue(data[dupplicateColCheck], dupplicateColCheck) != -1:
            #found a duplicate remove
            self.removeNode(data[dupplicateColCheck], dupplicateColCheck)
        super(LinkedListOfListsNoDuplicates, self).addBack(data)
        '''

    def addFront(self, data, dupplicateColCheck):
        if self.findValue(data[dupplicateColCheck], dupplicateColCheck) != -1:
            #found a duplicate remove
            self.removeNode(data[dupplicateColCheck], dupplicateColCheck)
        super(LinkedListOfListsNoDuplicates, self).addFront(data)

class SQLQueryCRUDObject(QtCore.QObject):
    def __init__(self, headersLst, db, parent):
        super(SQLQueryCRUDObject, self).__init__(parent)

        if type(db) == QtSql.QSqlDatabase:
            self.db = db
        else:
            raise Exception("db is not a QSqlDatabase")

        self.headersLst = self.__testForList(headersLst)
        self.headersLstLen = len(headersLst)

        self.selectQ = ""

        self.appendQ = ""
        self.appendQBindLst = []
        self.appendQDefaultValueLst = []

        self.updateQ = ""
        self.updateQBindLst = []
        self.updateQDefaultValueLst = []

        self.deleteQ = ""
        self.deleteQBindLst = []

    def __testForStr(self, s):
        if type(s) == str:
            return s
        else:
            raise Exception("s is not a string, its a ", type(s))

    def __testForList(self, l):
        if type(l) == list:
            return l
        else:
            raise Exception("l is not a list, its a ", type(l))

    def setSelectQ(self, q):
        self.selectQ = self.__testForStr(q)

    def setAppendQ(self, q, qBindLst, qDefaultValueLst):
        #if len(qBindLst) == self.headersLstLen:
        self.appendQ = self.__testForStr(q)
        self.appendQBindLst = self.__testForList(qBindLst)
        self.appendQDefaultValueLst = self.__testForList(qDefaultValueLst)
        #else:
        #    print(self.errBindNotMatching())
        #    raise Exception(self.errBindNotMatching())

    def setUpdateQ(self, q, qBindLst, qDefaultValueLst):
        #if len(qBindLst) == self.headersLstLen:
        self.updateQ = self.__testForStr(q)
        self.updateQBindLst = self.__testForList(qBindLst)
        self.updateQDefaultValueLst = self.__testForList(qDefaultValueLst)
        #else:
        #    print(self.errBindNotMatching())
        #    raise Exception(self.errBindNotMatching())

    def setDeleteQ(self, q, qBindLst):
        self.deleteQ = self.__testForStr(q)
        self.deleteQBindLst = self.__testForList(qBindLst)

    def allSet(self):
        s = len(self.selectQ)
        a = len(self.appendQ)
        u = len(self.updateQ)
        d = len(self.deleteQ)

        if s > 0 and a > 0 and u > 0 and d > 0:
            return True
        else:
            return False

    def errBindNotMatching(self):
        e = "Error: Query bind list length does not match the header list length"
        return e

class QSqlQueryExt(QtSql.QSqlQuery):
    def __init__(self, db):
        super(QSqlQueryExt, self).__init__(db)

    def prepareNBindLst(self, q, qBindLst, dirtyRecord):
        #prepare a query & bind values & handel null values
        self.prepare(q)
        for i in range(len(qBindLst)):
            f = dirtyRecord.field(dirtyRecord.indexOf(qBindLst[i]))
            bindValue = f.value()
            name = f.name()
            name = name[:2].lower()
            if name == "fk" or name == "pk":
                if bindValue == 0:
                    bindValue = QtCore.QVariant(QtCore.QVariant.Int)
            bind = ":" + qBindLst[i]

            self.bindValue(bind, bindValue)


    def getLastExecutedQuery(self):
        #resolve lastQuery bind values
        sql = str(self.lastQuery())
        dictBoundValues = self.boundValues()
        for key, value in dictBoundValues.items():
            sql = sql.replace(str(key), str(value))
        return sql

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
    '''LinkList Test'''
    ll = LinkedList()
    ll.addFront(1)
    ll.addFront(2)
    ll.addFront(3)
    print(ll.getList())
    print("Root:", ll.root.data)
    print("Tail:", ll.tail.data)
    print()

    ll.removeNode(1)
    print(ll.getList())
    print("Root:", ll.root.data)
    print("Tail:", ll.tail.data)
    print()


    ll = LinkedListOfListsNoDuplicates()
    ll.addFront([1, 1], 0)
    ll.addFront([2, 1], 0)
    ll.addFront([3, 0], 0)
    ll.addBack([4, 1], 0)
    print(ll.getList())
    print("length:", ll.length)
    print("Root:", ll.root.data)
    print("Tail:", ll.tail.data)
    print()

    ll.addFront([1, 1], 0)
    print(ll.getList())
    print("length:", ll.length)
    print("Root:", ll.root.data)
    print("Tail:", ll.tail.data)
    print()
    
    ll.addFront([4, 0], 0)
    print(ll.getList())
    print("length:", ll.length)
    print("Root:", ll.root.data)
    print("Tail:", ll.tail.data)
    print()

    ll.removeNode(4, 0)
    print(ll.getList())
    print("length:", ll.length)
    print("Root:", ll.root.data)
    print("Tail:", ll.tail.data)
    print()

    ll.removeNode(1,0)
    ll.removeNode(3,0)
    ll.removeNode(2,0)
    print(ll.getList())
    print("length:", ll.length)
    print("Root:", ll.root.data)
    print("Tail:", ll.tail.data)
    print()