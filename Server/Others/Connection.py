import socket
import time
from Enums.Next_message import Next_message
from Database.Database import Database
from Gameobjects.Player import Player
import sys
import threading
from Database.Actions.Set_status import set_online

semaphore:threading.Semaphore = threading.Semaphore(1)

class Connection:
    def __init__(self,address:str,client_socket:socket,database:Database,znakova_sada='UTF-8',number_of_recieve:int=4096,time_delay:float=0.001) -> None:
        self.ip_adress:str=address
        self.client_socket:socket=client_socket
        self.number_of_recieve:int=number_of_recieve
        self.znakova_sada:str=znakova_sada
        self.databaze:Database=database
        self.player:Player=None
        self.time_delay:int=time_delay
        self.__all_ip_list:list=None
        
    def set_ip_list(self,arr:list)->None:
        self.__all_ip_list=arr
                
    def recieve(self,next_message:Next_message,prompt=">",typ="text")->str:
        response:str=None
        while response==None:
            response = self.client_socket.recv(self.number_of_recieve).decode(self.znakova_sada)
        self.send("|||doruceno|||",next_message=next_message,prompt=prompt,typ=typ)
        response=response.strip()
        return response
    
    def send(self,value:str,next_message:Next_message,prompt=">",typ="text")->None:
        message=f'{prompt}@@{value}@@{next_message}@@{typ}'
        self.client_socket.sendall(message.encode(self.znakova_sada))
        time.sleep(self.time_delay)
    
    def load_player(self):
        self.player.load()
        
    def database_get_location(self)->tuple:
        return self.databaze.get_location(self.player)
    
    def close_connection(self)->None:
        with semaphore:
            self.send("kill_client",next_message=Next_message.PRIJMI,prompt="")
            if not self.player==None:
                set_online(self.databaze,self.player.username,0)
            self.__all_ip_list.remove(self.ip_adress)
            self.client_socket.close()
            sys.exit(0)
        
        
if __name__=="__main__":
    pass