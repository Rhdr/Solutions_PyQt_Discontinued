import utilityClasses.loggingSetup
logger = utilityClasses.loggingSetup.Logger.getLogger(__file__)

from PyQt5 import QtSql
class ObjectSql(object):
    #@staticmethod
    #def getLastInsertedId():
    #    return """SELECT SCOPE_IDENTITY()"""
    
    #Entity
    @staticmethod
    def getEntity_InsertSql():
        return """"""
    @staticmethod
    def getEntity_SelectSql():
        return """SELECT * 
                    FROM Entity"""
    @staticmethod
    def getEntity_Length(pk = 0, maxRowCount = 0):
        q = QtSql.QSqlQuery("""SELECT SUM(1) AS Counter
                                 FROM Entity""")
        q.first()
        return q.value(0)
    @staticmethod    
    def getEntity_UpdateSql():
        return """"""
    @staticmethod
    def getEntity_DeleteSql():
        return """"""
    
    
    #MyEntity
    @staticmethod
    def getMyEntity_InsertSql():
        #query returns lastInsertedID
        return """BEGIN TRANSACTION;
                        INSERT INTO Entity(Import_OldPk, Import_OldType, Name)
                        SELECT 0, 0, :name AS Name;
                        DECLARE @lastInsertedID INT
                        SET @lastInsertedID =  SCOPE_IDENTITY();
                        INSERT INTO MyEntity(Pk_MyEntityID)
                        SELECT @lastInsertedID;
                        SELECT @lastInsertedID;
                        COMMIT;"""
    @staticmethod
    def getMyEntity_HeaderLst():
        return ["Pk_MyEntityID", "Entity Name"]
    @staticmethod
    def getMyEntity_SelectSql():
        return """SELECT Pk_MyEntityID, Name 
                    FROM MyEntity LEFT JOIN
                    Entity ON MyEntity.Pk_MyEntityID = Entity.Pk_EntityID;"""
    @staticmethod
    def getMyEntity_Length(pk = 0, maxRowCount = 0):
        q = QtSql.QSqlQuery("""SELECT SUM(1) AS Counter
                                 FROM MyEntity""")
        q.first()
        return q.value(0)
    @staticmethod
    def getMyEntity_UpdateSql():
        return """UPDATE entity
                    SET Name = :name
                    WHERE Pk_EntityID = :pk_EntityID;"""
    @staticmethod
    def getMyEntity_DeleteSql():
        return """BEGIN TRANSACTION; 
                    DELETE FROM MyEntity  
                    WHERE Pk_MyEntityID IN (:pkStrLst)
                    DELETE FROM MyEntity
                    WHERE Pk_MyEntityID IN (:pkStrLst);
                    COMMIT;"""
                    
    #Owner
    @staticmethod
    def getOwner_InsertSql():
        return """"""
    @staticmethod
    def getOwner_SelectSql(pk = 0, maxRowCount = 0):
        return """SELECT PropertyOwner.Pk_PropertyOwnerID, Entity.Name, Entity.Surname, Entity.Initials, Entity.UserName, Entity.MonthlyStatement
                    FROM Entity INNER JOIN 
                    PropertyOwner ON Entity.Pk_EntityID = PropertyOwner.Pk_PropertyOwnerID"""
    @staticmethod
    def getOwner_Length(pk = 0, maxRowCount = 0):
        q = QtSql.QSqlQuery("""SELECT SUM(1) AS Counter
                                FROM Entity INNER JOIN 
                                PropertyOwner ON Entity.Pk_EntityID = PropertyOwner.Pk_PropertyOwnerID""")
        q.first()
        return q.value(0)
    @staticmethod
    def getOwner_UpdateSql():
        return """"""
    @staticmethod
    def getOwner_DeleteSql():
        return """"""

    
    #Consumer
    @staticmethod
    def getConsumer_InsertSql():
        return """"""
    @staticmethod
    def getConsumer_SelectSql(pk = 0, maxRowCount = 0):
        return """SELECT PropertyConsumer.Pk_PropertyConsumerID, Entity.Name, Entity.Surname, Entity.Initials, Entity.UserName, Entity.MonthlyStatement
                    FROM Entity INNER JOIN 
                    PropertyConsumer ON Entity.Pk_EntityID = PropertyConsumer.Pk_PropertyConsumerID"""
    @staticmethod
    def getConsumer_Length(pk = 0, maxRowCount = 0):
        q = QtSql.QSqlQuery("""SELECT SUM(1) AS Counter
                                FROM Entity INNER JOIN 
                                PropertyConsumer ON Entity.Pk_EntityID = PropertyConsumer.Pk_PropertyConsumerID""")
        q.first()
        return q.value(0)
    @staticmethod                   
    def getConsumer_UpdateSql():
        return """"""
    @staticmethod
    def getConsumer_DeleteSql():
        return """"""
    
    
    #Property
    @staticmethod
    def getProperty_InsertSql():
        return """"""
    @staticmethod
    def getProperty_SelectSql(pk = 0, maxRowCount = 0):
        return """SELECT * 
                    FROM Property"""
    @staticmethod
    def getProperty_Length(pk = 0, maxRowCount = 0):
        q = QtSql.QSqlQuery("""SELECT SUM(1) AS Counter 
                                FROM Property""")
        q.first()
        return q.value(0)
    @staticmethod
    def getProperty_UpdateSql():
        return """"""
    @staticmethod
    def getProperty_DeleteSql():
        return """"""
    
    
    #ConsumerPropertySelected
    @staticmethod
    def getConsumerPropertySelected_InsertSql():
        return """"""
    @staticmethod
    def getConsumerPropertySelected_SelectSql(pk = 0, maxRowCount = 0):
        return """SELECT * 
                    FROM ConsumerPropertySelected"""
    @staticmethod
    def getConsumerPropertySelected_Length(pk = 0, maxRowCount = 0):
        q = QtSql.QSqlQuery("""SELECT SUM(1) AS Counter 
                                FROM ConsumerPropertySelected""")
        q.first()
        return q.value(0)
    @staticmethod
    def getConsumerPropertySelected_UpdateSql():
        return """"""
    @staticmethod
    def getConsumerPropertySelected_DeleteSql():
        return """"""
    
    
    #OwnersProperty
    @staticmethod
    def getOwnersProperty_InsertSql():
        return """"""
    @staticmethod
    def getOwnersProperty_SelectSql():
        return """SELECT * 
                    FROM OwnersProperty"""
    @staticmethod
    def getOwnersProperty_Length(pk = 0, maxRowCount = 0):
        q = QtSql.QSqlQuery("""SELECT SUM(1) AS Counter 
                                FROM OwnersProperty""")
        q.first()
        return int(q.value(0))
    @staticmethod
    def getOwnersProperty_UpdateSql():
        return """"""
    @staticmethod
    def getOwnersProperty_DeleteSql():
        return """"""
    
if __name__ == "__main__":
    import models._databaseConnection
    models._databaseConnection.DBConnection().connect()
    
    q = QtSql.QSqlQuery(ObjectSql().getOwner_SelectSql())
    print(q.lastError().text())
    while (q.next()):
        print(q.value(2))
    print("getOwner_Length:", ObjectSql().getOwner_Length())
    
    q = QtSql.QSqlQuery(ObjectSql().getConsumerPropertySelected_SelectSql())
    print(q.lastError().text())
    while (q.next()):
        print(q.value(0))
    print("getConsumerPropertySelected_Length:", ObjectSql().getConsumerPropertySelected_Length())
    
    print(ObjectSql.getMyEntity_SelectSql())
