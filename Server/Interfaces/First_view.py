from Others.Connection import Connection
from Enums.Next_message import Next_message
from Interfaces.Load_user import Load_user

name_of_game:str="""███╗   ██╗ █████╗ ███╗   ███╗███████╗     ██████╗ ███████╗     ██████╗  █████╗ ███╗   ███╗███████╗
████╗  ██║██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██╔════╝    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝
██╔██╗ ██║███████║██╔████╔██║█████╗      ██║   ██║█████╗      ██║  ███╗███████║██╔████╔██║█████╗  
██║╚██╗██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║██╔══╝      ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  
██║ ╚████║██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝██║         ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═╝          ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
"""

class Login_int:
    
    prompt=">"

    def __init__(self,connect:Connection) -> None:
        self.connect=connect
        self.loop()
        
    def loop(self)->None:
        self.connect.send(name_of_game,next_message=Next_message.POSLI,prompt=self.prompt)
        while True:
            client_response:str = self.connect.recieve(next_message=Next_message.PRIJMI)
            if client_response=="help":
                help_message:str="""----------------------
-help=vypíšou se všechny příkazy, které můžete aktuálně použít
-login=přihlášení
-register=registrace
----------------------"""
                self.connect.send(help_message,next_message=Next_message.POSLI,prompt=self.prompt)
            elif client_response=="login":
                self.do_login()
            elif client_response=="register":
                self.do_register()
            else:
                self.connect.send("neznámý příkaz",next_message=Next_message.POSLI,prompt=self.prompt)
    def do_login(self):
        self.connect.send("",next_message=Next_message.POSLI,prompt="přezdívka:")
        username:str=self.connect.recieve(next_message=Next_message.POSLI,prompt="heslo:",typ="heslo")
        password:str=self.connect.recieve(next_message=Next_message.PRIJMI)
        login_succesful:bool=self.connect.login(username,password)
        if login_succesful:
            self.connect.player.username=username
            Load_user(self.connect).load()
        else:
            self.connect.send("neúspěšné přihlášení",next_message=Next_message.POSLI)
    
    def do_register(self):
        raise NotImplementedError("Přidat registraci")
                
if __name__=="__main__":
    pass