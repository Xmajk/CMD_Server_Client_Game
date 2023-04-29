from Others.Connection import Connection
from Enums.Next_message import Next_message

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
            print(client_response)
            if client_response=="help":
                self.connect.send("nevim\nnevim2\nnevim3 --option",next_message=Next_message.POSLI,prompt=self.prompt)
            else:
                self.connect.send("neznámí příkaz",next_message=Next_message.POSLI,prompt=self.prompt)