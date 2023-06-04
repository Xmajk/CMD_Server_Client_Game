import mysql.connector
from Database.Database import Database
from typing import Union

def set_everyone_offline(db:Database)->None:
    """
    Metoda nastavuje všem hráčům stav is_online na hodnotu 0 (offline).

    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází

    Vrací 
    -----
    None
    """
    template:str="UPDATE player SET is_online=0 Where True;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template)
        db.mydb.commit()
            
def set_online(db:Database,username:str,value:int)->None:
    """
    Metoda nastavuje stav is_online pro daného hráče.

    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské jméno hráče
    value : int
        Hodnota stavu is_online (0 - offline, 1 - online)

    Vrací 
    -----
    None
    """
    data:tuple=(value,username)
    template:str="UPDATE player SET is_online=%s Where username=%s;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()
        
def set_location(db:Database,username:str,lokace:str)->None:
    """
    Metoda nastavuje lokaci pro daného hráče.

    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské jméno hráče
    lokace : str
        Název lokace, kterou chcete nastavit hráči

    Vrací 
    -----
    None
    """
    data:tuple=(lokace,username)
    template:str="UPDATE player SET id_lokace=(SELECT id FROM lokace where nazev=%s LIMIT 1) Where username=%s;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()
        
def set_building(db:Database,username:str,lokace:Union[str,None]=None,building:Union[str,None]=None)->None:
    """
    Metoda nastavuje budovu pro daného hráče.

    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské jméno hráče
    lokace : str, optional
        Název lokace, ve které se nachází budova (výchozí hodnota je None)
    building : str, optional
        Název budovy, kterou chcete nastavit hráči (výchozí hodnota je None)

    Vrací 
    -----
    None
    """
    if building==None:
        data:tuple=(username,)
        template:str="UPDATE player SET id_building=null WHERE username=%s;"
    else:
        data:tuple=(building,lokace,username)
        template:str="UPDATE player SET id_building=(SELECT b.id FROM lokace l inner join building b on l.id=b.id_lokace WHERE b.nazev=%s and l.nazev=%s LIMIT 1) WHERE username=%s;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()