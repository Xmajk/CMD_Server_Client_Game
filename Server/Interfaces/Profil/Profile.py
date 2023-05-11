from Others.Connection import Connection
from lib.ICommand import ICommand
from Enums.Next_message import Next_message
from Others.Help_methods import edit_response
from Database.Actions.Authentication import username_exists

class Profil_view:
    
    def __init__(self,connect:Connection,prompt:str,username:str|None) -> None:
        self.connect:Connection=connect
        self.prompt:str=prompt+"profil>"
        self.commands:dict={
            "back":Zpet_command(),
            "help":Help_command(),
            "staty":None,
            "info":None
        }
        
    def loop(self):
        self.connect.send("",next_message=Next_message.POSLI,prompt=self.prompt)
        while True:
            client_response:str=self.connect.recieve(next_message=Next_message.PRIJMI,prompt=self.prompt)
            client_command,options=edit_response(client_response)
            client_command:ICommand=self.commands.get(client_command,Neznamy_command())
            if not client_command.execute(self,options):return
            self.connect.send("",next_message=Next_message.POSLI,prompt=self.prompt)
            
class Neznamy_command(ICommand):
    
    def __init__(self) -> None:
        pass
    
    def execute(self,profil_view:Profil_view,options:list) -> bool:
        profil_view.connect.send("Neznámý příkaz",next_message=Next_message.PRIJMI,prompt=profil_view.prompt)
        return True
    
class Help_command(ICommand):
    
    def __init__(self) -> None:
        pass
    
    def execute(self,profil_view:Profil_view,options:list) -> bool:
        if not len(options)==0:
            profil_view.connect.send("Příkaz \"help\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=profil_view.prompt)
            return True
        profil_view.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=profil_view.prompt)
        profil_view.connect.send("-back=>odejdete z profilu",next_message=Next_message.PRIJMI,prompt=profil_view.prompt)
        profil_view.connect.send("-help=>vypíšou se všechny příkazy, které můžete aktuálně použít",next_message=Next_message.PRIJMI,prompt=profil_view.prompt)
        profil_view.connect.send("----------------------",next_message=Next_message.PRIJMI,prompt=profil_view.prompt)
        return True
    
class Zpet_command(ICommand):
    def __init__(self) -> None:
        pass
    
    def execute(self,profil_view:Profil_view,options:list) -> bool:
        if not len(options)==0:
            profil_view.connect.send("Příkaz \"back\" nemá žádné argumenty",next_message=Next_message.PRIJMI,prompt=profil_view.prompt)
            return True
        return False