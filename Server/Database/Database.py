import mysql.connector

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

    def get_user(self,user_id:int)->list:
        pass