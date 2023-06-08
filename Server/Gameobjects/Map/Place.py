from Others.Connection import Connection
from typing import List,Dict,Callable
from lib.ICommand import ICommand
from Gameobjects.NPC import NPC
from Enums.Next_message import Next_message
from Others.Help_methods import edit_response
from Interfaces.CMD_level import CMD_level
from Database.Actions.Authentication import username_exists
from Interfaces.Profil.Profile import Profil_view
from Gameobjects.Building import Building
from Database.Actions.Set_status import set_location
from Database.Actions.Set_status import set_building
from Interfaces.Inventory_level import Inventory_level

class Place(CMD_level):
    """
    Třída, která reprezentuje nějakou polohu/lokaci
    
    Atributy
    --------
    connect : Connection
        Instance třídy Connection
    prompt : str
        Prompt na daném CMD levelu
    commands : Dict[str,ICommand]
        Slovník příkazů v dané lokalitě
    name : str
        Název loakce
    NPCs : List[NPC]
        List včech NPC v dané lokaci
    buildings : Dict[str,Building]
        Slovník všech budov v lokaci
    ways : Dict[str,Callable]
        Slovník metod, pro přechod do jiné lokace
    """
    
    def __init__(self,name:str,prompt:str,connect:Connection,
                 NPCs:List[NPC],buildings:Dict[str,Building],ways:Dict[str,Callable],
                 commands:Dict[str,ICommand]) -> None:
        
        commands["profil"]=Profil_command(self)
        if not "cesta" in commands.keys():commands["cesta"]=Cesta_command(self)
        if not "budova" in commands.keys():commands["budova"]=Budova_command(self)
        if not "NPC" in commands.keys():commands["NPC"]=NPC_command(self)
        if not "help" in commands.keys():commands["help"]=Full_help_command(self)
        if not "vypis_budovy" in commands.keys():commands["vypis_budovy"]=Vypis_budovy_command(self)
        if not "vypis_NPCs" in commands.keys():commands["vypis_NPCs"]=None
        if not "vypis_cesty" in commands.keys():commands["vypis_cesty"]=Vypis_cesty_command(self)
        if not "inventar" in commands.keys():commands["inventar"]=Inventar_command(self)
        
        super().__init__(connect,prompt,commands)
        self.name:str=name
        self.NPCs:List[NPC]=NPCs
        self.buildings:Dict[str,Building]=buildings
        self.ways:Dict[str,Callable]=ways
        
    def loop(self):
        super().loop()
        
    def supplementary_help(self):
        self.connect.send("-vypis_budovy=>vypíšou se budovy, které jsou v dané lokaci",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-budova --[název budovy]",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-vypis_NPCs=>vypíšou se NPC v dané lokaci",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-NPC --[název NPC]",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-profil --[jméno hráče (dobrovolné)]=>když napíšete příkaz bez argumentu, tak",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("zobrazíte svůj profil, jinak zobrazíte profil hráče",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-vypis_cesty=>vypíšou se cesty v dané lokaci",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-cesta --[název cesty]=>přejdete na cestu",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-inventar=>přejdete do svého inventáře",next_message=Next_message.PRIJMI,prompt=self.prompt)
        super().supplementary_help()
        
        
class Profil_command(ICommand):
    """
    Příkaz díky kterému se přejde na profil
    
    Atributy
    --------
    place : Place
        Instance třídy Place, ze které se příkaz volá
    """
    
    def __init__(self,place:Place) -> None:
        self.place:Place=place
        
    def execute(self,options:List[str]):
        if not len(options) in [0,1]:
            self.place.connect.send("Příkaz \"profil\" má jeden dobrovolný argument",next_message=Next_message.PRIJMI,prompt=self.place.prompt)
            return True
        if len(options)==1:
            if username_exists(self.place.connect.databaze,options[0]):
                Profil_view(self.place.connect,self.place.prompt,options[0]).loop()
            else:
                self.place.connect.send(f'Uživatel \"{options[0]}\" neexistuje',next_message=Next_message.PRIJMI,prompt=self.place.prompt)
            return True
        if len(options)==1:
            Profil_view(self.place.connect,self.place.prompt,options[0]).loop()
        else:
            Profil_view(self.place.connect,self.place.prompt).loop()
        return True
    
class Cesta_command(ICommand):
    """
    Příkaz pro přesun do jiné lokace
    
    Atributy
    --------
    place : Place
        Instance třídy Place, ze které se příkaz volá
    """
    
    def __init__(self,place:Place) -> None:
        self.place:Place=place    
    
    def execute(self,options:List[str]) -> bool:
        if not len(options) == 1:
            self.place.connect.send("Příkaz \"cesta\" má jeden povinný argument",next_message=Next_message.PRIJMI,prompt=self.place.prompt)
            return True
        if not options[0] in self.place.ways.keys():
            self.place.connect.send(f'Cesta \"{options[0]}\" neexistuje',next_message=Next_message.PRIJMI,prompt=self.place.prompt)
            return True
        set_location(self.place.connect.databaze,self.place.connect.player.username,options[0])
        self.place.connect.save_player()
        self.place.ways[options[0]](self.place.connect)
        return True
        
class Budova_command(ICommand):
    """
    Příkaz pro vstup do budovy
    
    Atributy
    --------
    place : Place
        Instance třídy Place, ze které se příkaz volá
    """
    
    def __init__(self,place:Place) -> None:
        self.place:Place=place    
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==1:
            self.place.connect.send(f'Příkaz \"budova\" má jeden povinný argument',next_message=Next_message.PRIJMI,prompt=self.place.prompt)
            return True
        if not options[0] in self.place.buildings.keys():
            self.place.connect.send(f'Budova \"{options[0]}\" neexistuje',next_message=Next_message.PRIJMI,prompt=self.place.prompt)
            return True
        set_building(self.place.connect.databaze,self.place.connect.player.username,lokace=self.place.name,building=options[0])
        self.place.buildings[options[0]].loop()
        return True
    
class NPC_command(ICommand):
    """
    Příkaz pro interakci s NPC
    
    Atributy
    --------
    place : Place
        Instance třídy Place, ze které se příkaz volá
    """
    
    def __init__(self,place:Place) -> None:
        self.place:Place=place    
        
    def execute(self,options:List[str]) -> bool:
        if not len(options) == 1:
            self.place.connect.send("Příkaz \"NPC\" má jeden povinný argument",next_message=Next_message.PRIJMI,prompt=self.place.prompt)
            return True
        npc_name:str=options[0]
        if not npc_name in self.place.NPCs.keys():
            self.place.connect.send(f'NPC \"{npc_name}\" není ve vaší lokalitě',next_message=Next_message.PRIJMI,prompt=self.place.prompt)
            return True
        self.place.NPCs[npc_name].loop()
        return True
    
class Full_help_command(ICommand):
    
    def __init__(self,place:Place) -> None:
        self.place:Place=place    
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.place.connect.send("Příkaz \"help\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.place.prompt)
            return True
        self.place.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.place.prompt)
        self.place.supplementary_help()
        self.place.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.place.prompt)
        return True
    
class Vypis_budovy_command(ICommand):
    """
    Příkaz pro vypsání všech dostupných budov
    
    Atributy
    --------
    place : Place
        Instance třídy Place, ze které se příkaz volá
    """
    
    def __init__(self,place:Place) -> None:
        self.place:Place=place    
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.place.connect.send("Příkaz \"vypis_budovy\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.place.prompt)
            return True
        if len(self.place.buildings)==0:
            self.place.connect.send(f'Lokace \"{self.place.name}\" nemá žádné budovy',next_message=Next_message.PRIJMI,prompt=self.place.prompt)
            return True
        self.place.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.place.prompt)
        for element in self.place.buildings.keys():
            self.place.connect.send(element,next_message=Next_message.PRIJMI,prompt=self.place.prompt)
        self.place.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.place.prompt)
        return True
    
