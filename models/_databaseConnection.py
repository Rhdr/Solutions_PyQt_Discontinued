import utilityClasses.loggingSetup
logger = utilityClasses.loggingSetup.Logger.getLogger(__file__)

from PyQt5 import QtSql

def connect():
    logger.debug("starting")
    try:
        isOpenBool = isOpen()
        if (isOpenBool == False):
            db = QtSql.QSqlDatabase.addDatabase("QODBC")
            db.setHostName("127.0.0.1") #192.168.2.5
            db.setDatabaseName("SolutionsDB")
            #db.setUserName("root")
            #db.setPassword("12345") #766Prop667
            
            isOpenBool = db.open() 
            if isOpenBool: #connect
                logger.info("DB Connection Created:" + str(isOpenBool))
            else:
                logger.exception("DB Connection Created:" + str(isOpenBool))         
                logger.exception(QtSql.QSqlDatabase().lastError().text())
        
        logger.debug("completed, db.isOpen: " + str(isOpenBool))             
    except Exception:
        logger.exception("DatabaseConnection Failed")
        isOpenBool = False
    finally:
        return isOpenBool
    
def isOpen():
    try:
        q = QtSql.QSqlQuery("SELECT 1")
        q.next()
        qVal = q.value(0)
        if qVal == 1:
            isOpen = True
        else:
            isOpen = False
    except:
        isOpen = False
    finally:
        return isOpen


if __name__ == "__main__":
    from PyQt5 import QtWidgets
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    print("isOpen? " + str(isOpen()))
    if connect():
        print("Db connected :)")
    else:
        print("Db not connected :(")
    print("isOpen? " + str(isOpen()))
    sys.exit(app.exec_())