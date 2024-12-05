from sqlite3 import connect,Row
import sqlite3

database:str = 'book.db'

def postprocess(sql:str)->bool:
    try:
        #connect to database
        db:object = connect(database)
        #create a cursor
        cursor:object = db.cursor()
        #execute the sql command
        cursor.execute(sql)
        #commit the command
        db.commit()
        #close the database
        cursor.close()
        db.close()
        return True if cursor.rowcount>0 else False
    except sqlite3.IntegrityError as e:
        return {"error":str(e)}
    
def getprocess(sql:str)->list:
    #connect to database
    db:object = connect(database)
    #create a cursor
    cursor:object = db.cursor()
    #convert the record into an object
    cursor.row_factory = Row
    #execute the sql command
    cursor.execute(sql)
    #fetch all the data
    data:list = cursor.fetchall()
    #close the database connection
    cursor.close()
    db.close()
    #return the collected data
    return data