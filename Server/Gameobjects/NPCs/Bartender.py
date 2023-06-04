from typing import Dict,List,Tuple
from Others.Connection import Connection
from Interfaces.CMD_level import CMD_level
from lib.ICommand import ICommand
from Gameobjects.NPC import NPC
from Enums.Next_message import Next_message
from Gameobjects.Item import Item
from Database.Actions.Inventory_db import get_item

class Bartender(NPC):
    
    def __init__(self, connect: Connection, base_prompt: str) -> None:
        self.bar_beer_cost:int=20
        self.beer_cost:int=25
        super().__init__(connect, 
                         name="hospodský", 
                         commads={
                            "pivo":Bar_beer_command(self),
                            "koupit_pivo":Buy_beer(self),
                            "help":Full_help_command(self),
                            "zpet":Back_command(self)
                        }, 
                        base_prompt=base_prompt)
        
    def supplementary_help(self):
        self.connect.send("pivo=>koupíte si 20 coinů za  na baru pivo, vypijete ho a vyléčíte si 50 životů",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("koupit_pivo=>koupíte si za 25 coinů předmět pivo",next_message=Next_message.PRIJMI,prompt=self.prompt)
        return super().supplementary_help()
    
class Full_help_command(ICommand):
    
    def __init__(self,bartender:Bartender) -> None:
        self.bartender:Bartender=bartender
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.bartender.connect.send("Příkaz \"help\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.bartender.prompt)
            return True
        self.bartender.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.bartender.prompt)
        self.bartender.connect.send(f'pivo=>koupíte si pivo za {self.bartender.bar_beer_cost} coinů a vypijete ho, což vám vyléčí 50 životů',next_message=Next_message.PRIJMI,prompt=self.bartender.prompt)
        self.bartender.connect.send(f'koupit_pivo=>koupíte si item piva za {self.bartender.beer_cost}',next_message=Next_message.PRIJMI,prompt=self.bartender.prompt)
        self.bartender.connect.send(f'zpet=>vystoupíte z kounverzace s NPC',next_message=Next_message.PRIJMI,prompt=self.bartender.prompt)
        self.bartender.supplementary_help()
        self.bartender.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.bartender.prompt)
        return True

class Bar_beer_command(ICommand):
    def __init__(self,bartender:Bartender) -> None:
        self.bartender:Bartender=bartender
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.bartender.connect.send("Příkaz \"pivo\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.bartender.prompt)
            return True
        if self.bartender.bar_beer_cost>self.bartender.connect.player.coins:
            self.bartender.connect.send(f'Nemáte dostatek coinů, pivo stojí {self.bartender.bar_beer_cost} coinů',next_message=Next_message.PRIJMI,prompt=self.bartender.prompt)
            return True
        item:Item=Item(get_item(self.bartender.connect.databaze,'0013')+(0,))
        if self.bartender.connect.player.current_hp==self.bartender.connect.player.get_full_hp():
            self.bartender.connect.send(f'Máte plný počet hp',next_message=Next_message.PRIJMI,prompt=self.bartender.prompt)
            return True
        self.bartender.connect.player.coins-=self.bartender.bar_beer_cost
        if self.bartender.connect.player.current_hp+item.add_hp>self.bartender.connect.player.get_full_hp():
            healt_hp:int=self.bartender.connect.player.get_full_hp()-self.bartender.connect.player.current_hp
        else:
            healt_hp:int=item.add_hp
        self.bartender.connect.send(f'Po vypití piva jste si vyléčili {healt_hp} hp',next_message=Next_message.PRIJMI,prompt=self.bartender.prompt)
        self.bartender.connect.player.current_hp+=healt_hp
        return True
    
class Buy_beer(ICommand):
    def __init__(self,bartender:Bartender) -> None:
        self.bartender:Bartender=bartender
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.bartender.connect.send("Příkaz \"koupit_pivo\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.bartender.prompt)
            return True
        if self.bartender.beer_cost>self.bartender.connect.player.coins:
            self.bartender.connect.send(f'Nemáte dostatek coinů, pivo stojí {self.bartender.beer_cost} coinů',next_message=Next_message.PRIJMI,prompt=self.bartender.prompt)
            return True
        item:Item=Item(get_item(self.bartender.connect.databaze,'0013')+(0,))
        self.bartender.connect.player.coins-=self.bartender.beer_cost
        self.bartender.connect.player.inventory.append(item)
        self.bartender.connect.send(f'Zakoupil jste si pivo',next_message=Next_message.PRIJMI,prompt=self.bartender.prompt)
        return True
    
class Back_command(ICommand):
    def __init__(self,bartender:Bartender) -> None:
        self.bartender:Bartender=bartender
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.bartender.connect.send("Příkaz \"zpet\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.bartender.prompt)
            return True
        return False