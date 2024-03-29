from typing import Dict,List,Tuple,Union
from Interfaces.CMD_level import CMD_level
from lib.ICommand import ICommand
from Others.Connection import Connection
from Enums.Next_message import Next_message
from Database.Actions.Inventory_db import all_using_to_inventory,print_inventory
from Gameobjects.Item import Item
from Database.Actions.Ability_CRUD import create_abiliti_owning,get_ability
from Gameobjects.Ability import Ability

class Inventory_level(CMD_level):
    """
    Třída znázorňujicí inventář.
    
    Atributy
    --------
    connect : Connection
        Instance třídy Connection, která reprezentuje spojení s klientem.
    base_prompt : str
        Řetězec promptu levelu ze kterého přicházím na inventář
    """
    
    def __init__(self, connect: Connection, base_prompt: str) -> None:
        super().__init__(
            connect=connect,
            prompt=f'{base_prompt}inventář>', 
            commands={
                "help":Full_help_command(self),
                "svleknout":Svleknout_command(self),#n nepovinných atributů
                "vypis_inventar":Print_inventory_command(self),
                "vypis_postavu":Print_character(self),
                "nasadit":Put_on_command(self),# jeden povinný a n nepovinných atributů
                "informace":Information_command(self),#jeden povinný atribut
                "zpet":Back_command(self),
                "pouzij":Use_command(self)#jeden povinný atribut
            })
        self.base_prompt:str=base_prompt
        
    def loop(self):
        self.connect.load_player()
        return super().loop()
    
    def supplementary_help(self):
        self.connect.send("-nasadit n x --[kód itemu, který chcete nasadit]=> nasadíte předměty",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("když napíšete kod itemu se stejným type jako jste už zadali tak se nasadí, ten později zadaný",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-informace --[kód itemu]=>vypíšou se informace o itemu, který vlastníte",next_message=Next_message.PRIJMI,prompt=self.prompt)        
        self.connect.send("-vypis_postavu=>vypíšou se  itemy, které má hráč na sobě",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-vypis_inventar=>vypíše všechny itemy, které uživatel má v inventáři",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-svleknout n x --[kód itemu, který chcete svléknout]=>postava svlekne všechno vynavení, které má na sobě",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-pouzij --[kód itemu, který chcete použít]=>použije se item",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-zpet=>vyjdete z inventáře",next_message=Next_message.PRIJMI,prompt=self.prompt)
        return super().supplementary_help()
    
class Full_help_command(ICommand):
    """
    Třída představující příkaz, který klintovy odešle, příkazy, které může použít.
    
    Atributy
    --------
    inventory : Inventory_level
        Instance třídy Inventory_level, ze které se přichází na příkaz.
    """
    
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
    """
    Třída představující příkaz, který svlékne itemy z postavy.
    
    Atributy
    --------
    inventory : Inventory_level
        Instance třídy Inventory_level, ze které se přichází na příkaz.
    """
    
    def __init__(self,inventory:Inventory_level) -> None:
        self.inventory:Inventory_level=inventory
    
    def execute(self,options:List[str]) -> bool:
        if not len(options)>=0:
            self.inventory.connect.send("Příkaz \"svleknout\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        if len(options)==0:
            all_using_to_inventory(self.inventory.connect.databaze,self.inventory.connect.player.username)
            self.inventory.connect.send("Všechny předměty byly svléknuty a dány do inventáře.",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            self.inventory.connect.load_player()
            return True
        else:
            for kod in options:
                if not len(kod)==4:
                    self.inventory.connect.send(f'Kód \"{kod}\" nesplňuje pravidla kódů itemů',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
                    continue
                if False in [element in [str(i) for i in range(10)] for element in kod]:
                    self.inventory.connect.send(f'Kód \"{kod}\" nesplňuje pravidla kódů itemů',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
                    continue
                if not kod in [item.code for item in self.inventory.connect.player.inventory]:
                    self.inventory.connect.send(f'Nevlastníte předmět s kódem \"{kod}\"',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
                    continue
                if not kod in [item.code for item in self.inventory.connect.player.inventory if item.is_using]:
                    self.inventory.connect.send(f'Nemáte nasazený předmět s kódem \"{kod}\"',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
                    continue
                for using_item in [item for item in self.inventory.connect.player.inventory if item.is_using]:
                    if using_item.code==kod:
                        using_item.is_using=False
                        break
            self.inventory.connect.save_player()
            self.inventory.connect.player.update_item_stats()
            return True
                
class Print_inventory_command(ICommand):
    """
    Třída představující příkaz, který klintovy odešle, itemy, které má postava v inventáři.
    
    Atributy
    --------
    inventory : Inventory_level
        Instance třídy Inventory_level, ze které se přichází na příkaz.
    """

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
    """
    Třída představující příkaz, který klintovy odešle, co má jeho postava na sobě.
    
    Atributy
    --------
    inventory : Inventory_level
        Instance třídy Inventory_level, ze které se přichází na příkaz.
    """
    
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
    """
    Třída představující příkaz, který nasadí item, který uživatel zadá.
    
    Atributy
    --------
    inventory : Inventory_level
        Instance třídy Inventory_level, ze které se přichází na příkaz.
    """
    
    def __init__(self,inventory:Inventory_level) -> None:
        self.inventory:Inventory_level=inventory
    
    def execute(self,options:List[str]) -> bool:
        if not len(options)>=1:
            self.inventory.connect.send("Příkaz \"nasadit\" má minimálně jeden povinný argument",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        for kod in options:
            if not len(kod)==4:
                self.inventory.connect.send(f'Kód \"{kod}\" nesplňuje pravidla kódů itemů',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
                continue
            if False in [element in [str(i) for i in range(10)] for element in kod]:
                self.inventory.connect.send(f'Kód \"{kod}\" nesplňuje pravidla kódů itemů',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
                continue
            if not kod in [item.code for item in self.inventory.connect.player.inventory]:
                self.inventory.connect.send(f'Nevlastníte předmět s kódem \"{kod}\"',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
                continue
            if not kod in [item.code for item in self.inventory.connect.player.inventory if not item.is_using]:
                self.inventory.connect.send(f'Nemáte v inventáři předmět s kódem \"{kod}\"',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
                continue
            if not kod in [item.code for item in self.inventory.connect.player.inventory if not item.is_using and not item.type in ["non_combat_useable","useable","combat_useable"]]:
                self.inventory.connect.send(f'Item s kóddem \"{kod}\" není nasaditelný',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
                continue
            change_item:Union[Item,None]=None
            for item in [element for element in self.inventory.connect.player.inventory if not element.is_using]:
                if item.code==kod:
                    item.is_using=True
                    change_item=item
                    break
            for is_using_item in [item for item in self.inventory.connect.player.inventory if item.is_using]:
                if change_item.type==is_using_item.type and not is_using_item is change_item:
                    is_using_item.is_using=False
        self.inventory.connect.save_player()
        self.inventory.connect.player.update_item_stats()
        return True
        
class Information_command(ICommand):
    """
    Třída představující příkaz, který klintovy odešle, informace o itemu, který zadá jako atribut.
    
    Atributy
    --------
    inventory : Inventory_level
        Instance třídy Inventory_level, ze které se přichází na příkaz.
    """
    
    def __init__(self,inventory:Inventory_level) -> None:
        self.inventory:Inventory_level=inventory
    
    def execute(self,options:List[str]) -> bool:
        if not len(options)==1:
            self.inventory.connect.send("Příkaz \"informace\" má 1 povinný atribut",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        kod:str=options[0]
        if not len(kod)==4:
            self.inventory.connect.send(f'Kód \"{kod}\" nesplňuje pravidla kódů itemů',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        if False in [element in [str(i) for i in range(10)] for element in kod]:
            self.inventory.connect.send(f'Kód \"{kod}\" nesplňuje pravidla kódů itemů',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        if not kod in [item.code for item in self.inventory.connect.player.inventory]:
            self.inventory.connect.send(f'Nevlastníte předmět s kódem \"{kod}\"',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        item:Item=[item for item in self.inventory.connect.player.inventory if item.code==kod][0]
        self.inventory.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.send(f'název:{item.nazev}',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.send(f'kod:{item.code}',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.send(f'typ:{item.type.upper()}',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.send(f'životy[hp]:{item.add_hp}',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.send(f'útok[atk]:{item.add_atk}',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.send(f'mana:{item.add_mana}',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.send(f'rychlost[speed]:{item.add_speed}',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        if item.ability==None:
            self.inventory.connect.send(f'schopnost[ability]:-',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        else:
            self.inventory.connect.send(f'schopnost[ability]:{item.ability}',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        self.inventory.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
        return True

class Back_command(ICommand):
    """
    Třída představující příkaz, který vyhodí klienta z inventáře.
    
    Atributy
    --------
    inventory : Inventory_level
        Instance třídy Inventory_level, ze které se přichází na příkaz.
    """
    
    def __init__(self,inventory:Inventory_level) -> None:
        self.inventory:Inventory_level=inventory
    
    def execute(self,options:List[str]) -> bool:
        if not len(options)==0:
            self.inventory.connect.send("Příkaz \"zpet\" nemá žádné atributy",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        return False
    
class Use_command(ICommand):
    """
    Třída představující příkaz, který použije item, který uživatel zadá jako atribut
    
    Atributy
    --------
    inventory : Inventory_level
        Instance třídy Inventory_level, ze které se přichází na příkaz.
    """
    
    def __init__(self,inventory:Inventory_level) -> None:
        self.inventory:Inventory_level=inventory
    
    def execute(self,options:List[str]) -> bool:
        if not len(options)==1:
            self.inventory.connect.send("Příkaz \"pouzij\" má jeden povinný atribut",next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        kod:str=options[0]
        if not len(kod)==4:
            self.inventory.connect.send(f'Kód \"{kod}\" nesplňuje pravidla kódů itemů',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        if False in [element in [str(i) for i in range(10)] for element in kod]:
            self.inventory.connect.send(f'Kód \"{kod}\" nesplňuje pravidla kódů itemů',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        if not kod in [item.code for item in self.inventory.connect.player.inventory]:
            self.inventory.connect.send(f'Nevlastníte předmět s kódem \"{kod}\"',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        item:Item=[item for item in self.inventory.connect.player.inventory if item.code==kod][0]
        if not item.type in ["useable","non_combat_useable"]:
            self.inventory.connect.send(f'Předmět s kódem \"{kod}\" nelze použít',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            return True
        item:Union[Item,None]=None
        for for_item in self.inventory.connect.player.inventory:
            if not for_item.is_using and for_item.code==kod:
                item:Item=for_item
                break
        if item==None:
            return True
        if item.code=="0009" or item.code=="0013": # health potion or beer
            if self.inventory.connect.player.get_full_hp()>=item.add_hp+self.inventory.connect.player.current_hp:
                self.inventory.connect.player.current_hp+=item.add_hp
                self.inventory.connect.send(f'Vyléčil jste si {item.add_hp} životů',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
                self.inventory.connect.player.inventory.remove(item)
            elif self.inventory.connect.player.get_full_hp()==self.inventory.connect.player.current_hp :
                self.inventory.connect.send(f'Nelze vyléčit, už máte plný počet životů',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            else:
                self.inventory.connect.send(f'Vyléčil jste si {self.inventory.connect.player.get_full_hp()-self.inventory.connect.player.current_hp} životů',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
                self.inventory.connect.player.current_hp=self.inventory.connect.player.get_full_hp()
                self.inventory.connect.player.inventory.remove(item)
            self.inventory.connect.save_player()
            return True
        elif item.code=="0010": #mana potion
            if self.inventory.connect.player.get_full_mana()>=item.add_mana+self.inventory.connect.player.current_mana:
                self.inventory.connect.player.current_mana+=item.add_mana
                self.inventory.connect.send(f'Přidal jste si {item.add_mana} many',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
                self.inventory.connect.player.inventory.remove(item)
            elif self.inventory.connect.player.get_full_mana()==self.inventory.connect.player.current_mana :
                self.inventory.connect.send(f'Nelze přidat manu, už máte plno many',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
            else:
                self.inventory.connect.send(f'Přidal jste si {self.inventory.connect.player.get_full_mana()-self.inventory.connect.player.current_mana} many',next_message=Next_message.PRIJMI,prompt=self.inventory.prompt)
                self.inventory.connect.player.current_mana=self.inventory.connect.player.get_full_mana()
                self.inventory.connect.player.inventory.remove(item)
            self.inventory.connect.save_player()
            return True
        elif item.code=="0014":
            create_abiliti_owning(self.inventory.connect.databaze,self.inventory.connect.player.username,"A001")
            tmp:Ability=Ability()
            tmp.create_by_tuple(get_ability(self.inventory.connect.databaze,"A0001"))
            self.inventory.connect.player.abilities.append(tmp)
            self.inventory.connect.player.inventory.remove(item)
            return True
        raise NotImplementedError("inventar-pouzij")