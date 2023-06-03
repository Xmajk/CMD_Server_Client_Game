import mysql.connector

class Database:
    """
    Třída reprezentující připojení k databázi
    
    Atributy
    --------
    mydb : MySQLConnection
        instance třídy reprezentující připojení k MySQL databázi
    """

    def __init__(self) -> None:
        self.mydb=mysql.connector.connect(
            host="127.0.0.1",
            user="player_loc",
            password="heslojeveslo",
            database="game",
            auth_plugin='mysql_native_password'
        )
        print("Úspěšně jste se připojili k databázi")