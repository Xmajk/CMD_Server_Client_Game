from Others.Connection import Connection
from Database.Actions.Quests import capital_city_tawern
from Database.Actions.Set_quests import set_capital_city_tawern
from Gameobjects.Map.Place import Place
from Others.Crossing import to_route1
from Enums.Next_message import Next_message
from NPC_battle.NPC_battle import NPC_battle
from NPC_battle.Battle_NPC import Battle_NPC

class Forest(Place):

    def __init__(self,connect:Connection) -> None:
        super().__init__(
            name="Les",
            prompt="Les>",
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
        if not capital_city_tawern(self.connect.databaze,self.connect.player.username):
            battle:NPC_battle=NPC_battle(self.connect,self.prompt,Battle_NPC("bandita",300,30,35))
            battle.loop()
            set_capital_city_tawern(self.connect.databaze,self.connect.player.username)
            self.connect.send("Zachránil jste hospodského a splnili jste úkol!",next_message=Next_message.PRIJMI,prompt=self.prompt)
        super().loop()