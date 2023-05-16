from Others.Connection import Connection
from typing import Dict, List
from lib.ICommand import ICommand
from Gameobjects.Building import Building

class Capital_city_tawern(Building):
    
    def __init__(self, connect: Connection) -> None:
        super().__init__(connect, 
                         "Hlavní město>",
                         commands={
                             
                        }, 
                        name="hospoda", 
                        NPCs=[
                            
                        ])

    def loop(self) -> None:
        super().loop()