class Vypis_cesty_command(ICommand):
    """
    Příkaz pro vypsání všech dostupných cest do jiných lokalit
    
    Atributy
    --------
    place : Place
        Instance třídy Place, ze které se příkaz volá
    """
    
    def __init__(self,place:Place) -> None:
        self.place:Place=place    
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.place.connect.send("Příkaz \"vypis_cesty\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.place.prompt)
            return True
        if len(self.place.ways)==0:
            self.place.connect.send(f'Lokace \"{self.place.name}\" nemá žádné cesty',next_message=Next_message.PRIJMI,prompt=self.place.prompt)
            return True
        self.place.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.place.prompt)
        for element in self.place.ways.keys():
            self.place.connect.send(element,next_message=Next_message.PRIJMI,prompt=self.place.prompt)
        self.place.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.place.prompt)
        return True
    
class Inventar_command(ICommand):
    """
    Příkaz pro vstup do inventáře uživatele
    
    Atributy
    --------
    place : Place
        Instance třídy Place, ze které se příkaz volá
    """
    
    def __init__(self,place:Place) -> None:
        self.place:Place=place    
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.place.connect.send("Příkaz \"inventar\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.place.prompt)
            return True
        Inventory_level(connect=self.place.connect,base_prompt=self.place.prompt).loop()
        return True