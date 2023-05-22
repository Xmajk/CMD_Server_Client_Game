from typing import Dict,List,Tuple
from Interfaces.CMD_level import CMD_level
from lib.ICommand import ICommand
from Others.Connection import Connection
from Enums.Next_message import Next_message
from Database.Actions.Inventory_db import all_using_to_inventory,print_inventory
from Gameobjects.Item import Item

class Inventory_level(CMD_level):
    
    def __init__(self, connect: Connection, base_prompt: str) -> None:
        super().__init__(
            connect=connect,
            prompt=f'{base_prompt}inventář>', 
            commands={
                "help":Full_help_command(self),
                "svleknout":Svleknout_command(self),
                "vypis_inventar":Print_inventory_command(self),
                "vypis_postavu":Print_character(self),
                "nasadit":Put_on_command(self)
            })
        self.base_prompt:str=base_prompt
        
    def loop(self):
        return super().loop()
    
    def supplementary_help(self):
        self.connect.send("-vypis_inventar=>vypíše všechny itemy, které uživatel má v inventáři",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-svléknout=>postava svlekne všechno vynavení, které má na sobě",next_message=Next_message.PRIJMI,prompt=self.prompt)
        return super().supplementary_help()
    
class Full_help_command(ICommand):
    
    def __init__(self,inventory:Inventory_level) -> None:
        self.inventory:Inventory_level=inventory
    
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.inventory.connect.send("Příkaz \"help\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        self.inventory.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.supplementary_help()
        self.inventory.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        return True

class Svleknout_command(ICommand):
    
    def __init__(self,inventory:Inventory_level) -> None:
        self.inventory:Inventory_level=inventory
    
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.inventory.connect.send("Příkaz \"svleknout\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        all_using_to_inventory(self.inventory.connect.databaze,self.inventory.connect.player.username)
        self.inventory.connect.send("Všechny předměty byly svléknuty a dány do inventáře.",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.load_player()
        return True
        
class Print_inventory_command(ICommand):

    def __init__(self,inventory:Inventory_level) -> None:
        self.inventory:Inventory_level=inventory
    
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.inventory.connect.send("Příkaz \"vypis_inventar\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        inventory:List[Tuple[str,str,int]]=print_inventory(self.inventory.connect.databaze,self.inventory.connect.player.username)
        if len(inventory)==0:
            self.inventory.connect.send("Máte prázdný inventář",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        self.inventory.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        for nazev,kod,count in inventory:
            self.inventory.connect.send(f'{count}x{nazev}[{kod}]',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        return True

class Print_character(ICommand):
    def __init__(self,inventory:Inventory_level) -> None:
        self.inventory:Inventory_level=inventory
    
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.inventory.connect.send("Příkaz \"vypis_postavu\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        self.inventory.connect.load_player()
        character:Dict[str,str] = {item.type:f'{item.nazev}[{item.code}]' for item in [element for element in self.inventory.connect.player.inventory if element.is_using]}
        self.inventory.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.send(f'helma :{character.get("přilba","-")}',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.send(f'zbroj :{character.get("zbroj","-")}',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.send(f'boty  :{character.get("boty","-")}',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.send(f'zbraň :{character.get("zbraň","-")}',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.send(f'peníze:{self.inventory.connect.player.coins}',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        return True
        
class Put_on_command(ICommand):
    def __init__(self,inventory:Inventory_level) -> None:
        self.inventory:Inventory_level=inventory
    
    def execute(self,options:List[str]) -> bool:
        if not len(options)==1:
            self.inventory.connect.send("Příkaz \"nasadit\" má 1 argument",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        #nasazování
        self.inventory.connect.save_player()
        return True
        