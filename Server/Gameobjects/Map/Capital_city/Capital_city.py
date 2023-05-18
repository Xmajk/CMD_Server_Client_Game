from Others.Connection import Connection
from Enums.Next_message import Next_message
from lib.ICommand import ICommand
from Gameobjects.Map.Place import Place
from typing import List
from Others.Crossing import to_route1
from Gameobjects.Building import Building
from Gameobjects.Map.Capital_city.Capital_city_tawern import Capital_city_tawern
from Database.Actions.Set_status import set_building
from Database.Actions.Quests import Capital_city_tawern as cptq

class Capital_city(Place):
    """
        Označení v databázi jako 1
    """ 
    name:str="Hlavní město"
    prompt:str="Hlavní_město>"
    
    def __init__(self,connect:Connection) -> None:
        super().__init__(
            name=self.name,
            prompt=self.prompt,
            connect=connect,
            NPCs=[],
            buildings={
            "hospoda":Capital_city_tawern(connect=connect)    
            },
            ways={"Route1": to_route1},
            commands={
                "help": Help_command(self),
                "budova":Budova_command(self)
            }
        )
    
    def loop(self):
        super().loop()
        
class Help_command(ICommand):
    
    def __init__(self,capital_city:Capital_city) -> None:
        self.capital_city:Capital_city=capital_city
        
    def execute(self,options:list):
        if not len(options)==0:
            self.capital_city.connect.send("Příkaz \"help\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.capital_city.prompt)
            return True
        self.capital_city.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.capital_city.prompt)
        self.capital_city.supplementary_help()
        self.capital_city.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.capital_city.prompt)
        return True
    
class Budova_command(ICommand):
    
    def __init__(self,capital_city:Capital_city) -> None:
        self.capital_city:Capital_city=capital_city   
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==1:
            self.capital_city.connect.send(f'Příkaz \"budova\" má jeden povinný argument',next_message=Next_message.PRIJMI,prompt=self.capital_city.prompt)
            return True
        if not options[0] in self.capital_city.buildings.keys():
            self.capital_city.connect.send(f'Budova \"{options[0]}\" neexistuje',next_message=Next_message.PRIJMI,prompt=self.capital_city.prompt)
            return True
        if options[0]=="hospoda" and not cptq(self.capital_city.connect.databaze,self.capital_city.connect.player.username):
            self.capital_city.connect.send(f'Hospoda je uzavřena, protože hospodského unesli banditi!',next_message=Next_message.PRIJMI,prompt=self.capital_city.prompt)
            return True
        set_building(self.capital_city.connect.databaze,self.capital_city.connect.player.username,self.capital_city.name,options[0])
        self.capital_city.buildings[options[0]].loop()
        return True
