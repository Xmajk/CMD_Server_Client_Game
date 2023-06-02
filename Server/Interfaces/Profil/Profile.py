from Others.Connection import Connection
from lib.ICommand import ICommand
from Enums.Next_message import Next_message
from Others.Help_methods import edit_response
from Database.Actions.Authentication import username_exists
from Interfaces.CMD_level import CMD_level
from typing import Union


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
        if username==None:
            self.username=connect.player.username
            add_prompt:str="profil>"
        else:
            self.username:str=username
            add_prompt:str=f'profil[{self.username}]>'
        super().__init__(
            connect=connect,
            prompt=prompt+add_prompt,
            commands={
            "zpet":Zpet_command(self),
            "help":Help_command(self),
            "staty":None,
            "info":None,
            "vypis_vse":None
            }
        )
        
    def supplementary_help(self):
        self.connect.send("-zpet=>odejdete z profilu",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.connect.send("-help=>vypíšou se všechny příkazy, které můžete aktuálně použít",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
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