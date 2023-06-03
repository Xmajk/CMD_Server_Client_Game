from Others.Connection import Connection
from lib.ICommand import ICommand
from Enums.Next_message import Next_message
from Others.Help_methods import edit_response
from Database.Actions.Authentication import username_exists
from Interfaces.CMD_level import CMD_level
from typing import Union
from Gameobjects.Player import Player
from Database.Actions.Get_user_informations import player_is_online

class Profil_view(CMD_level):
    """
    Třída znázorňujicí profil.
    
    Atributy
    --------
    connect : Connection
        Instance třídy Connection, která reprezentuje spojení s klientem.
    prompt : str
        Řetězec promptu levelu ze kterého přicházím na inventář.
    username : str|None
        Username uživatele na kterého se chceme podívat.
    """
    
    def __init__(self,connect:Connection,prompt:str,username:Union[str,None]=None) -> None:
        self.username:str=username
        if username==None:
            add_prompt:str="profil>"
        else:
            add_prompt:str=f'profil[{self.username}]>'
        super().__init__(
            connect=connect,
            prompt=prompt+add_prompt,
            commands={
            "zpet":Zpet_command(self),
            "help":Help_command(self),
            "staty":Print_stats_command(self),
            "je_online":Is_online_command(self),
            "informace":Information_command(self)
            }
        )
        
    def supplementary_help(self):
        self.connect.send("-staty=>vypíšou se v tabulce staty",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-je_online=>zobrazí se jestli je hráč online",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-informace=>vypíšou se informace o uživateli",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("-zpet=>odejdete z profilu",next_message=Next_message.PRIJMI,prompt=self.prompt)
        return super().supplementary_help()
        
        
    def loop(self):
        super().loop()
    
class Help_command(ICommand):
    """
    Třída představující příkaz, který klintovy odešle, příkazy, které může použít.
    
    Atributy
    --------
    profil : Profil_view
        Instance třídy Profil_view, ze které se přichází na příkaz.
    """
    
    def __init__(self,profil:Profil_view) -> None:
        self.profil:Profil_view=profil
    
    def execute(self,options:list) -> bool:
        if not len(options)==0:
            self.profil.connect.send("Příkaz \"help\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
            return True
        self.profil.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.supplementary_help()
        self.profil.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        return True
    
class Zpet_command(ICommand):
    """
    Třída představující příkaz, díky kterému se uživatel dostane z profilu.
    
    Atributy
    --------
    profil : Profil_view
        Instance třídy Profil_view, ze které se přichází na příkaz.
    """
    
    def __init__(self,profil:Profil_view) -> None:
        self.profil:Profil_view=profil
    
    def execute(self,options:list) -> bool:
        if not len(options)==0:
            self.profil.connect.send("Příkaz \"zpet\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
            return True
        return False
    
class Print_stats_command(ICommand):
    """
    Třída představující příkaz, díky kterému si uživatel vypíše staty uživatele
    
    Atributy
    --------
    profil : Profil_view
        Instance třídy Profil_view, ze které se přichází na příkaz.
    """
    
    def __init__(self,profil:Profil_view) -> None:
        self.profil:Profil_view=profil
    
    def execute(self,options:list) -> bool:
        if not len(options)==0:
            self.profil.connect.send("Příkaz \"staty\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
            return True
        if self.profil.username==None:
            tmp_player:Player=self.profil.connect.player
        else:
            tmp_player:Player=Player(self.profil.username)
            tmp_player.load(self.profil.connect.databaze)
        tmp_player.update_item_stats()
        header:str=f'| stat | třídy | přidaný | z itemů |'
        self.profil.connect.send('_'*36,next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.connect.send(header,next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.connect.send(f'| hp   | {tmp_player.base_hp:5} | {tmp_player.add_hp:7} | {tmp_player.items_hp:7} |',next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.connect.send(f'| atk  | {tmp_player.base_atk:5} | {tmp_player.add_atk:7} | {tmp_player.items_atk:7} |',next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.connect.send(f'| mana | {tmp_player.base_mana:5} | {tmp_player.add_mana:7} | {tmp_player.items_mana:7} |',next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.connect.send(f'| speed| {tmp_player.base_speed:5} | {tmp_player.add_speed:7} | {tmp_player.items_speed:7} |',next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.connect.send('_'*36,next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        return True

class Is_online_command(ICommand):
    """
    Třída představující příkaz, díky kterému si zjistíme, jestli je uživatel online
    
    Atributy
    --------
    profil : Profil_view
        Instance třídy Profil_view, ze které se přichází na příkaz.
    """
    
    def __init__(self,profil:Profil_view) -> None:
        self.profil:Profil_view=profil
    
    def execute(self,options:list) -> bool:
        if not len(options)==0:
            self.profil.connect.send("Příkaz \"je_online\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
            return True
        if self.profil.username==None:
            tmp_username:str=self.profil.connect.player.username
        else:
            tmp_username:str=self.profil.username
        if player_is_online(self.profil.connect.databaze,tmp_username):
            self.profil.connect.send(f'Uživatel \"{tmp_username}\" je online',next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        else:
            self.profil.connect.send(f'Uživatel \"{tmp_username}\" není online',next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        return True
    
class Information_command(ICommand):
    """
    Třída představující příkaz, který vypíše informace o uživateli
    
    Atributy
    --------
    profil : Profil_view
        Instance třídy Profil_view, ze které se přichází na příkaz.
    """
    
    def __init__(self,profil:Profil_view) -> None:
        self.profil:Profil_view=profil
    
    def execute(self,options:list) -> bool:
        if not len(options)==0:
            self.profil.connect.send("Příkaz \"informace\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
            return True
        if self.profil.username==None:
            tmp_player:Player=self.profil.connect.player
        else:
            tmp_player:Player=Player(self.profil.username)
            tmp_player.load(self.profil.connect.databaze)
        self.profil.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.connect.send(f'hp: {tmp_player.current_hp}/{tmp_player.get_full_hp()}',next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.connect.send(f'atk: {tmp_player.get_full_speed()}',next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.connect.send(f'mana: {tmp_player.current_mana}/{tmp_player.get_full_mana()}',next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.connect.send(f'speed: {tmp_player.get_full_speed()}',next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.connect.send(f'třída: {tmp_player.trida.upper()}',next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        if player_is_online(self.profil.connect.databaze,tmp_player.username):
            self.profil.connect.send(f'Uživatel je online',next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        else:
            self.profil.connect.send(f'Uživatel není online',next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        return True