import mysql.connector
from Gameobjects.Player import Player

class Database:
    def __init__(self) -> None:
        self.mydb=mysql.connector.connect(
            host="localhost",
            user="Player",
            password="NezukoKamado1",
            database="game"
        )
        print("Úspěšně jste se připojili k databázi")  
    
    def get_all_online_players_of_locaiotn(self,player:Player)->list:
        data:tuple=(player.username,player.username)
        template:str="""SELECT username from player inner join (SELECT location,building FROM player WHERE username=%s)tmp 
on player.location=tmp.location and player.building=tmp.building
WHERE player.username!=%s;"""
        with self.mydb.cursor() as cursor:
            cursor.execute(template,data)
            db_output:list=cursor.fetchall()
        return [element[0] for element in db_output]
        