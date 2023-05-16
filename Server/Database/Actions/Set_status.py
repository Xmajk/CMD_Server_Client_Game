import mysql.connector
from Database.Database import Database

def set_everyone_offline(db:Database)->None:
    template:str="UPDATE player SET is_online=0 Where True;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template)
        db.mydb.commit()
            
def set_online(db:Database,username:str,value:int)->None:
    data:tuple=(value,username)
    template:str="UPDATE player SET is_online=%s Where username=%s;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()
        
def set_location(db:Database,username:str,lokace:str)->None:
    data:tuple=(lokace,username)
    template:str="UPDATE player SET id_lokace=(SELECT id FROM lokace where nazev=%s LIMIT 1) Where username=%s;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()
        
def set_building(db:Database,username:str,lokace:str|None=None,building:str|None=None)->None:
    if building==None:
        data:tuple=(username,)
        template:str="UPDATE player SET id_building=null WHERE username=%s;"
    else:
        data:tuple=(building,lokace,username)
        template:str="UPDATE player SET id_building=(SELECT b.id FROM lokace l inner join building b on l.id=b.id_lokace WHERE b.nazev=%s and l.nazev=%s LIMIT 1) WHERE username=%s;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()