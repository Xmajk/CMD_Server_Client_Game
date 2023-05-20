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
    """
    Třída Connection slouží pro uchování informací o klientovi a komunikaci s ním.
    
    Parametery
    ----------
    
    
    Atributy:
    ---------
    ip_adress: str
        IP adresa klienta.
    client_socket: socket
        Socket klienta pro komunikaci se serverem.
    number_of_recieve: int
        Maximální délka zprávy, kterou klient může přijmout najednou.
    znakova_sada: str
        Použitá znaková sada.
    databaze: Database
        Objekt třídy Database pro práci s databází.
    player: Player
        Objekt třídy Player pro uchování informací o hráči.
    time_delay: int
        Časová prodleva mezi odesláním zpráv.
    __all_ip_list: list
        Seznam IP adres všech připojených klientů.
    """
    def __init__(self,address:str,client_socket:socket,database:Database,znakova_sada='UTF-8',number_of_recieve:int=4096,time_delay:float=0) -> None:
        self.ip_adress:str=address
        self.client_socket:socket=client_socket
        self.number_of_recieve:int=number_of_recieve
        self.znakova_sada:str=znakova_sada
        self.databaze:Database=database
        self.player:Player=Player(None)
        self.time_delay:int=time_delay
        self.__all_ip_list:list=None
        
    def set_ip_list(self,arr:list)->None:
        """
        nastaví vstupní list jako seznam všech ip adress
        
        Parametry:
        ----------
        arr: list
            list ip adres
        """
        self.__all_ip_list=arr
                
    def recieve(self,next_message:Next_message,prompt=">",typ="text")->str:
        """
        Metoda, která přijímá zprávu od klineta, po přijetí zprávy odešle, že zpráva byla doručena.
        
        Parametry:
        ----------
        next_message: Next_message
            Enum, jestli má klient přijímat nebo odesílat.
        prompt: str, defaultně '>'
            Určuje prompt u klienta.
        typ: str, defaultně 'text'
            Určuje jaký typ bude u klinta input.
        """
        response:str=None
        while response==None:
            response = self.client_socket.recv(self.number_of_recieve).decode(self.znakova_sada)
        self.send("|||doruceno|||",next_message=next_message,prompt=prompt,typ=typ)
        response=response.strip()
        return response
    
    def send(self,value:str,next_message:Next_message,prompt=">",typ="text")->None:
        message=f'@|start|@{prompt}@@{value}@@{next_message}@@{typ}@|end|@'
        self.client_socket.sendall(message.encode(self.znakova_sada))
        time.sleep(self.time_delay)
    
    def close_connection(self)->None:
        with semaphore:
            try: self.send("kill_client",next_message=Next_message.PRIJMI,prompt="")
            except:pass
            if not self.player==None:
                set_online(self.databaze,self.player.username,0)
            self.__all_ip_list.remove(self.ip_adress)
            self.client_socket.close()
            sys.exit(0)
        
        
if __name__=="__main__":
    pass