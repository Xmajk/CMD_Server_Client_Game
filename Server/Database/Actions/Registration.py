from Database.Database import Database

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
    