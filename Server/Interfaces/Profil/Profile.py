from Others.Connection import Connection
from lib.ICommand import ICommand
from Enums.Next_message import Next_message
from Others.Help_methods import edit_response
from Database.Actions.Authentication import username_exists
from Interfaces.CMD_level import CMD_level


class Profil_view(CMD_level):
    
    def __init__(self,connect:Connection,prompt:str,username:str|None=None) -> None:
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
            "back":Zpet_command(self),
            "help":Help_command(self),
            "staty":None,
            "info":None
            }
        )
        
    def loop(self):
        super().loop()
    
class Help_command(ICommand):
    
    def __init__(self,profil:Profil_view) -> None:
        self.profil:Profil_view=profil
    
    def execute(self,options:list) -> bool:
        if not len(options)==0:
            self.profil.connect.send("Příkaz \"help\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
            return True
        self.profil.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.connect.send("-back=>odejdete z profilu",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.connect.send("-help=>vypíšou se všechny příkazy, které můžete aktuálně použít",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        self.profil.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
        return True
    
class Zpet_command(ICommand):
    
    def __init__(self,profil:Profil_view) -> None:
        self.profil:Profil_view=profil
    
    def execute(self,options:list) -> bool:
        if not len(options)==0:
            self.profil.connect.send("Příkaz \"back\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=self.profil.prompt)
            return True
        return False