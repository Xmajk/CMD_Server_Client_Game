from typing import Union,Tuple

class Item:
    
    def __init__(self,db_data:Tuple[str,str,str,int,int,int,int,Union[str,None]]) -> None:
        self.nazev:str=db_data[0]
        self.code:str=db_data[1]
        self.type:str=db_data[2]
        self.add_hp:int=db_data[3]
        self.add_atk:int=db_data[4]
        self.add_mana:int=db_data[5]
        self.add_speed:int=db_data[6]
        self.ability:Union[str,None]=db_data[7]
        self.is_using:bool=db_data[8]
        