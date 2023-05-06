from Others.Connection import Connection
from Enums.Next_message import Next_message
from Interfaces.Load_user import Load_user
from lib.ICommand import ICommand
from Database.Actions.Set_status import set_online
from Database.Actions.Authentication import login
from Gameobjects.Player import Player
from Database.Actions.Authentication import username_exists
from Database.Actions.Get_user_informations import player_is_online

name_of_game:str="""███╗   ███╗██╗   ██╗███████╗████████╗██╗ ██████╗         ██╗███████╗██╗    ██╗███████╗██╗     ███████╗
████╗ ████║╚██╗ ██╔╝██╔════╝╚══██╔══╝██║██╔════╝         ██║██╔════╝██║    ██║██╔════╝██║     ██╔════╝
██╔████╔██║ ╚████╔╝ ███████╗   ██║   ██║██║              ██║█████╗  ██║ █╗ ██║█████╗  ██║     ███████╗
██║╚██╔╝██║  ╚██╔╝  ╚════██║   ██║   ██║██║         ██   ██║██╔══╝  ██║███╗██║██╔══╝  ██║     ╚════██║
██║ ╚═╝ ██║   ██║   ███████║   ██║   ██║╚██████╗    ╚█████╔╝███████╗╚███╔███╔╝███████╗███████╗███████║
╚═╝     ╚═╝   ╚═╝   ╚══════╝   ╚═╝   ╚═╝ ╚═════╝     ╚════╝ ╚══════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝
"""

class First_view:
    
    prompt=">"

    def __init__(self,connect:Connection) -> None:
        self.connect=connect
        self.commands:dict={
            "help":Help_command,
            "login":Login_command,
            "register":Register_command,
            "exit":Exit_command
        }
        
    def loop(self)->None:
        self.connect.send(name_of_game,next_message=Next_message.POSLI,prompt=self.prompt)
        while True:
            client_response:str = self.connect.recieve(next_message=Next_message.PRIJMI)
            client_response:str=client_response.strip()
            command:str=self.commands.get(client_response,None)
            if not command==None:
                command(self.connect).execute()
            else:
                self.connect.send("Neznámý příkaz",Next_message.PRIJMI)
            self.connect.send("",next_message=Next_message.POSLI)
    
    def do_register(self)->None:
        self.connect.send("",next_message=Next_message.POSLI,prompt="přezdívka:")
        username:str=self.connect.recieve(next_message=Next_message.POSLI,prompt="heslo:",typ="heslo")
        heslo:str=self.connect.recieve(next_message=Next_message.POSLI,prompt="potvrzení hesla:",typ="heslo")
        heslo_potvrz:str=self.connect.recieve(next_message=Next_message.PRIJMI,prompt="")
        """
        TODO
        kontrola integrity
        """
        try:
            self.connect.databaze.register_user(username,heslo)
            self.connect.send("Ůčet vytvořen úspěšně",next_message=Next_message.POSLI)
        except:    
            self.connect.send("Ůčet nejde vytvořit",next_message=Next_message.POSLI)
            
class Help_command(ICommand):
    
    def __init__(self,connect:Connection) -> None:
        self.connect:Connection=connect
        
    def execute(self):
        self.connect.send("",next_message=Next_message.PRIJMI)
        self.connect.send("----------------------",next_message=Next_message.PRIJMI)
        self.connect.send("-help=>vypíšou se všechny příkazy, které můžete aktuálně použít",next_message=Next_message.PRIJMI)
        self.connect.send("-login=>přihlášení",next_message=Next_message.PRIJMI)
        self.connect.send("-register=>registrace",next_message=Next_message.PRIJMI)
        self.connect.send("-exit=>ukončení programu",next_message=Next_message.PRIJMI)
        self.connect.send("----------------------",next_message=Next_message.PRIJMI)
        self.connect.send("",next_message=Next_message.PRIJMI)
        
class Login_command(ICommand):
    
    def __init__(self,connect:Connection) -> None:
        self.connect:Connection=connect
        
    def execute(self):
        self.connect.send("",next_message=Next_message.PRIJMI)
        try:
            self.connect.send("",next_message=Next_message.POSLI,prompt="přezdívka:")
            username:str=self.connect.recieve(next_message=Next_message.PRIJMI)
            if not username_exists(self.connect.databaze,username):
                self.connect.send(f'Uživatelské jméno \"{username}\" neexistuje',next_message=Next_message.PRIJMI)
                return
            else:
                self.connect.send("",next_message=Next_message.POSLI,prompt="heslo:",typ="heslo")
            password:str=self.connect.recieve(next_message=Next_message.PRIJMI)
            if login(self.connect,username,password):
                if player_is_online(self.connect.databaze,username):
                    self.connect.send(f'Uživatel \"{username}\" je online',next_message=Next_message.PRIJMI)
                    return
                self.connect.player=Player(username)
                set_online(self.connect.databaze,username,1)
                Load_user(self.connect).load()
            else:
                self.connect.send("Neúspěšné přihlášení",next_message=Next_message.PRIJMI)
        except ConnectionResetError:
            if not self.connect.player.username==None:
                    set_online(self.connect.databaze,self.connect.player.username,0)
            raise ConnectionResetError()
        self.connect.send("",next_message=Next_message.PRIJMI)
    
class Register_command(ICommand):

    def __init__(self,connect:Connection) -> None:
        self.connect:Connection=connect
        
    def execute(self):
        raise NotImplementedError("Register")
    
class Exit_command(ICommand):
    
    def __init__(self,connect:Connection) -> None:
        self.connect:Connection=connect
        
    def execute(self):
        self.connect.close_connection()
        
                
if __name__=="__main__":
    pass