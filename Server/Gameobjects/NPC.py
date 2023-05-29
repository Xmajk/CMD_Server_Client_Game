from typing import Dict
from Others.Connection import Connection
from Interfaces.CMD_level import CMD_level
from lib.ICommand import ICommand

class NPC(CMD_level):
    """
    Třída představující NPC (Non-Player Character).

    Atributy
    --------
    connect : Connection
        Připojení k databázi.
    name : str
        Jméno NPC.
    commands : Dict[str, ICommand]
        Slovník příkazů NPC.
    base_prompt : str
        Základní prompt NPC.
    """
    
    def __init__(self, connect: Connection,name:str,commads:Dict[str,ICommand],base_prompt:str) -> None:
        super().__init__(connect,
                         prompt=f'{base_prompt}{name}[NPC]>', 
                         commands=commads)
        self.name=name