from Database.Database import Database
from typing import List,Tuple

def all_using_to_inventory(db:Database,username:str)->None:
    data:Tuple[str]=(username,)
    template:str="""UPDATE own_item SET is_using=0 WHERE id_playera=(SELECT id FROM player WHERE username=%s LIMIT 1);"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()
        
def print_inventory(db:Database,username:str)->List[Tuple[str,str,int]]:
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
    data:Tuple[str]=(username,)
    template:str="""SELECT i.nazev,i.kod,o.is_using FROM
item i inner join 
(player p inner join own_item o on p.id=o.id_playera)
on i.id=o.id_itemu where o.is_using=0 and p.username=%s;"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:List[Tuple[str,str,int]]=cursor.fetchall()
    return db_output