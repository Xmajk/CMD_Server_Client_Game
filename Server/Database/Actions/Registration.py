from Database.Database import Database
import random
import string

def get_info_classes(db:Database)->list:
    data:tuple=()
    template:str="SELECT nazev,info from class;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:list=cursor.fetchall()
    return db_output

def get_info_class(db:Database,trida:str)->tuple:
    data:tuple=(trida,)
    template:str="SELECT nazev,hp,atk,speed,mana,info FROM class WHERE nazev=%s;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
    return db_output

def register(db:Database,username:str,trida:str,password:str)->None:
    data:tuple=(username,password,trida)
    template:str="INSERT INTO player (username, passwd, id_class) VALUES (%s, %s, (SELECT id FROM class WHERE nazev = %s));"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()

def code_in_database(db:Database,kod:str)->bool:
    data:tuple=(kod,)
    template:str="SELECT CASE WHEN EXISTS (SELECT * FROM player WHERE kod=%s) THEN 1 ELSE 0 END;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
    return db_output[0]==1

def generate_unique_code(db:Database)->str:
    code:str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    while code_in_database(db,code):
        code:str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return code