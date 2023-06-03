import mysql.connector
from Database.Database import Database
from Others.Connection import Connection
from Gameobjects.Player import Player
from typing import Union

def login(connect:Connection,username:str,password:str)->bool:
    """
    Metoda, která vrací jestli je přihlášení správné

    Parametry
    ---------
    connect : Connection
        Instance třídy Connection, která reprezentuje spojení s uživatelem
    username : str
        Uživatelské jméno
    password : str
        Heslo, které má účet s uživatelský jménem
        
    Vrací
    -----
    bool
        Boolovská hodnota jestli je přihlášení validní.
    """
    db_password_tuple:Union[tuple,None]=get_password(connect.databaze,username)
    if db_password_tuple==None:
        return False
    db_player_id,db_password=db_password_tuple
    if db_password==password:
        connect.player=Player(username)
        return True
    return False

def get_password(db:Database,username:str)->Union[tuple,None]:
    """
    Metoda, která vrací id a heslo účtu se zadaným uživatelským jménem nebo None
    
    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské jméno od kterého chceme heslo
        
    Vrací
    -----
    Tuple[int,str]|None
        hodnoty int=id str=heslo usernamu
    """
    data:tuple=(username,)
    template:str="SELECT id,passwd from player WHERE username=%s;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
        if db_output==None:
            return None
    return db_output
        
def username_exists(db:Database,username:str)->bool:
    """
    Metoda, která vrací boolovskou hodnotu, jestli username existuje
    
    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské, které chceme zjistit jestli existuje
        
    Vrací
    -----
    bool
        Hodnota, jestli username existuje
    """
    data:tuple=(username,)
    template:str="SELECT username from player WHERE username=%s;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
        if db_output==None:
            return False
    return True
