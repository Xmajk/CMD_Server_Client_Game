from Others.Connection import Connection
from Enums.Next_message import Next_message
from Interfaces.Load_user import Load_user
from lib.ICommand import ICommand
from Database.Actions.Set_status import set_online
from Database.Actions.Authentication import login
from Gameobjects.Player import Player
from Database.Actions.Authentication import username_exists
from Database.Actions.Get_user_informations import player_is_online
from Interfaces.Register_view import Register_view
from Interfaces.CMD_level import CMD_level

name_of_game:str="""███╗   ███╗██╗   ██╗███████╗████████╗██╗ ██████╗         ██╗███████╗██╗    ██╗███████╗██╗     ███████╗
████╗ ████║╚██╗ ██╔╝██╔════╝╚══██╔══╝██║██╔════╝         ██║██╔════╝██║    ██║██╔════╝██║     ██╔════╝
██╔████╔██║ ╚████╔╝ ███████╗   ██║   ██║██║              ██║█████╗  ██║ █╗ ██║█████╗  ██║     ███████╗
██║╚██╔╝██║  ╚██╔╝  ╚════██║   ██║   ██║██║         ██   ██║██╔══╝  ██║███╗██║██╔══╝  ██║     ╚════██║
██║ ╚═╝ ██║   ██║   ███████║   ██║   ██║╚██████╗    ╚█████╔╝███████╗╚███╔███╔╝███████╗███████╗███████║
╚═╝     ╚═╝   ╚═╝   ╚══════╝   ╚═╝   ╚═╝ ╚═════╝     ╚════╝ ╚══════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝
"""

class First_view(CMD_level):
    """
    Třída, která zajišťuje první pohled uživatele do hry.
    Zobrazuje prompt a přijímá vstup od uživatele, který je poté
    interpretován jako příkaz a vykonán. Podporované příkazy jsou
    předem definovány v slovníku `commands`.
    
    Parametry:
    ----------

    Atributy:
    ---------
    - connect: Connection - instance třídy Connection pro komunikaci s klientem
    - commands: dict - slovník příkazů, kde klíčem je název příkazu a hodnotou je třída příkazu
    """
    
    prompt=">"

    def __init__(self,connect:Connection) -> None:
        super().__init__(
            connect=connect,
            prompt=">",
            commands={
            "help":Help_command(self),
            "login":Login_command(self),
            "registrovat":Register_command(self),
            "exit":Exit_command(self)
            }
        )
        
    def loop(self)->None:
        """
        Loop interfacu, který se zobrazí ihned po pripojení uživatele.
        Přijímá vstup od uživatele, který je poté interpretován jako příkaz a vykonán.
        """
        for element in name_of_game.split("\n"):
            self.connect.send(element,next_message=Next_message.PRIJMI,prompt=self.prompt)
        #self.connect.send(name_of_game,next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("Autor: Michal Hrouda",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send(" ",next_message=Next_message.PRIJMI,prompt=self.prompt)
        super().loop()
            
class Help_command(ICommand):
    
    def __init__(self,first_view:First_view) -> None:
        self.first_view:First_view=first_view
        
    def execute(self,options:list)->None:
        self.first_view.connect.send("",next_message=Next_message.PRIJMI)
        self.first_view.connect.send("----------------------",next_message=Next_message.PRIJMI)
        self.first_view.connect.send("-login=>přihlášení",next_message=Next_message.PRIJMI)
        self.first_view.connect.send("-registrovat=>registrace",next_message=Next_message.PRIJMI)
        self.first_view.connect.send("-help=>vypíšou se všechny příkazy, které můžete aktuálně použít",next_message=Next_message.PRIJMI)
        self.first_view.connect.send("-exit=>ukončení programu",next_message=Next_message.PRIJMI)
        self.first_view.connect.send("----------------------",next_message=Next_message.PRIJMI)
        self.first_view.connect.send("",next_message=Next_message.PRIJMI)
        return True
        
class Login_command(ICommand):
    
    def __init__(self,first_view:First_view) -> None:
        self.first_view:First_view=first_view
        
    def execute(self,options:list)->None:
        self.first_view.connect.send("",next_message=Next_message.PRIJMI)
        try:
            self.first_view.connect.send("",next_message=Next_message.POSLI,prompt="přezdívka:")
            username:str=self.first_view.connect.recieve(next_message=Next_message.PRIJMI)
            if not username_exists(self.first_view.connect.databaze,username):
                self.first_view.connect.send(f'Uživatelské jméno \"{username}\" neexistuje',next_message=Next_message.PRIJMI)
                return True
            else:
                self.first_view.connect.send("",next_message=Next_message.POSLI,prompt="heslo:",typ="heslo")
            password:str=self.first_view.connect.recieve(next_message=Next_message.PRIJMI)
            if login(self.first_view.connect,username,password):
                if player_is_online(self.first_view.connect.databaze,username):
                    self.first_view.connect.send(f'Uživatel \"{username}\" je online',next_message=Next_message.PRIJMI)
                    return True
                self.first_view.connect.player=Player(username)
                set_online(self.first_view.connect.databaze,username,1)
                self.first_view.connect.load_player()
                Load_user(self.first_view.connect).load()
            else:
                self.first_view.connect.send("Neúspěšné přihlášení",next_message=Next_message.PRIJMI)
        except ConnectionResetError:
            if not self.first_view.connect.player.username==None:
                    set_online(self.first_view.connect.databaze,self.first_view.connect.player.username,0)
            raise ConnectionResetError()
        self.first_view.connect.send("",next_message=Next_message.PRIJMI)
        return True
    
class Register_command(ICommand):

    def __init__(self,first_view:First_view) -> None:
        self.first_view:First_view=first_view
        
    def execute(self,options:list)->None:
        Register_view(self.first_view.connect).loop()
        return True
    
class Exit_command(ICommand):
    
    def __init__(self,first_view:First_view) -> None:
        self.first_view:First_view=first_view
        
    def execute(self,options:list)->None:
        self.first_view.connect.close_connection()
        
                
if __name__=="__main__":
    pass