import socket
import threading
import time
import pwinput as pin
from lib import hashing
import sys

class Client:
    
    def __init__(self,ip_address='localhost',port=5000,response_size=4096) -> None:
        self.client_socket:socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip_address,port))
        self.response_size:int=response_size
        self.prompt:str=None
        
    def __processed_data(self,raw_data:str)->dict:
        output:list=raw_data.split("@@")
        output:dict={
            "prompt":output[0],
            "text":output[1],
            "next_message":output[2],
            "typ":output[3]
        }
        self.prompt=output.get("prompt")
        return output
        
    def run(self):
        try:
            recieve_data:str = self.client_socket.recv(self.response_size).decode()
            print(self.__processed_data(recieve_data).get("text"))
            while True:
                if self.__processed_data(recieve_data).get("next_message")=="posli":
                    if self.__processed_data(recieve_data).get("typ")=="text":
                        send_data:str = input(self.prompt)
                    elif self.__processed_data(recieve_data).get("typ")=="heslo":
                        send_data:str = pin.pwinput(self.prompt,'*')
                    else:
                        raise ValueError("Hodnota typ neplňuje hodnoty")
                    if send_data.strip()=="":
                        continue
                    try:
                        self.client_socket.send(send_data.encode())
                    except socket.error as error:
                        if error.errno == 10054:
                            input("Stávající připojení bylo vynuceně ukončeno vzdáleným hostitelem.")
                            sys.exit()
                    tmp:str=self.client_socket.recv(self.response_size).decode()
                    if self.__processed_data(tmp).get("text")=="|||doruceno|||":
                        recieve_data:str=tmp
                else:
                    recieve_data:str=self.client_socket.recv(self.response_size).decode()
                    if self.__processed_data(recieve_data).get("text")=="kill_client":
                        input("Byl jste odpojen")
                        break
                    if not self.__processed_data(recieve_data).get("text")=="":
                        print(f'{self.__processed_data(recieve_data).get("text")}')
        except Exception as e:
            print(e)

if __name__=="__main__":
    try:
        client=Client()
        client.run()
    except ConnectionRefusedError:
        input("Nelze se připojit k serveru")
        sys.exit()