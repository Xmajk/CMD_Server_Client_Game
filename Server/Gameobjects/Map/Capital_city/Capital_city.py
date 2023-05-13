from Others.Connection import Connection
from Enums.Next_message import Next_message
import time
from lib.ICommand import ICommand
from Others.Help_methods import edit_response
from Interfaces.Profil.Profile import Profil_view
from Database.Actions.Authentication import username_exists
from Gameobjects.Map.Place import Place
from Others.Crossing import to_route1

class Capital_city(Place):
    """
        Označení v databázi jako 1
    """    
    def __init__(self,connect:Connection) -> None:
        super().__init__(
            name="Hlavní město",
            prompt="Hlavní město>",
            connect=connect,
            NPCs=[],
            buildings=[],
            ways={"Route1": to_route1},
            commands={
                "help": Help_command(),
                "profil": Profil_command(),
                "vypis_budovy": None,
                "budova": None,
                "vypis_cesty": None,
                "cesta": Cesta_command(),
                "vypis_postavy": None,
                "postava": None
            }
        )
    
    def loop(self):
        print("loop capital city")
        super().loop()
        
class Neznamy_command(ICommand):
    
    def __init__(self) -> None:
        pass
    
    def execute(self,capital_city:Capital_city,options:list):
        capital_city.connect.send("Neznámý příkaz",next_message=Next_message.PRIJMI,prompt=capital_city.prompt)
        return True
        
class Help_command(ICommand):
    
    def __init__(self) -> None:
        pass
        
    def execute(self,capital_city:Capital_city,options:list):
        if not len(options)==0:
            capital_city.connect.send("Příkaz \"help\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=capital_city.prompt)
            return True
        capital_city.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=capital_city.prompt)
        capital_city.connect.send("-profil --[jméno hráče (dobrovolné)]=>když napíšete příkaz bez argumentu, tak",next_message=Next_message.PRIJMI,prompt=capital_city.prompt)
        capital_city.connect.send("zobrazíte svůj profil, jinak zobrazíte profil hráče",next_message=Next_message.PRIJMI,prompt=capital_city.prompt)
        capital_city.connect.send("-cesta --[název cesty]=>přejdete na cestu",next_message=Next_message.PRIJMI,prompt=capital_city.prompt)
        capital_city.connect.send("-help=>vypíšou se všechny příkazy, které můžete aktuálně použít",next_message=Next_message.PRIJMI,prompt=capital_city.prompt)
        capital_city.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=capital_city.prompt)
        return True
    
class Profil_command(ICommand):
    
    def __init__(self) -> None:
        pass
        
    def execute(self,capital_city:Place,options:list):
        if not len(options) in [0,1]:
            capital_city.connect.send("Příkaz \"profil\" má jeden dobrovolný argument",next_message=Next_message.PRIJMI,prompt=capital_city.prompt)
            return True
        if len(options)==1:
            if username_exists(capital_city.connect.databaze,options[0]):
                pass
            else:
                capital_city.connect.send(f'Uživatel \"{options[0]}\" neexistuje',next_message=Next_message.PRIJMI,prompt=capital_city.prompt)
            return True
        Profil_view(capital_city.connect,capital_city.prompt).loop()
        return True
    
class Cesta_command(ICommand):
    def execute(self,capital_city:Place,options:list):
        if not len(options) == 1:
            capital_city.connect.send("Příkaz \"cesta\" má jeden povinný argument",next_message=Next_message.PRIJMI,prompt=capital_city.prompt)
            return True
        if not options[0] in capital_city.ways.keys():
            capital_city.connect.send(f'Cesta \"{options[0]}\" neexistuje',next_message=Next_message.PRIJMI,prompt=capital_city.prompt)
            return True
        capital_city.ways[options[0]](capital_city.connect)