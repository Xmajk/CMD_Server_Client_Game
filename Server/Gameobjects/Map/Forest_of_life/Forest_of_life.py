from Others.Connection import Connection
from lib.ICommand import ICommand
from Enums.Next_message import Next_message
from Others.Help_methods import edit_response
from Gameobjects.Map.Place import Place
from Others.Crossing import to_route1

class Forest_of_life(Place):

    def __init__(self,connect:Connection) -> None:
        super().__init__(
            name="Les života",
            prompt="Les_života>",
            connect=connect,
            NPCs=[],
            buildings={},
            ways={
                "Route1":to_route1
            },
            commands={
            }
        )
        
    def loop(self):
        super().loop()