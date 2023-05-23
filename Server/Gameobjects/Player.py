from typing import List,Union,Tuple
from Gameobjects.Item import Item
from Database.Database import Database

class Player:
    
    def __init__(self,username) -> None:
        self.username:str=username
        self.current_hp:int=0
        self.trida:Union[str,None]=None
        self.base_hp:int=0
        self.base_atk:int=0
        self.base_speed:int=0
        self.base_mana:int=0
        self.add_hp:int=0
        self.add_atk:int=0
        self.add_speed:int=0
        self.add_mana:int=0
        self.items_hp:int=0
        self.items_atk:int=0
        self.items_speed:int=0
        self.items_mana:int=0
        self.coins:int=0
        self.inventory:List[Item]=[]
    
    def load(self,db:Database)->None:
        from Database.Actions.Load_player import load_base,get_inventory
        data:Tuple[int,int,int,int,int,int,int,int,int,str,int]=load_base(db,self.username)
        self.base_hp=data[0]
        self.base_atk=data[1]
        self.base_speed=data[2]
        self.base_mana=data[3]
        self.add_hp=data[4]
        self.add_atk=data[5]
        self.add_speed=data[6]
        self.add_mana=data[7]
        self.coins=data[8]
        self.trida=data[9]
        self.current_hp=data[10]
        
        self.inventory:List[Item]=[]
        
        for item in get_inventory(db,self.username):
            tmp:Item=Item(item)
            if tmp.is_using:
                self.items_atk+=tmp.add_atk
                self.items_hp+=tmp.add_hp
                self.items_mana+=tmp.add_mana
                self.items_speed+=tmp.add_speed
            self.inventory.append(tmp)
            
    def save(self,db:Database)->None:
        from Database.Actions.Load_player import save_stats
        from Database.Actions.Inventory_db import get_inventory_2,change_owning_put_on
        save_stats(db,self)
        database:List[Tuple[str,str,bool]]=[(nazev,kod,bool(is_using)) for nazev,kod,is_using in get_inventory_2(db,self.username)]
        my_inventory:List[Tuple[str,str,bool]]=[(element.nazev,element.code,element.is_using) for element in self.inventory]
        tmp_database = [t for t in database if t not in my_inventory]
        tmp_my_inventory = [t for t in my_inventory if t not in database]
        database:List[Tuple[str,str,bool]]=tmp_database
        my_inventory:List[Tuple[str,str,bool]]=tmp_my_inventory
        #kontrola změny
        if not len(database)==0 and not len(my_inventory)==0:
            common_tuples:List[Tuple[str,str,bool]] = [t for t in my_inventory if any(t[:2] == x[:2] for x in database)]
            for common_nazev,common_kod,common_is_using in common_tuples:
                for index,tup in enumerate(database,start=0):
                    db_nazev,db_kod,db_is_using=tup
                    if db_nazev==common_nazev and db_kod==common_kod:
                        database.pop(index)
                        break
                for index,tup in enumerate(my_inventory,start=0):
                    mi_nazev,mi_kod,mi_is_using=tup
                    if mi_nazev==common_nazev and mi_kod==common_kod:
                        my_inventory.pop(index)
                change_owning_put_on(db,self.username,common_kod,common_is_using)
        #kontrola existence
        if True:
            pass