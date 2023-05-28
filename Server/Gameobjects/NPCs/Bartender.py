from typing import Dict,List
from Others.Connection import Connection
from Interfaces.CMD_level import CMD_level
from lib.ICommand import ICommand
from Gameobjects.NPC import NPC
from Enums.Next_message import Next_message
from Gameobjects.Item import Item

class Bartender(NPC):
    
    def __init__(self, connect: Connection, base_prompt: str) -> None:
        self.bar_beer_cost:int=20
        self.beer_cost:int=25
        super().__init__(connect, 
                         name="hospodský", 
                         commads={
                            "pivo":Bar_beer_command(self),
                            "koupit_pivo":None,
                            "help":Full_help_command(self)
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
            self.bartender.connect.send(f'Nemáte dostatek coinů, pivo stojí {self.bartender.bar_beer_cost}',next_message=Next_message.PRIJMI,prompt=self.bartender.prompt)
            return True
        print(self.bartender.connect.player.coins)
        return True