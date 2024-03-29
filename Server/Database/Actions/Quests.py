import mysql.connector
from Gameobjects.Player import Player
from Database.Database import Database

#Hlavní město
def capital_city_tawern(db:Database,username:str)->bool:
    """
    Metoda ověřuje, zda má hráč splněnou misi "Capital city tawer quest".

    Parametry
    ---------
    db : Database
        Instance třídy Database, která reprezentuje spojení s databází
    username : str
        Uživatelské jméno hráče, pro kterého se má ověřit splnění mise

    Vrací 
    -----
    bool
        True, pokud má hráč splněnou misi "Capital city tawer quest", jinak False
    """
    data:tuple=(username,)
    template:str="""SELECT q.nazev FROM
player p inner join
(quests q inner join missions_completed m on q.id=m.id_questu) on m.id_playera=p.id
WHERE p.username=%s and q.nazev='Capital city tawer quest';"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db_output:tuple=cursor.fetchone()
    return not db_output==None