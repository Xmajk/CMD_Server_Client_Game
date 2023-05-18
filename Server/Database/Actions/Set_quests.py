import mysql.connector
from Database.Database import Database

def set_capital_city_tawern(db:Database,username:str):
    data:tuple=(username,)
    template:str="""INSERT INTO missions_completed(id_playera,id_questu) values 
((SELECT id FROM player WHERE username=%s LIMIT 1),(SELECT id FROM quests WHERE kod=1 LIMIT 1));"""
    with db.mydb.cursor() as cursor:
        cursor.execute(template,data)
        db.mydb.commit()