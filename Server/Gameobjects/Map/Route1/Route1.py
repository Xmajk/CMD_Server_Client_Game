from Others.Connection import Connection
from lib.ICommand import ICommand
from Enums.Next_message import Next_message
from Others.Help_methods import edit_response
from Gameobjects.Map.Place import Place
from Others.Crossing import to_capital_city

class Route1(Place):
    
    def __init__(self,connect:Connection) -> None:
        super().__init__(
            name="Route1",
            prompt="Route1>",
            connect=connect,
            NPCs=[],
            buildings=[],
            ways={
                "Hlavní město":to_capital_city
            },
            commands={
            }
        )
        
    def loop(self):
        super().loop()