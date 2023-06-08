from typing import List,Tuple
from Database.Database import Database

def player_abilities(db:Database,username:str)->List[Tuple[str,int,int,int,int,bool,int,int,str]]:
    data:tuple=(username,)
    template:str="""SELECT a.nazev,a.hp,a.atk,a.speed,a.damage,a.effect,a.rounds_of_effect,a.mana_cost,a.code FROM
player p INNER JOIN(
abilities a INNER JOIN own_ability oa ON a.id=oa.id_ability)
ON p.id=oa.id_playera WHERE p.username=%s"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        return cursor.fetchall()
    
def get_ability(db:Database,code:str)->Tuple[str,int,int,int,int,bool,int,int,str]:
    data:tuple=(code,)
    template:str="""SELECT nazev,hp,atk,speed,damage,effect,rounds_of_effect,mana_cost,code FROM
abilities where code=%s"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        return cursor.fetchone()
    
def create_abiliti_owning(db:Database,username:str,ability_code:str)->None:
    data:tuple=(username,ability_code)
    template:str="""INSERT INTO own_ability(id_playera,id_ability) values ((SELECT id FROM player WHERE username=%s LIMIT 1),(SELECT id FROM abilities where code=%s LIMIT 1))"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()
