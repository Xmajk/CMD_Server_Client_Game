from Others.Connection import Connection
from Interfaces.CMD_level import CMD_level
from typing import Dict,List
from lib.ICommand import ICommand
from Enums.Next_message import Next_message
from Database.Actions.Set_status import set_building
from Interfaces.Profil.Profile import Profil_view
from Database.Actions.Authentication import username_exists
from Interfaces.Inventory_level import Inventory_level
from Gameobjects.NPC import NPC

class Building(CMD_level):
    
    def __init__(self,connect:Connection,prompt:str,commands:Dict[str,ICommand],name:str,
                 NPCs:List[str]) -> None:
        
        if not "ven" in commands.keys():commands["ven"]=Ven_command(self)
        if not "help" in commands.keys():commands["help"]=Full_help_command(self)
        if not "profil" in commands.keys():commands["profil"]=Profil_command(self)
        if not "inventar" in commands.keys():commands["inventar"]=Inventar_command(self)
        if not "vypis_NPCs" in commands.keys():commands["vypis_NPCs"]=Print_NPCs_command(self)
        if not "NPC" in commands.keys():commands["NPC"]=NPC_command(self)
        
        super().__init__(
            connect=connect,
            prompt=prompt+f'{name}>',
            commands=commands
        )
        self.name:str=name
        self.NPCs:Dict[str,NPC]=NPCs
        
    def loop(self) -> None:
        super().loop()
        
    def supplementary_help(self):
        self.connect.send("-profil --[jméno hráče (dobrovolné)]=>když napíšete příkaz bez argumentu, tak",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("zobrazíte svůj profil, jinak zobrazíte profil hráče",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-ven=>vyjdete z budovy",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-vypis_NPCs=>vypíšou se všechny NPC ve vaší lokalitě",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-NPC --[jméno NPC se kterým chcete interagovat]=>začne interagce se zadaným NPC",next_message=Next_message.PRIJMI,prompt=self.prompt)
        super().supplementary_help()
        
class Ven_command(ICommand):
    
    def __init__(self,building:Building) -> None:
        self.building:Building=building
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.building.connect.send("Příkaz \"ven\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.building.prompt)
            return True
        set_building(self.building.connect.databaze,self.building.connect.player.username)
        self.building.connect.save_player()
        return False
    
class Full_help_command(ICommand):
    
    def __init__(self,building:Building) -> None:
        self.building:Building=building
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.building.connect.send("Příkaz \"help\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.building.prompt)
            return True
        self.building.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.building.prompt)
        self.building.supplementary_help()
        self.building.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.building.prompt)
        return True
    
class Profil_command(ICommand):
    
    def __init__(self,building:Building) -> None:
        self.building:Building=building
        
    def execute(self,options:List[str]):
        if not len(options) in [0,1]:
            self.building.connect.send("Příkaz \"profil\" má jeden dobrovolný argument",next_message=Next_message.PRIJMI,prompt=self.building.prompt)
            return True
        if len(options)==1:
            if username_exists(self.building.connect.databaze,options[0]):
                Profil_view(self.building.connect,self.building.prompt,options[0]).loop()
            else:
                self.building.connect.send(f'Uživatel \"{options[0]}\" neexistuje',next_message=Next_message.PRIJMI,prompt=self.building.prompt)
            return True
        if len(options)==1:
            Profil_view(self.building.connect,self.building.prompt,options[0]).loop()
        else:
            Profil_view(self.building.connect,self.building.prompt).loop()
        return True
    
class Inventar_command(ICommand):
    
    def __init__(self,building:Building) -> None:
        self.building:Building=building
        
    def execute(self,options:List[str]):
        if not len(options) == 0:
            self.building.connect.send("Příkaz \"inventar\" nemá žadné argumenty",next_message=Next_message.PRIJMI,prompt=self.building.prompt)
            return True
        Inventory_level(self.building.connect,self.building.prompt).loop()
        return True
    
class Print_NPCs_command(ICommand):
    
    def __init__(self,building:Building) -> None:
        self.building:Building=building
        
    def execute(self,options:List[str]):
        if not len(options) == 0:
            self.building.connect.send("Příkaz \"vypis_NPCs\" nemá žadné argumenty",next_message=Next_message.PRIJMI,prompt=self.building.prompt)
            return True
        if len(self.building.NPCs)==0:
            self.building.connect.send(f'V budově \"{self.building.name}\" nejsou žádna NPC',next_message=Next_message.PRIJMI,prompt=self.building.prompt)
        self.building.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.building.prompt)
        for npc in self.building.NPCs.keys():
            self.building.connect.send(npc,next_message=Next_message.PRIJMI,prompt=self.building.prompt)
        self.building.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.building.prompt)
        return True
    
class NPC_command(ICommand):
    
    def __init__(self,building:Building) -> None:
        self.building:Building=building
        
    def execute(self,options:List[str]):
        if not len(options) == 1:
            self.building.connect.send("Příkaz \"NPC\" má jeden povinný argument",next_message=Next_message.PRIJMI,prompt=self.building.prompt)
            return True
        npc_name:str=options[0]
        if not npc_name in self.building.NPCs.keys():
            self.building.connect.send(f'NPC \"{npc_name}\" není ve vaší lokalitě',next_message=Next_message.PRIJMI,prompt=self.building.prompt)
            return True
        self.building.NPCs[npc_name].loop()
        return True