import mysql.connector
from Database.Database import Database
from typing import Tuple,Union,List

def load_base(db:Database,username:str)->Tuple[int,int,int,int,int,int,int,int,int,str]:
    data:tuple=(username,)
    template:str="""select c.hp,c.atk,c.speed,c.mana,p.add_hp,p.add_atk,p.add_speed,p.add_mana,p.coins,c.nazev from 
player p inner join class c on c.id=p.id_class where p.username=%s;"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
    return db_output

def get_inventory(db:Database,username:str)->List[Tuple[str,str,str,int,int,int,int,Union[str,None]]]:
    data:Tuple[str]=(username,)
    template:str="""SELECT i.nazev,i.kod, it.nazev, i.player_hp,i.player_damage,i.player_mana,i.player_speed,i.ability_info,o.is_using FROM
item_type it inner join
(item i inner join
(player p inner join own_item o on p.id=o.id_playera)
on i.id=o.id_itemu) on it.id=i.id_typu where p.username=%s;
"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchall()
    return db_output
