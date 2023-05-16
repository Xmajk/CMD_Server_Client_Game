from Others.Connection import Connection
from Enums.Next_message import Next_message
from Gameobjects.Player import Player
from Gameobjects.Map.Capital_city.Capital_city import Capital_city
from Gameobjects.Map.Route1.Route1 import Route1
from Database.Actions.Get_user_informations import get_location
from Gameobjects.Map.Capital_city.Capital_city_tawern import Capital_city_tawern

class Load_user:
    def __init__(self,connect:Connection) -> None:
        self.connect:Connection=connect
    
    def load(self):
        location,building=get_location(self.connect.databaze,self.connect.player)
        print(location,building)
        self.connect.send("úspěšné přihlášení",next_message=Next_message.PRIJMI)
        if location=="Hlavní město":
            if building == "hospoda":
                Capital_city_tawern(self.connect).loop()
            place=Capital_city(self.connect)
            place.loop()
        if location=="Route1":
            Route1(self.connect).loop()
        else:
            raise NotImplementedError('Load')