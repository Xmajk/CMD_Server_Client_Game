from typing import List,Tuple
from Database.Database import Database

def player_abilities(db:Database,username:str)->List[Tuple[str,int,int,int,int,bool,int,int,str]]:
    data:tuple=(username,)
    template:str="""SELECT a.nazev,a.hp,a.atk,a.speed,a.damage,a.effect,a.rounds_of_effect,a.mana_cost,a.code FROM
player p INNER JOIN(
abilities a INNER JOIN own_ability oa ON a.id=oa.id_ability)
ON p.id=oa.id_playera"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        return cursor.fetchall()
