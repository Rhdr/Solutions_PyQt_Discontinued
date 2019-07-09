import utilityClasses.loggingSetup
logger = utilityClasses.loggingSetup.Logger.getLogger(__file__)

from PyQt5 import QtSql, QtCore
import models._databaseConnection
import models._objectSql


class MyEntity():
    __model = QtSql.QSqlQueryModel()
    
    def __init__(self):
        logger.debug("starting")
        pk = 0
        name = ""
        logger.info("object instantiated pk: " + str(pk) + " name:" + str(name))
        logger.debug("completed")
        
    @staticmethod
    def __setupModel():
        logger.debug("starting")
        models._databaseConnection.DBConnection.connect()
        try:
            MyEntity.__model.setQuery(models._objectSql.ObjectSql.getMyEntity_SelectSql())
        except Exception as e:
            logger.exception(MyEntity.__model.lastError().text())
            raise SyntaxError("modelMyEntity Sql query error: " + e)
        
        lst = models._objectSql.ObjectSql.getMyEntity_HeaderLst()
        for i, val in enumerate(lst):
            MyEntity.__model.setHeaderData(i, QtCore.Qt.Horizontal, val)
        logger.debug("completed")
        
    @staticmethod
    def getHeaderLst():
        logger.debug("starting")
        h = models._objectSql.ObjectSql.getMyEntity_HeaderLst()
        logger.debug("completed returning: " + str(h))
        return h
    
    @staticmethod
    def getModel():
        logger.debug("starting")
        MyEntity.__setupModel()
        m = MyEntity.__model
        logger.debug("completed returning: " + str(m))
        return m

    @staticmethod
    def refreshModel():
        logger.debug("starting")
        MyEntity.__setupModel()
        MyEntity.__model.clear()
        MyEntity.__model.setQuery(models._objectSql.ObjectSql.getMyEntity_SelectSql())
        logger.info("model refreshed")
        logger.debug("completed")
    
    @staticmethod
    def insertRecord(name):
        logger.debug("starting")
        models._databaseConnection.DBConnection().connect()
        try:
            q = QtSql.QSqlQuery()
            q.prepare(models._objectSql.ObjectSql.getMyEntity_InsertSql())
            q.bindValue(":name", name)
            q.exec()
            q.first()
        except:
            qErr = q.lastError().text()
            logger.warning(qErr)
            return [-1, qErr]
        logger.info("inserted Record, name: " + str(name))
        logger.debug("completed, lastInsertedId:" + str(q.value(0)) + " q.lastQuery(): " + str(q.lastQuery()))
        return  [q.value(0), ""]
    
    @staticmethod
    def updateRecord(pk, name):
        logger.debug("starting")
        models._databaseConnection.DBConnection().connect()
        try:
            q = QtSql.QSqlQuery()
            q.prepare(models._objectSql.ObjectSql.getMyEntity_UpdateSql())
            q.bindValue(":pk_EntityID", pk)
            q.bindValue(":name", name)
            q.exec()
        except Exception:
            qErr = q.lastError().text()
            logger.warning(qErr)
            return [-1, qErr]
        logger.info("updated Record: pk: " + str(pk) + " name: " + str(name))
        logger.debug("completed, q.lastQuery(): " + str(q.lastQuery()))
        return [pk, ""]
    
    @staticmethod
    def deleteRecords(pkLst):
        logger.debug("starting, pkLst: " + str(pkLst))
        models._databaseConnection.DBConnection().connect()        
        q = QtSql.QSqlQuery()
        q.prepare(models._objectSql.ObjectSql.getMyEntity_DeleteSql())
        qVarList = QtCore.QVariant(pkLst)
        q.bindValue(":pkStrLst", qVarList)
        try:
            q.execBatch()
        except Exception:
            logger.exception(q.lastError().text())
            return -1
        logger.info("deleted Record, pkLst: " + str(pkLst))
        logger.debug("completed, q.lastQuery(): " + str(q.lastQuery()))
        return pkLst
        
if __name__ == "__main__":
    from PyQt5 import QtWidgets
    import sys
    logger = utilityClasses.loggingSetup.Logger.getLogger(True, __file__)
    
    app = QtWidgets.QApplication(sys.argv)
    p = QtWidgets.QWidget()
    myEntity = MyEntity()
    #try:
    model = MyEntity.getModel()
    print(models._objectSql.ObjectSql.getMyEntity_SelectSql())
    print(model.rowCount())
    #except:
    #    print(model.lastError().text())
    #finally:
    #    myEntity.closeConnection()

    sys.exit(app.exec_())