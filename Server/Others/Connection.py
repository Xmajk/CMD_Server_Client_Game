import socket
import time
from Enums.Next_message import Next_message

class Connection:
    def __init__(self,address:str,client_socket:socket,znakova_sada='UTF-8',number_of_recieve:int=4096) -> None:
        self.ip_adress:str=address
        self.client_socket:socket=client_socket
        self.number_of_recieve:int=number_of_recieve
        self.znakova_sada:str=znakova_sada
        
    def recieve(self,next_message:Next_message)->str:
        response=None
        while response==None:
            response = self.client_socket.recv(self.number_of_recieve).decode(self.znakova_sada)
        print(response)
        self.send("|||doruceno|||",next_message=next_message)
        return response
    
    def send(self,value:str,next_message:Next_message,prompt=">")->None:
        message=f'{prompt}@@{value}@@{next_message}'
        self.client_socket.sendall(message.encode(self.znakova_sada))