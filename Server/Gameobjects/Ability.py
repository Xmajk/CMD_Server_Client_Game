from typing import List,Tuple

class Ability:
    
    def __init__(self) -> None:
        self.name:str=""
        self.hp:int=0
        self.atk:int=0
        self.speed:int=0
        self.damage:int=0
        self.effect:bool=False
        self.round_of_effect:int=0
        self.mana_cost:int=0
        self.code:str=""
        
    def create_by_tuple(self,value:Tuple[str,int,int,int,int,bool,int,int,str])->None:
        self.name,self.hp,self.atk,self.speed,self.damage,self.effect,self.round_of_effect,self.mana_cost,self.code=value
        return self
        
    
    