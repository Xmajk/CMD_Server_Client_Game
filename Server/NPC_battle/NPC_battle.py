from typing import Dict,List,Tuple
from Interfaces.CMD_level import CMD_level
from lib.ICommand import ICommand
from Others.Connection import Connection
from Enums.Next_message import Next_message
from NPC_battle.Battle_NPC import Battle_NPC
from copy import deepcopy
from Gameobjects.Player import Player
from Gameobjects.Item import Item

class NPC_battle(CMD_level):
    
    def __init__(self, connect: Connection,base_prompt:str,enemy:Battle_NPC,left_able:bool=False) -> None:
        super().__init__(connect=connect,
                         prompt=f'{base_prompt}souboj[NPC]>', 
                         commands={
                             "vypis_inventar":Print_inventory_command(self),
                             "help":Full_help_command(self),
                             "vypis_informace_o_nepriteli":Print_enemy_informations_command(self),
                             "zautocit":None,
                             "pouzit":Use_command(self),
                             "vypis_ability":Print_abilities_command(self),
                             "vypis_informace":Print_informations_command(self)
                         })
        if left_able:
            self.commands["opustit"]=Left_command(self)
        self.leftable:bool=left_able
        self.enemy:Battle_NPC=enemy
        self.tmp_player:Player=deepcopy(self.connect.player)
        self.effects:List[Tuple[Item,int]]=[]
    
    def loop(self):
        return super().loop()
    
    def supplementary_help(self):
        self.connect.send("-vypis_inventar=>vypíše se použitelný inventář",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-vypis_informace_o_nepriteli=>vypíšou se itemy, které mohu použít v souboji",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-zautocit=>zautočíte na nepřítele",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-pouzit --[kod, itemu, který chcete použít]=>použijete item",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-vypis_ability=>vypíšou se ability",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-pouzit_abilitu --[]=>použijete abilitu",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-vypis_informace=>vypíšou se informace o vaší postavě",next_message=Next_message.PRIJMI,prompt=self.prompt)
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
        self.npc_battle.connect.send(f'Hp:{self.npc_battle.tmp_player.current_hp}/{self.npc_battle.enemy.hp}',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.connect.send(f'Atk:{self.npc_battle.enemy.atk}',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.connect.send(f'Speed:{self.npc_battle.enemy.speed}',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        return True
    
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

class Use_command(ICommand):
    """
    Třída reprezentující příkaz použítí itemu
    
    Atributy
    --------
    npc_battle : NPC_battle
        Instance NPC_battle, ze které byl příkaz spuštěn
    """
    
    def __init__(self,npc_battle:NPC_battle) -> None:
        self.npc_battle:NPC_battle=npc_battle
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==1:
            self.npc_battle.connect.send("Příkaz \"pouzij\" má jeden povinný argument kód itemu",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            return True
        selected_code:str=options[0]
        if not len(selected_code)==4:
            self.npc_battle.connect.send(f'Kód \"{selected_code}\" nesplňuje pravidla kódů itemů',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            return True
        if False in [element in [str(i) for i in range(10)] for element in selected_code]:
            self.npc_battle.connect.send(f'Kód \"{selected_code}\" nesplňuje pravidla kódů itemů',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            return True
        if not selected_code in [item.code for item in self.npc_battle.tmp_player.inventory if item.type in ["useable","combat_useable"]]:
            self.npc_battle.connect.send(f'Nevlastníte předmět s kódem \"{selected_code}\"',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            return True
        if not selected_code in [item.code for item in self.npc_battle.tmp_player.inventory if item.type in ["useable","combat_useable"]]:
            self.npc_battle.connect.send(f'Nemáte v inventáři předmět s kódem \"{selected_code}\"',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            return True
        if not selected_code in [item.code for item in self.npc_battle.tmp_player.inventory if item.type in ["useable","combat_useable"]]:
            self.npc_battle.connect.send(f'Item s kóddem \"{selected_code}\" nelze použít',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            return True
        for item in self.npc_battle.tmp_player.inventory:
            if item.code==selected_code:
                selected_item:Item=item
                break
        if selected_item.code in ["0009","0013"]: #léčivý lektvar
            if self.npc_battle.tmp_player.current_hp==self.npc_battle.tmp_player.get_full_hp():
                self.npc_battle.connect.send(f'Máte plný počet životů a nepotřebujete použít \"{selected_item.nazev}\"',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
                return True
            if self.npc_battle.tmp_player.current_hp+selected_item.add_hp>self.npc_battle.tmp_player.get_full_hp():
                self.npc_battle.connect.send(f'Vyléčil jste si {self.npc_battle.tmp_player.get_full_hp()-self.npc_battle.tmp_player.current_hp} životů',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            else:
                self.npc_battle.connect.send(f'Vyléčil jste si {selected_item.add_hp} životů',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            self.npc_battle.tmp_player.add_to_current_health(selected_item.add_hp)
        elif selected_item.code=="0010": # mana lektvar
            if self.npc_battle.tmp_player.current_mana==self.npc_battle.tmp_player.get_full_mana():
                self.npc_battle.connect.send(f'Máte plný počet many a nepotřebujete použít \"{selected_item.nazev}\"',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
                return True
            if self.npc_battle.tmp_player.current_mana+selected_item.add_mana>self.npc_battle.tmp_player.get_full_mana():
                self.npc_battle.connect.send(f'Přidal jste si {self.npc_battle.tmp_player.get_full_mana()-self.npc_battle.tmp_player.current_mana} many',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            else:
                self.npc_battle.connect.send(f'Přidal jste si {selected_item.add_mana} many',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            self.npc_battle.tmp_player.add_to_current_mana(selected_item.add_mana)
        elif selected_item.code=="0011":
            self.npc_battle.tmp_player.add_to_add_speed(selected_item.add_speed)
            self.npc_battle.effects.append((selected_item,3))
            self.npc_battle.connect.send(f'Použil se item \"{selected_item.nazev}\" a efekt potrvá 3 kola',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            self.npc_battle.connect.send(f'Item \"{selected_item.nazev}\" vám přidal {selected_item.add_speed} k rychlosti',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        else:
            raise ValueError(f'{selected_code} není zaznamenán jako použítelný item')
        self.npc_battle.tmp_player.inventory.remove(selected_item)
        return True
    
class Print_informations_command(ICommand):
    """
    Třída reprezentující příkaz pro vypsání informací o uživatelu
    
    Atributy
    --------
    npc_battle : NPC_battle
        Instance NPC_battle, ze které byl příkaz spuštěn
    """
    
    def __init__(self,npc_battle:NPC_battle) -> None:
        self.npc_battle:NPC_battle=npc_battle
        
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.npc_battle.connect.send("Příkaz \"vypis_infomace\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            return True
        self.npc_battle.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.connect.send(f'Hp:{self.npc_battle.tmp_player.current_hp}/{self.npc_battle.tmp_player.get_full_hp()}',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.connect.send(f'Atk:{self.npc_battle.tmp_player.get_full_atk()}',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.connect.send(f'Mana:{self.npc_battle.tmp_player.current_mana}/{self.npc_battle.tmp_player.get_full_mana()}',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.connect.send(f'Speed:{self.npc_battle.tmp_player.get_full_speed()}',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        return True
    
class Print_abilities_command(ICommand):
    """

    
    Atributy
    --------
    npc_battle : NPC_battle
        Instance NPC_battle, ze které byl příkaz spuštěn
    """
    
    def __init__(self,npc_battle:NPC_battle) -> None:
        self.npc_battle:NPC_battle=npc_battle
        
    def execute(self,options:List[str]) -> bool:
        if len(self.npc_battle.tmp_player.abilities)==0:
            self.npc_battle.connect.send(f'Nemáte žádné ability',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
            return True
        self.npc_battle.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        for ability in self.npc_battle.tmp_player.abilities:
            self.npc_battle.connect.send(f'-{ability.name}[{ability.code}]',next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        self.npc_battle.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.npc_battle.prompt)
        return True
        
    
class Attack_command(ICommand):
    """

    
    Atributy
    --------
    npc_battle : NPC_battle
        Instance NPC_battle, ze které byl příkaz spuštěn
    """
    
    def __init__(self,npc_battle:NPC_battle) -> None:
        self.npc_battle:NPC_battle=npc_battle
        
    def execute(self,options:List[str]) -> bool:
        return True