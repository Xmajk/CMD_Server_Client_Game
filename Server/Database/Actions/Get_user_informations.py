import mysql.connector
from Gameobjects.Player import Player
from Database.Database import Database

def player_is_online(db:Database,username:str)->bool:
    """
    Metada vracící, jestli je uživatel online
    
    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské jméno od kterého chceme zjistit jestli je online
        
    Vrací
    -----
    bool
        Vrací jestli je uživatel online
    """
    data:tuple=(username,)
    template:str="SELECT is_online from player WHERE username=%s"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()[0]
    return db_output==1  

def get_location(db:Database,player:Player)->tuple:
    """
    Metada vracící, tuple lokace a budovy, kde je uživatel
    
    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    player : Player
        Uživatel od kterého chceme zjistit jeho lokaci a budovy
        
    Vrací
    -----
    Tuple[str,str]
        Tuple s dvěmi elementy
    """
    data:tuple=(player.username,)
    template:str="""SELECT l.nazev,b.nazev FROM 
(player p inner join lokace l on p.id_lokace=l.id)left join building b
on b.id=p.id_building WHERE p.username=%s;"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
    return db_output