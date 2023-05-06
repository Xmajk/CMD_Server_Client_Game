import mysql.connector
from Database.Database import Database

def set_everyone_offline(db:Database)->None:
    template:str="UPDATE player SET is_online=0 Where True;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template)
        db.mydb.commit()
            
def set_online(db:Database,username:str,value:int):
    data:tuple=(value,username)
    template:str="UPDATE player SET is_online=%s Where username=%s;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()