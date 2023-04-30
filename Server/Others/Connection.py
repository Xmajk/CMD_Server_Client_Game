import socket
import time
from Enums.Next_message import Next_message
from Database.Database import Database
from Gameobjects.Player import Player

class Connection:
    def __init__(self,address:str,client_socket:socket,database:Database,znakova_sada='UTF-8',number_of_recieve:int=4096) -> None:
        self.ip_adress:str=address
        self.client_socket:socket=client_socket
        self.number_of_recieve:int=number_of_recieve
        self.znakova_sada:str=znakova_sada
        self.databaze:Database=database
        self.player:Player=None
        
        
    def recieve(self,next_message:Next_message,prompt=">",typ="text")->str:
        response=None
        while response==None:
            response = self.client_socket.recv(self.number_of_recieve).decode(self.znakova_sada)
        self.send("|||doruceno|||",next_message=next_message,prompt=prompt,typ=typ)
        return response
    
    def send(self,value:str,next_message:Next_message,prompt=">",typ="text")->None:
        message=f'{prompt}@@{value}@@{next_message}@@{typ}'
        self.client_socket.sendall(message.encode(self.znakova_sada))
        
    def login(self,username:str,password:str)->bool:
        db_password_tuple:tuple|None=self.databaze.get_password(username)
        if db_password_tuple==None:
            return False
        db_player_id,db_password=db_password_tuple
        if db_password==password:
            self.player=Player(db_player_id)
            return True
        return False
    
    def load_player(self):
        self.player.load()
        
    def database_get_location(self)->tuple:
        return self.databaze.get_location(self.player)
        
        
if __name__=="__main__":
    pass