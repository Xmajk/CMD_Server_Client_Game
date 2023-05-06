from Others.Connection import Connection
from Enums.Next_message import Next_message
import time
from lib.ICommand import ICommand

class Capital_city:
    """
        Označení v databázi jako 1
    """    
    def __init__(self,connect:Connection) -> None:
        self.NPCs:list=[]
        self.nazev:str="Hlavní město"
        self.budovy:list=[]
        self.connect:Connection=connect
        self.promtp="Hlavní město>"
        
    def loop(self)->None:
        while True:
            client_response:str=self.connect.recieve(next_message=Next_message.PRIJMI,prompt=self.promtp)
            client_response:str=client_response.strip()
            if client_response=="help":
                self.do_help()
            elif client_response=="profil":
                raise NotImplementedError()
            elif client_response=="postavy":
                self.do_postavy()
            elif client_response=="budovy":
                raise NotImplementedError()
            elif client_response=="cesty":
                raise NotImplementedError()
            else:
                self.connect.send("Neznámý příkaz",next_message=Next_message.PRIJMI,prompt=self.promtp)
            self.connect.send('',next_message=Next_message.POSLI,prompt=self.promtp)
    
    def do_help(self)->None:
        raise NotImplementedError("hlavni mesto, help")
    
    def do_postavy(self)->None:
        self.connect.send('----------------------',next_message=Next_message.PRIJMI,prompt=self.promtp)
        self.connect.send('Hráči',next_message=Next_message.PRIJMI,prompt=self.promtp)
        for i in self.connect.databaze.get_all_online_players_of_locaiotn(self.connect.player):
            self.connect.send(i,next_message=Next_message.PRIJMI,prompt=self.promtp)
        self.connect.send(' ',next_message=Next_message.PRIJMI,prompt=self.promtp)
        self.connect.send('NPCs',next_message=Next_message.PRIJMI,prompt=self.promtp)
        self.connect.send('----------------------',next_message=Next_message.PRIJMI,prompt=self.promtp)
        
