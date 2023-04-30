from Others.Connection import Connection
from Enums.Next_message import Next_message

class Capital_city:
    """
        Označení v databázi jako null nebo 1
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
            print(client_response)
            self.connect.send('',next_message=Next_message.POSLI,prompt=self.promtp)