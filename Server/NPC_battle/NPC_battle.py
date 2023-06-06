from typing import Dict,List
from Interfaces.CMD_level import CMD_level
from lib.ICommand import ICommand
from Others.Connection import Connection
from Enums.Next_message import Next_message
from NPC_battle.Battle_NPC import Battle_NPC

class NPC_battle(CMD_level):
    
    def __init__(self, connect: Connection,base_prompt:str,enemy:Battle_NPC,left_able:bool=False) -> None:
        super().__init__(connect=connect,
                         prompt=f'{base_prompt}>souboj[NPC]', 
                         commands={
                             "vypis_inventar":Print_inventory_command(self),
                             "help":Full_help_command(self),
                             "vypis_informace_o_nepriteli":None,
                             "zautocit":None,
                             "pouzit":None
                         })
        if left_able:
            self.commands["opustit"]=Left_command(self)
        self.leftable:bool=left_able
        self.enemy:Battle_NPC=enemy
    
    def loop(self):
        return super().loop()
    
    def supplementary_help(self):
        self.connect.send("-vypis_inventar=>vypíše se použitelný inventář",next_message=Next_message.PRIJMI,prompt=self.prompt)
        if self.leftable:
            self.connect.send("-opustit=>opustíte souboj",next_message=Next_message.PRIJMI,prompt=self.prompt)
        return super().supplementary_help()
    
class Left_command(ICommand):
    
    def __init__(self,npc_battle:NPC_battle) -> None:
        self.npc_battle:NPC_battle=npc_battle
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.npc_battle.connect.send("Příkaz \"opustit\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            return True  
        self.npc_battle.connect.send(f'Opustil jste souboj s {self.npc_battle.enemy.name}',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        return False
    
class Print_inventory_command(ICommand):
    """
    Třída reprezentující příkaz výpisu inventáře.
    
    Atributy
    --------
    npc_battle : NPC_battle
        Instance NPC_battle, ze které byl příkaz spuštěn
    """
    
    def __init__(self,npc_battle:NPC_battle) -> None:
        self.npc_battle:NPC_battle=npc_battle
        
    def execute(self,options:List[str]) -> bool:
        raise NotImplementedError("NPC battle")
    
class Full_help_command(ICommand):
    """
    Třída reprezentující příkaz help
    
    Atributy
    --------
    npc_battle : NPC_battle
        Instance NPC_battle, ze které byl příkaz spuštěn
    """
    
    def __init__(self,npc_battle:NPC_battle) -> None:
        self.npc_battle:NPC_battle=npc_battle
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.npc_battle.connect.send("Příkaz \"help\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            return True            
        self.npc_battle.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.supplementary_help()
        self.npc_battle.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        return True
