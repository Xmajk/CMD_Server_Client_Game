from Others.Connection import Connection
from Gameobjects.Map.Place import Place
from Others.Crossing import to_capital_city,to_forest,to_route2

class Route1(Place):
    
    def __init__(self,connect:Connection) -> None:
        super().__init__(
            name="Route1",
            prompt="Route1>",
            connect=connect,
            NPCs=[],
            buildings={},
            ways={
                "Hlavní město":to_capital_city,
                "Les života":to_forest,
                "Route2":to_route2
            },
            commands={
            }
        )
        
    def loop(self):
        super().loop()