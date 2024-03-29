from Database.Database import Database
from typing import List,Tuple

def all_using_to_inventory(db:Database,username:str)->None:
    """
    Metoda, která všem předmětům v inventáře uživatele nastaví is_using na 0
    
    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské jméno uživatele, kterému patří inventář
    
    Vrací 
    -----
    None
    """
    data:Tuple[str]=(username,)
    template:str="""UPDATE own_item SET is_using=0 WHERE id_playera=(SELECT id FROM player WHERE username=%s LIMIT 1);"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()
        
def print_inventory(db:Database,username:str)->List[Tuple[str,str,int]]:
    """
    Metoda vracící list tuplů s informacemi o itemech.
    
    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské jméno uživatele, kterému patří inventář
    
    Vrací 
    -----
    List[Tuple[str,str,int]]
        List tuplů s informacemi o itemech ve formátu (název_itemu,kód_itemu,počet_itemů_v_inventáři)
    """
    data:Tuple[str]=(username,)
    template:str="""SELECT i.nazev,i.kod,count(o.id) FROM
item i inner join 
(player p inner join own_item o on p.id=o.id_playera)
on i.id=o.id_itemu where o.is_using=0 and p.username=%s GROUP BY i.nazev,i.kod;"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:List[Tuple[str,str,int]]=cursor.fetchall()
    return db_output

def get_inventory_2(db:Database,username:str)->List[Tuple[str,str,int]]:
    """
    Metoda vracící listu tupů s informace jednotlivých předmětů v inventáři
    
    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské jméno uživatele, kterému patří inventář
        
    Vrací
    -----
    List[Tuple[str,str,int]]
        List tuplů s informacemi jednotlivých předmětů ve formátu (název_itemu,kód_itemu,jestli_je_předmět_používán)
    """
    data:Tuple[str]=(username,)
    template:str="""SELECT i.nazev,i.kod,o.is_using FROM
item i inner join 
(player p inner join own_item o on p.id=o.id_playera)
on i.id=o.id_itemu where p.username=%s;"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:List[Tuple[str,str,int]]=cursor.fetchall()
    return db_output

def create_owning(db:Database,username:str,item_code:str)->None:
    """
    Metoda vytvoří záznam o vlastnictví předmětu pro daného uživatele.
    
    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské jméno uživatele, kterému bude předmět přiřazen
    item_code : str
        Kód předmětu, který bude vlastněn
    
    Vrací 
    -----
    None
    """
    data: T
    data:Tuple[str]=(username,item_code)
    template:str="""insert into own_item(id_playera,id_itemu) values ((SELECT id FROM player WHERE username=%s LIMIT 1),(SELECT id FROM item WHERE kod=%s LIMIT 1))"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()

def delete_owning(db:Database,username:str,item_code:str)->None:
    """
    Metoda odstraní záznam o vlastnictví předmětu daného uživatele.
    
    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské jméno uživatele, kterému předmět patří
    item_code : str
        Kód předmětu, který bude odstraněn
    
    Vrací 
    -----
    None
    """
    data:Tuple[str]=(username,item_code)
    template:str="""DELETE FROM own_item WHERE id_playera=(SELECT id FROM player WHERE username=%s LIMIT 1) and id_itemu=(SELECT id FROM item WHERE kod=%s LIMIT 1) LIMIT 1"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()
        
def change_owning_put_on(db:Database,username:str,item_code:str,put_in:bool)->None:
    """
    Metoda změní stav používání předmětu daného uživatele.
    
    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské jméno uživatele, kterému předmět patří
    item_code : str
        Kód předmětu, u kterého se bude měnit stav používání
    put_in : bool
        True, pokud se předmět má začít používat; False, pokud se má přestat používat
    
    Vrací 
    -----
    None
    """
    data:Tuple[str]=(int(put_in),int(not put_in),username,item_code)
    template:str="""UPDATE own_item SET is_using=%s WHERE is_using=%s and id_playera=(SELECT id FROM player WHERE username=%s LIMIT 1) and id_itemu=(SELECT id FROM item WHERE kod=%s LIMIT 1)"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()
        
from Gameobjects.Item import Item 
def get_item(db:Database,item_code:Item)->Tuple[str,str,str,int,int,int,int,str]:
    """
    Metoda získá informace o předmětu na základě jeho kódu.
    
    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    item_code : Item
        Kód předmětu, pro který se mají získat informace
    
    Vrací 
    -----
    Tuple[str, str, str, int, int, int, int, str]
        Tuple obsahující informace o předmětu ve formátu (název, kód, název, hp, damage, mana, speed, ability_info)
    """
    data:Tuple[str]=(item_code,)
    template:str="""SELECT nazev,kod, nazev, player_hp,player_damage,player_mana,player_speed,ability_info FROM item WHERE kod=%s;"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
    return db_output