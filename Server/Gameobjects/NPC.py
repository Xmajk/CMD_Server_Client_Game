from typing import Dict
from Others.Connection import Connection
from Interfaces.CMD_level import CMD_level
from lib.ICommand import ICommand

class NPC(CMD_level):
    
    def __init__(self, connect: Connection,name:str,commads:Dict[str,ICommand],base_prompt:str) -> None:
        super().__init__(connect,
                         prompt=f'{base_prompt}{name}[NPC]>', 
                         commands=commads)
        self.name=name