import mysql.connector

class Database:
    """
    Třída reprezentující připojení k databázi
    
    Atributy
    --------
    mydb : MySQLConnection
        instance třídy reprezentující připojení k MySQL databázi
    """

    def __init__(self,host,user,password,database,auth_plugin) -> None:
        self.mydb=mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            auth_plugin=auth_plugin
        )
        print("Úspěšně jste se připojili k databázi")