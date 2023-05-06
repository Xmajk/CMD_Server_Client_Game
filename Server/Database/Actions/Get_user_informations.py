import mysql.connector
from Gameobjects.Player import Player
from Database.Database import Database

def player_is_online(db:Database,username:str)->bool:
    data:tuple=(username,)
    template:str="SELECT is_online from player WHERE username=%s"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()[0]
    return db_output==1  

def get_location(db:Database,player:Player)->tuple:
    data:tuple=(player.username,)
    template:str="SELECT location,building from player WHERE username=%s"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
    return db_output