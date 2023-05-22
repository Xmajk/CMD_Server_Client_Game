from typing import Dict,List
from Interfaces.CMD_level import CMD_level
from lib.ICommand import ICommand
from Others.Connection import Connection
from Enums.Next_message import Next_message

class Inventory_level(CMD_level):
    
    def __init__(self, connect: Connection, prompt: str) -> None:
        super().__init__(
            connect=connect,
            prompt=f'{prompt}inventář>', 
            commands={
                "help":Full_help_command(self)
            })
        
    def loop(self):
        return super().loop()
    
    def supplementary_help(self):
        self.connect.send("",next_message=Next_message.PRIJMI,prompt=self.prompt)
        return super().supplementary_help()
    
class Full_help_command(ICommand):
    
    def __init__(self,inventory:Inventory_level) -> None:
        self.inventory:Inventory_level=inventory
    
    def execute(self,options:List[str]) -> bool:
        self.inventory.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.supplementary_help()
        self.inventory.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        return True