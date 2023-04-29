from Others.Connection import Connection
from Enums.Next_message import Next_message
from Gameobjects.Player import Player

class Load_user:
    def __init__(self,connect:Connection) -> None:
        self.connect:Connection=connect
    
    def load(self):
        
        self.connect.send("úspěšné přihlášení",next_message=Next_message.POSLI,prompt=f'{self.connect.player.username}>')