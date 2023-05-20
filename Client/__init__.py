import socket
import threading
import pwinput as pin
import sys
import re
from typing import List,Tuple,Dict,Union
import json
import time

class Client:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, ip_address:str='localhost', port:int=5000, response_size:int=4096,time_delay:float=1.0):
        if not hasattr(self, 'client_socket'):
            self.client_socket:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip_address, port))
            self.response_size:int = response_size
            self.prompt:Union[str,None] = None
            self.recieved:List[Dict[str,str]]=[]
            self.next_move:str="prijmi"
            self.expect_control:bool=False
            self.time_delay:float=time_delay
            
    def __split_and_proccess_data(self,raw_data:str)->str:
        regex:str = r"@\|start\|@([^@]+)?@@([^@]+)?@@([^@]+)@@([^@]+)@\|end\|@"
        matches:List[Tuple[str]] = re.findall(regex, raw_data)
        for protocol_data in matches:
            data:Dict[str,str]=self.__processed_data(protocol_data)
            self.recieved.append(data)
            
    def __processed_data(self,protocol_data:Tuple[str,str,str,str])->Dict[str,str]:
        if not len(protocol_data)==4:
            raise ValueError("Protokol nemá správný počet dat")
        return {
            "prompt":protocol_data[0],
            "value":protocol_data[1],
            "next_message":protocol_data[2],
            "type":protocol_data[3]
        }
        
    def control_kill_client(self):
        while True:
            if "kill_client" in [element.get("value") for element in self.recieved]:
                self.close_client()
    
    def thread_recieve(self):
        while True:
            server_message:str=self.recieve()
            self.__split_and_proccess_data(server_message)
            
    def recieve(self)->str:
        return self.client_socket.recv(self.response_size).decode()
    
    def send(self,value:str)->None:
        self.client_socket.send(value.encode())
    
    def __process_recieve(self,protocol:Dict[str,str]):
        self.next_move=protocol.get("next_message","prijmi")
        if self.next_move == "prijmi":
            if protocol.get("value","")=="":
                return
            if protocol.get("value","kill_client")=="kill_client":
                self.close_client()
            if self.expect_control:
                if protocol.get("value",None)=="|||doruceno|||":
                    self.expect_control:bool=True
                    return
            print(protocol.get("value"))            
        elif self.next_move == "posli":
            send_data:str=""
            while send_data=="":
                if protocol.get("type","text")=="text":
                    send_data:str = input(self.prompt)
                elif protocol.get("type","text")=="heslo":
                    send_data:str = pin.pwinput(self.prompt,'*')
            self.send(send_data)
            self.expect_control:bool=True
        
    def run(self):
        while True:
            if not len(self.recieved)==0:
                protocol:Dict[str,str] = self.recieved.pop(0)
                self.prompt=protocol.get("prompt",">")
                self.__process_recieve(protocol)
                time.sleep(self.time_delay)
     
    def close_client(self):
        print("Aplikace byla uzavřena")
        sys.exit()
                        
if __name__=="__main__":
    with open("konfig/client.json", 'r') as file:
        data:Dict[str,int] = json.load(file)
    if not "server_address" in data.keys():
        input("V konfiguračním souboru není adresa serveru")
        sys.exit()
    if not "server_port" in data.keys():
        input("V konfiguračním souboru není port serveru")
        sys.exit()
    if not "response_size" in data.keys():
        input("V konfiguračním souboru není velikost odpovědi")
        sys.exit()
    if not "time_delay" in data.keys():
        input("V konfiguračním souboru není pauza po zpracování protokolu")
    if not type(data.get("server_address"))==str:
        input("Adresa serveru musí být řetězec")
        sys.exit()
    if not type(data.get("server_port"))==int:
        input("Port serveru musí být celé číslo")
        sys.exit()
    if not type(data.get("response_size"))==int:
        input("Velikost odpovědi musí být celé číslo")
        sys.exit()
    if not type(data.get("time_delay"))==float:
        input("Pauza po zpracování protokolu musí být typu float")
        sys.exit()
        
    try:
        #client=Client(ip_address='dev.spsejecna.net',port=20148)
        client=Client(ip_address=data.get("server_address"),port=data.get("server_port"),response_size=data.get("response_size"),time_delay=data.get("time_delay"))
        recieve_thread=threading.Thread(target=client.thread_recieve,args=())
        recieve_thread.start()
        client.run()
    except ConnectionRefusedError:
        input("Nelze se připojit k serveru")
        sys.exit()
    except KeyboardInterrupt:
        print()
        client.close_client()