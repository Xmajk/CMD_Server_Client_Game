from typing import Dict
from Interfaces.CMD_level import CMD_level
from lib.ICommand import ICommand
from Others.Connection import Connection
from Enums.Next_message import Next_message

class NPC_battle(CMD_level):
    
    
    def __init__(self, connect: Connection,base_prompt:str,left_able:bool=False) -> None:
        super().__init__(connect=connect,
                         prompt="", 
                         commands={
                             "vypis_inventar":Print_inventory(self)
                         })
    
    def loop(self):
        return super().loop()
    
    def supplementary_help(self):
        self.connect.send("vypis_inventar=>vypíše se použitelný inventář",Next_message=Next_message.PRIJMI,prompt=self.prompt)
        return super().supplementary_help()
    
class Print_inventory(ICommand):
    
    def __init__(self,npc_battle:NPC_battle) -> None:
        self.npc_battle:NPC_battle=npc_battle
        
    def execute(self) -> bool:
        raise NotImplementedError("NPC battle")