import mysql.connector
from Database.Database import Database
from Others.Connection import Connection
from Gameobjects.Player import Player

def login(connect:Connection,username:str,password:str)->bool:
    db_password_tuple:tuple|None=get_password(connect.databaze,username)
    if db_password_tuple==None:
        return False
    db_player_id,db_password=db_password_tuple
    if db_password==password:
        connect.player=Player(username)
        return True
    return False

def get_password(db:Database,username:str)->tuple|None:
    data:tuple=(username,)
    template:str="SELECT id,passwd from player WHERE username=%s;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
        if db_output==None:
            return None
    return db_output
    
def register_user(db:Database,username:str,password:str)->None:
    data:tuple=(username,password)
    template:str="INSERT INTO player(username,passwd) values(%s,%s);"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()
        
def username_exists(db:Database,username:str)->bool:
    data:tuple=(username,)
    template:str="SELECT username from player WHERE username=%s;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
        if db_output==None:
            return False
    return True
