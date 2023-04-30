from Others.Connection import Connection
from Enums.Next_message import Next_message
from Gameobjects.Player import Player
from Gameobjects.Map.Places.Capital_city import Capital_city

class Load_user:
    def __init__(self,connect:Connection) -> None:
        self.connect:Connection=connect
    
    def load(self):
        location,building=self.connect.database_get_location()
        if location==1 or location==None:
            place=Capital_city(self.connect)
            self.connect.send("úspěšné přihlášení",next_message=Next_message.POSLI,prompt=f'{place.promtp}')
            place.loop()
        else:
            raise NotImplementedError('Load')