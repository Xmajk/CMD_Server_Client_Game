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
        
    def get_password(self,username:str)->tuple|None:
        data:tuple=(username,)
        template:str="SELECT id,passwd from player WHERE username=%s"
        with self.mydb.cursor() as cursor:
            cursor.execute(template,data)
            db_output:tuple=cursor.fetchone()
            if db_output==None:
                return None
        return db_output

    def set_everyone_offline(self)->None:
        template:str="UPDATE player SET is_online=0 Where True;"
        with self.mydb.cursor() as cursor:
            cursor.execute(template)
            self.mydb.commit()
            
    def set_online(self,username:str,value:int):
        data:tuple=(value,username)
        template:str="UPDATE player SET is_online=%s Where username=%s;"
        with self.mydb.cursor() as cursor:
            cursor.execute(template,data)
            self.mydb.commit()

    def player_is_online(self,username:str)->bool:
        data:tuple=(username,)
        template:str="SELECT is_online from player WHERE username=%s"
        with self.mydb.cursor() as cursor:
            cursor.execute(template,data)
            db_output:tuple=cursor.fetchone()[0]
        return db_output==1    
    
    def get_location(self,player:Player)->tuple:
        data:tuple=(player.username,)
        template:str="SELECT location,building from player WHERE username=%s"
        with self.mydb.cursor() as cursor:
            cursor.execute(template,data)
            db_output:tuple=cursor.fetchone()
        return db_output