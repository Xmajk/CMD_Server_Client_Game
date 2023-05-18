from typing import Dict
from Others.Connection import Connection
from lib.ICommand import ICommand
from Interfaces.CMD_level import CMD_level

class Inventory_interface(CMD_level):
    
    def __init__(self, connect: Connection,base_prompt:str) -> None:
        super().__init__(connect,
                         prompt=f'{base_prompt}inventář>',
                         commands={
                             
                         })
        self.base_prompt:str=base_prompt
        
    def loop(self):
        return super().loop()
    
