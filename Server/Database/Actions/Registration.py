from Database.Database import Database
import random
import string

def get_info_classes(db:Database)->list:
    """
    Metoda získává informace o všech třídách (classes).

    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází

    Vrací 
    -----
    list
        Seznam tuplů obsahujících název třídy a informace o třídě
    """
    data:tuple=()
    template:str="SELECT nazev,info from class;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:list=cursor.fetchall()
    return db_output

def get_info_class(db:Database,trida:str)->tuple:
    """
    Metoda získává informace o konkrétní třídě (class).

    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    trida : str
        Název třídy, pro kterou se mají získat informace

    Vrací 
    -----
    tuple
        Tuple obsahující název třídy, životy (hp), útok (atk), rychlost (speed), mana (mana) a informace o třídě
    """
    data:tuple=(trida,)
    template:str="SELECT nazev,hp,atk,speed,mana,info FROM class WHERE nazev=%s;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
    return db_output

def register(db:Database,username:str,trida:str,password:str)->None:
    """
    Metoda registruje nového hráče do databáze.

    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské jméno hráče
    trida : str
        Název třídy, kterou si hráč zvolil
    password : str
        Heslo hráče

    Vrací 
    -----
    None
    """
    data:tuple=(username,password,trida)
    template:str="call mp_register(%s,%s,%s);"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()

def code_in_database(db:Database,kod:str)->bool:
    """
    Metoda ověřuje, zda se kód nachází v databázi.

    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    kod : str
        Kód, který se má ověřit

    Vrací 
    -----
    bool
        True, pokud se kód nachází v databázi, jinak False
    """
    data:tuple=(kod,)
    template:str="SELECT CASE WHEN EXISTS (SELECT * FROM player WHERE kod=%s) THEN 1 ELSE 0 END;"
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
    return db_output[0]==1