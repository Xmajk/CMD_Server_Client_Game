from Others.Connection import Connection
from Gameobjects.Map.Place import Place
from Others.Crossing import to_route1,to_gem_town
from Database.Actions.Ability_CRUD import get_ability
from Database.Actions.Inventory_db import get_item
from Gameobjects.Item import Item
from Enums.Next_message import Next_message

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
        if not "A001" in [x.code for x in self.connect.player.abilities] and not "0014" in [x.code for x in self.connect.player.inventory]:
            self.connect.send("Našel jsi na zemi svitek s kouzlem, máš ho v inventáři",next_message=Next_message.PRIJMI,prompt=self.prompt)
            self.connect.player.inventory.append(Item(get_item(self.connect.databaze,"0014")+(0,)))
        super().loop()