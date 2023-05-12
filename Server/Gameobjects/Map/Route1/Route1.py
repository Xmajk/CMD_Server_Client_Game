from Others.Connection import Connection
from lib.ICommand import ICommand
from Enums.Next_message import Next_message
from Others.Help_methods import edit_response
from Gameobjects.Map.Place import Place
from Others.Crossing.To_capit_city import to_capital_city

class Route1(Place):
    
    def __init__(self,connect:Connection) -> None:
        self.NPCs:list=[]
        self.nazev:str="Route1"
        self.budovy:list=[]
        self.ways:dict={
            "Hlavní město":to_capital_city
        }
        self.connect:Connection=connect
        self.prompt="Route1>"
        self.commands:dict={
            "cesta":Cesta_command()
        }
        
    def loop(self):
        self.connect.send("",next_message=Next_message.POSLI,prompt=self.prompt)
        while True:
            client_response:str=self.connect.recieve(next_message=Next_message.PRIJMI,prompt=self.prompt)
            client_command,options=edit_response(client_response)
            client_command:ICommand=self.commands.get(client_command,Neznamy_command())
            continue_loop:bool=client_command.execute(self,options)
            if not continue_loop:
                return
            self.connect.send('',next_message=Next_message.POSLI,prompt=self.prompt)
    
class Help_command(ICommand):
    pass

class Neznamy_command(ICommand):
    
    def __init__(self) -> None:
        pass
    
    def execute(self,route1:Route1,options:list):
        route1.connect.send("Neznámý příkaz",next_message=Next_message.PRIJMI,prompt=route1.prompt)
        return True
    
class Cesta_command(ICommand):
    def execute(self,route1:Route1,options:list):
        if not len(options) == 1:
            route1.connect.send("Příkaz \"cesta\" má jeden povinný argument",next_message=Next_message.PRIJMI,prompt=route1.prompt)
            return True
        if not options[0] in route1.ways.keys():
            route1.connect.send(f'Cesta \"{options[0]}\" neexistuje',next_message=Next_message.PRIJMI,prompt=route1.prompt)
            return True
        route1.ways[options[0]](route1.connect)
        