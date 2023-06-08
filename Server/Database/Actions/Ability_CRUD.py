from typing import List,Tuple
from Database.Database import Database

def player_abilities(db:Database,username:str)->List[Tuple[str,int,int,int,int,bool,int,int,str]]:
    """
    Metoda, která vrací seznam herních schopností hráče.

    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské jméno hráče, pro kterého se mají získat schopnosti
        
    Vrací
    -----
    List[Tuple[str, int, int, int, int, bool, int, int, str]]
        Seznam obsahující tuple pro každou abilitu hráče
    """
    data:tuple=(username,)
    template:str="""SELECT a.nazev,a.hp,a.atk,a.speed,a.damage,a.effect,a.rounds_of_effect,a.mana_cost,a.code FROM
player p INNER JOIN(
abilities a INNER JOIN own_ability oa ON a.id=oa.id_ability)
ON p.id=oa.id_playera WHERE p.username=%s"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        return cursor.fetchall()
    
def get_ability(db:Database,code:str)->Tuple[str,int,int,int,int,bool,int,int,str]:
    """
    Metoda, která vrací detaily herní schopnosti na základě jejího kódu.

    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    code : str
        Kód schopnosti, pro kterou se mají získat detaily
        
    Vrací
    -----
    Tuple[str, int, int, int, int, bool, int, int, str]
        Tuple obsahující detaily abilit
    """
    data:tuple=(code,)
    template:str="""SELECT nazev,hp,atk,speed,damage,effect,rounds_of_effect,mana_cost,code FROM
abilities where code=%s"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        return cursor.fetchone()
    
def create_abiliti_owning(db:Database,username:str,ability_code:str)->None:
    """
    Metoda pro vytvoření záznamu o vlastnění ability hráčem.

    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské jméno hráče, který vlastní schopnost
    ability_code : str
        Kód schopnosti, kterou hráč vlastní
    """
    data:tuple=(username,ability_code)
    template:str="""INSERT INTO own_ability(id_playera,id_ability) values ((SELECT id FROM player WHERE username=%s LIMIT 1),(SELECT id FROM abilities where code=%s LIMIT 1))"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()
