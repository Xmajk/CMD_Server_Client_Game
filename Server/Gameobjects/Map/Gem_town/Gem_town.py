from Others.Connection import Connection
from Gameobjects.Map.Place import Place
from Others.Crossing import to_route2

class Gem_town(Place):
    def __init__(self,connect:Connection) -> None:
        super().__init__(
            name="Rubínové město",
            prompt="Rubínové_město>",
            connect=connect,
            NPCs=[],
            buildings={},
            ways={
                "Route2":to_route2
            },
            commands={
            }
        )
        
    def loop(self):
        super().loop()