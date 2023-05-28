from Others.Connection import Connection
from typing import Dict, List
from lib.ICommand import ICommand
from Gameobjects.Building import Building
from Gameobjects.NPCs.Bartender import Bartender 

class Capital_city_tawern(Building):
    
    def __init__(self, connect: Connection) -> None:
        super().__init__(connect, 
                         prompt="Hlavní město>",
                         commands={
                             
                        }, 
                        name="hospoda", 
                        NPCs={
                            "hospodsky":Bartender(connect,f'Hlavní město>hospoda>')
                        }
                        )

    def loop(self) -> None:
        super().loop()