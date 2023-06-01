import socket
import threading
import time
import pwinput as pin
from lib import hashing
import sys

class Client:
    
    def __init__(self,ip_address='localhost',port=5000,response_size=4096) -> None:
        self.client_socket:socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip_address,port))
        self.response_size:int=response_size
        self.prompt:str=None
        
    def __processed_data(self,raw_data:str)->dict:
        output:list=raw_data.split("@@")
        if not len(output)==4:
            print("chybyčka se vloudila")
            print(output)
            time.sleep(1)
            return{
            "prompt":self.prompt,
            "text":"",
            "next_message":"prijmi",
            "typ":"text"
        } 
        output:dict={
            "prompt":output[0],
            "text":output[1],
            "next_message":output[2],
            "typ":output[3]
        }
        self.prompt=output.get("prompt")
        return output
    
    def recieve(self)->str:
        return self.client_socket.recv(self.response_size).decode()
    
    def send(self,value:str)->None:
        self.client_socket.send(value.encode())
        
    def run(self)->None:
        try:
            recieved_data:str=self.recieve()
            recieved_data:dict=self.__processed_data(recieved_data)
            print(recieved_data.get("text"))
            while True:
                if recieved_data.get("next_message")=="posli":
                    if recieved_data.get("typ")=="text":
                        send_data:str = input(self.prompt)
                    elif recieved_data.get("typ")=="heslo":
                        send_data:str = pin.pwinput(self.prompt,'*')
                    else:
                        raise ValueError("Hodnota typ neplňuje hodnoty")
                    if send_data.strip()=="":
                        continue
                    try:
                        self.send(send_data)
                    except socket.error as error:
                        if error.errno == 10054:
                            input("Stávající připojení bylo vynuceně ukončeno vzdáleným hostitelem.")
                            input()
                            Client().run()
                            sys.exit()
                    tmp:str=self.recieve()
                    tmp:dict=self.__processed_data(tmp)
                    if tmp.get("text")=="|||doruceno|||":
                        recieved_data:dict=tmp
                else:
                    recieved_data:dict=self.__processed_data(self.recieve())
                    if recieved_data.get("text")=="kill_client":
                        input("Byl jste odpojen")
                        Client().run()
                        break
                    if not recieved_data.get("text")=="":
                        print(f'{recieved_data.get("text")}')
        except Exception as e:
            input(e)
                
if __name__=="__main__":
    try:
        #client=Client(ip_address='dev.spsejecna.net',port=20148)
        client=Client()
        client.run()
    except ConnectionRefusedError:
        input("Nelze se připojit k serveru")
        sys.exit()