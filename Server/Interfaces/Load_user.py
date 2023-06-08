from Others.Connection import Connection
from Enums.Next_message import Next_message
from Gameobjects.Player import Player
from Gameobjects.Map.Capital_city.Capital_city import Capital_city
from Gameobjects.Map.Route1.Route1 import Route1
from Database.Actions.Get_user_informations import get_location
from Gameobjects.Map.Capital_city.Capital_city_tawern import Capital_city_tawern
from Gameobjects.Map.Forest.Forest import Forest 
from Gameobjects.Map.Route2.Route2 import Route2
from Gameobjects.Map.Gem_town.Gem_town import Gem_town

class Load_user:
    """
    Třída sloužící pro načtení uživatele.
    
    Atributy
    --------
    connect : Connection
        Instance třídy Connection, která reprezentuje spojení s klientem.
    """
    def __init__(self,connect:Connection) -> None:
        self.connect:Connection=connect
    
    def load(self):
        """
        Metoda sloužící k načtení uživatele
        """
        location,building=get_location(self.connect.databaze,self.connect.player)
        self.connect.send("úspěšné přihlášení",next_message=Next_message.PRIJMI)
        if location=="Hlavní město":
            if building == "hospoda":
                Capital_city_tawern(self.connect).loop()
            place=Capital_city(self.connect)
            place.loop()
        elif location=="Route1":
            Route1(self.connect).loop()
        elif location=="Les":
            Forest(self.connect).loop() 
        elif location=="Route2":
            Route2(self.connect).loop()
        elif location=="Rubínové město":
            Gem_town(self.connect).loop()
        else:
            raise NotImplementedError('Load')