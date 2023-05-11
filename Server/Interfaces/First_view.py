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

name_of_game:str="""███╗   ███╗██╗   ██╗███████╗████████╗██╗ ██████╗         ██╗███████╗██╗    ██╗███████╗██╗     ███████╗
████╗ ████║╚██╗ ██╔╝██╔════╝╚══██╔══╝██║██╔════╝         ██║██╔════╝██║    ██║██╔════╝██║     ██╔════╝
██╔████╔██║ ╚████╔╝ ███████╗   ██║   ██║██║              ██║█████╗  ██║ █╗ ██║█████╗  ██║     ███████╗
██║╚██╔╝██║  ╚██╔╝  ╚════██║   ██║   ██║██║         ██   ██║██╔══╝  ██║███╗██║██╔══╝  ██║     ╚════██║
██║ ╚═╝ ██║   ██║   ███████║   ██║   ██║╚██████╗    ╚█████╔╝███████╗╚███╔███╔╝███████╗███████╗███████║
╚═╝     ╚═╝   ╚═╝   ╚══════╝   ╚═╝   ╚═╝ ╚═════╝     ╚════╝ ╚══════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝
"""

class First_view:
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
        self.connect:Connection=connect
        self.commands:dict={
            "help":Help_command(),
            "login":Login_command(),
            "registrovat":Register_command(),
            "exit":Exit_command()
        }
        
    def loop(self)->None:
        """
        Loop interfacu, který se zobrazí ihned po pripojení uživatele.
        Přijímá vstup od uživatele, který je poté interpretován jako příkaz a vykonán.
        """
        self.connect.send(name_of_game,next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send("Autor: Michal Hrouda",next_message=Next_message.PRIJMI,prompt=self.prompt)
        self.connect.send(" ",next_message=Next_message.POSLI,prompt=self.prompt)
        while True:
            client_response:str = self.connect.recieve(next_message=Next_message.PRIJMI)
            client_response:str=client_response.strip()
            command:ICommand=self.commands.get(client_response,Neznamy_command())
            if not command==None:
                command.execute(self.connect)
            else:
                self.connect.send("Neznámý příkaz",Next_message.PRIJMI)
            self.connect.send("",next_message=Next_message.POSLI)
            
class Help_command(ICommand):
    
    def __init__(self) -> None:
        pass
        
    def execute(self,connect:Connection)->None:
        connect.send("",next_message=Next_message.PRIJMI)
        connect.send("----------------------",next_message=Next_message.PRIJMI)
        connect.send("-login=>přihlášení",next_message=Next_message.PRIJMI)
        connect.send("-registrovat=>registrace",next_message=Next_message.PRIJMI)
        connect.send("-help=>vypíšou se všechny příkazy, které můžete aktuálně použít",next_message=Next_message.PRIJMI)
        connect.send("-exit=>ukončení programu",next_message=Next_message.PRIJMI)
        connect.send("----------------------",next_message=Next_message.PRIJMI)
        connect.send("",next_message=Next_message.PRIJMI)
        
class Login_command(ICommand):
    
    def __init__(self) -> None:
        pass
        
    def execute(self,connect:Connection)->None:
        connect.send("",next_message=Next_message.PRIJMI)
        try:
            connect.send("",next_message=Next_message.POSLI,prompt="přezdívka:")
            username:str=connect.recieve(next_message=Next_message.PRIJMI)
            if not username_exists(connect.databaze,username):
                connect.send(f'Uživatelské jméno \"{username}\" neexistuje',next_message=Next_message.PRIJMI)
                return
            else:
                connect.send("",next_message=Next_message.POSLI,prompt="heslo:",typ="heslo")
            password:str=connect.recieve(next_message=Next_message.PRIJMI)
            if login(connect,username,password):
                if player_is_online(connect.databaze,username):
                    connect.send(f'Uživatel \"{username}\" je online',next_message=Next_message.PRIJMI)
                    return
                connect.player=Player(username)
                set_online(connect.databaze,username,1)
                Load_user(connect).load()
            else:
                connect.send("Neúspěšné přihlášení",next_message=Next_message.PRIJMI)
        except ConnectionResetError:
            if not connect.player.username==None:
                    set_online(connect.databaze,connect.player.username,0)
            raise ConnectionResetError()
        connect.send("",next_message=Next_message.PRIJMI)
    
class Register_command(ICommand):

    def __init__(self) -> None:
        pass
        
    def execute(self,connect:Connection)->None:
        Register_view(connect).loop()
    
class Exit_command(ICommand):
    
    def __init__(self) -> None:
        pass
        
    def execute(self,connect:Connection)->None:
        connect.close_connection()
        
class Neznamy_command(ICommand):
    
    def __init__(self) -> None:
        pass
    
    def execute(self,connect:Connection) -> bool:
        connect.send("Neznámý příkaz",next_message=Next_message.PRIJMI)
        return True
        
                
if __name__=="__main__":
    pass