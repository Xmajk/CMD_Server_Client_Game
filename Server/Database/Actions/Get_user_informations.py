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
    template:str="""SELECT l.nazev,b.nazev FROM 
(player p inner join lokace l on p.id_lokace=l.id)left join building b
on b.id=p.id_building WHERE p.username=%s;"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
    return db_output

def get_player_code(db:Database,username:str)->str:
    data:tuple=(username,)
    template:str="SELECT kod from player WHERE username=%s"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
    return db_output[0]