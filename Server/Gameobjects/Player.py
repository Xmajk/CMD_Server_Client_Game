from typing import List,Union,Tuple
from Gameobjects.Item import Item
from Database.Database import Database

class Player:
    
    def __init__(self,username) -> None:
        self.username:str=username
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
        from Database.Actions.Load_player import load_base
        data:Tuple[int,int,int,int,int,int,int,int,int,str]=load_base(db,self.username)
        print(data)
        