from Others.Connection import Connection
from typing import List,Dict,Callable
from lib.ICommand import ICommand
from Gameobjects.NPC import NPC
from Enums.Next_message import Next_message
from Others.Help_methods import edit_response

class Place:
    
    def __init__(self,name:str,prompt:str,connect:Connection,
                 NPCs:List[NPC],buildings:list,ways:Dict[str,Callable],
                 commands:Dict[str,Callable]) -> None:
        self.name:str=name
        self.prompt:str=prompt
        self.connect:Connection=connect
        self.NPCs:List[NPC]=NPCs
        self.buildings:list=buildings
        self.ways:Dict[str,Callable]=ways
        self.commands:Dict[str,Callable]=commands
    
    def loop(self):
        self.connect.send("",next_message=Next_message.POSLI,prompt=self.prompt)
        while True:
            client_response:str=self.connect.recieve(next_message=Next_message.PRIJMI,prompt=self.prompt)
            client_command,options=edit_response(client_response)
            client_command:ICommand=self.commands.get(client_command,Unknown_command())
            continue_loop:bool=client_command.execute(self,options)
            if not continue_loop:
                return
            self.connect.send('',next_message=Next_message.POSLI,prompt=self.prompt)
            
class Unknown_command(ICommand):
    
    def __init__(self) -> None:
        pass
    
    def execute(self,place:Place,options:list):
        place.connect.send("Neznámý příkaz",next_message=Next_message.PRIJMI,prompt=place.prompt)
        return True