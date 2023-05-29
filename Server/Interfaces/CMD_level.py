from Others.Connection import Connection
from typing import Dict,Callable
from Enums.Next_message import Next_message
from lib.ICommand import ICommand
from Others.Help_methods import edit_response

class CMD_level:
    """
    Třída, která slouží jako základ interfacu.
    
    Atributy
    --------
    connect : Connection
        Instance třídy Connection, která reprezentuje spojení s klientem.
    prompt : str
        Prompt CMD levelu.
    commands : Dict[str,ICommand]
        Příkazy, které se budou spouštět.
    """
    
    def __init__(self,connect:Connection,prompt:str,commands:Dict[str,ICommand]) -> None:
        self.connect:Connection=connect
        self.prompt:str=prompt
        self.commands:Dict[str,ICommand]=commands
        
    def loop(self):
        self.connect.send("",next_message=Next_message.POSLI,prompt=self.prompt)
        while True:
            self.connect.save_player()
            client_response:str=self.connect.recieve(next_message=Next_message.PRIJMI,prompt=self.prompt)
            client_command,options=edit_response(client_response)
            client_command:ICommand=self.commands.get(client_command,Unknown_command(self))
            continue_loop:bool=client_command.execute(options)
            if not continue_loop:
                return
            self.connect.send('',next_message=Next_message.POSLI,prompt=self.prompt)
            
    def supplementary_help(self):
        self.connect.send("-help=>vypíšou se všechny příkazy, které můžete aktuálně použít",next_message=Next_message.PRIJMI,prompt=self.prompt)
            
class Unknown_command(ICommand):
    
    def __init__(self,cmd_level:CMD_level) -> None:
        self.cmd_level:CMD_level=cmd_level
    
    def execute(self,options:list):
        self.cmd_level.connect.send("Neznámý příkaz",next_message=Next_message.PRIJMI,prompt=self.cmd_level.prompt)
        return True

    