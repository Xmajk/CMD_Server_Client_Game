import mysql.connector

class Database:
    def __init__(self) -> None:
        self.mydb=mysql.connector.connect(
            host="localhost",
            user="Player",
            password="NezukoKamado1"
        )
        print("Úspěšně jste se připojili k databázi")
        
    def get_password(self,username:str)->str|None:
        return None