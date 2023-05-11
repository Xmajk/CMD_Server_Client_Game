from Others.Connection import Connection
from Enums.Next_message import Next_message
from Gameobjects.Player import Player
from Gameobjects.Map.Capital_city.Capital_city import Capital_city
from Database.Actions.Get_user_informations import get_location

class Load_user:
    def __init__(self,connect:Connection) -> None:
        self.connect:Connection=connect
    
    def load(self):
        location,building=get_location(self.connect.databaze,self.connect.player)
        self.connect.send("úspěšné přihlášení",next_message=Next_message.PRIJMI)
        if location==1:
            place=Capital_city(self.connect)
            place.loop()
        else:
            raise NotImplementedError('Load')