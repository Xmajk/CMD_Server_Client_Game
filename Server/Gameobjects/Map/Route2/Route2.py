from Others.Connection import Connection
from Gameobjects.Map.Place import Place
from Others.Crossing import to_route1,to_gem_town

class Route2(Place):
    def __init__(self,connect:Connection) -> None:
        super().__init__(
            name="Route2",
            prompt="Route2>",
            connect=connect,
            NPCs=[],
            buildings={},
            ways={
                "Rubínové město":to_gem_town,
                "Route1":to_route1
            },
            commands={
            }
        )
        
    def loop(self):
        super().loop()