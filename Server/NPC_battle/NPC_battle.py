from typing import Dict,List
from Interfaces.CMD_level import CMD_level
from lib.ICommand import ICommand
from Others.Connection import Connection
from Enums.Next_message import Next_message
from NPC_battle.Battle_NPC import Battle_NPC
from copy import deepcopy
from Gameobjects.Player import Player

class NPC_battle(CMD_level):
    
    def __init__(self, connect: Connection,base_prompt:str,enemy:Battle_NPC,left_able:bool=False) -> None:
        super().__init__(connect=connect,
                         prompt=f'{base_prompt}souboj[NPC]>', 
                         commands={
                             "vypis_inventar":Print_inventory_command(self),
                             "help":Full_help_command(self),
                             "vypis_informace_o_nepriteli":Print_enemy_informations_command(self),
                             "zautocit":None,
                             "pouzit":None,
                             "vypis_ability":None,
                             "pouzit_abilitu":None
                         })
        if left_able:
            self.commands["opustit"]=Left_command(self)
        self.leftable:bool=left_able
        self.enemy:Battle_NPC=enemy
        self.tmp_player:Player=deepcopy(self.connect.player)
    
    def loop(self):
        return super().loop()
    
    def supplementary_help(self):
        self.connect.send("-vypis_inventar=>vypíše se použitelný inventář",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-vypis_informace_o_nepriteli=>vypíšou se itemy, které mohu použít v souboji",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-zautocit=>zautočíte na nepřítele",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-pouzit --[kod, itemu, který chcete použít]=>použijete item",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-vypis_ability=>vypíšou se ability",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-pouzit_abilitu --[]=>použijete abilitu",next_message=Next_message.PRIJMI,prompt=self.prompt)
        if self.leftable:
            self.connect.send("-opustit=>opustíte souboj",next_message=Next_message.PRIJMI,prompt=self.prompt)
        return super().supplementary_help()
    
class Left_command(ICommand):
    """
    Třída reprezentující příkaz opuštění souboje.
    
    Atributy
    --------
    npc_battle : NPC_battle
        Instance NPC_battle, ze které byl příkaz spuštěn
    """
    
    def __init__(self,npc_battle:NPC_battle) -> None:
        self.npc_battle:NPC_battle=npc_battle
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.npc_battle.connect.send("Příkaz \"opustit\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            return True  
        self.npc_battle.connect.send(f'Opustil jste souboj s {self.npc_battle.enemy.name}',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        return False
    
class Print_enemy_informations_command(ICommand):
    """
    Třída reprezentující příkaz vypsání informací o nepříteli.
    
    Atributy
    --------
    npc_battle : NPC_battle
        Instance NPC_battle, ze které byl příkaz spuštěn
    """
    def __init__(self,npc_battle:NPC_battle) -> None:
        self.npc_battle:NPC_battle=npc_battle
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.npc_battle.connect.send("Příkaz \"vypis_informace_o_nepriteli\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            return True  
        self.npc_battle.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.connect.send(f'Jméno:{self.npc_battle.enemy.name}',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.connect.send(f'Hp:{self.npc_battle.enemy.hp}',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.connect.send(f'Atk:{self.npc_battle.enemy.atk}',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.connect.send(f'Speed:{self.npc_battle.enemy.speed}',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
    
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
        if not len(options)==0:
            self.npc_battle.connect.send("Příkaz \"vypis_inventar\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            return True  
        group_items = {}
        for item in [x for x in self.npc_battle.tmp_player.inventory if x.type in ["useable","combat_useable"]]:
            if (item.nazev,item.code) in group_items:
                group_items[(item.nazev,item.code)] += 1
            else:
                group_items[(item.nazev,item.code)] = 1
        self.npc_battle.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        for key, count in group_items.items():
            self.npc_battle.connect.send(f'{count:3}x{key[0]}[{key[1]}]',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        return True
    
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
