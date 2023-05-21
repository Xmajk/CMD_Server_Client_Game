import mysql.connector
from Database.Database import Database
from typing import Tuple,Union

def load_base(db:Database,username:str)->Tuple[Union[str,int]]:
    data:tuple=(username,)
    template:str="""select c.hp,c.atk,c.speed,c.mana,p.add_hp,p.add_atk,p.add_speed,p.add_mana,p.coins,c.nazev from 
player p inner join class c on c.id=p.id_class where p.username=%s;"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
    return db_output