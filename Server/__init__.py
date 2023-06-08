import socket
import threading
from typing import IO,Union,Dict
from Others.Connection import Connection
from Interfaces.First_view import First_view
from Database.Database import Database
from Enums.Next_message import Next_message
import sys
from Database.Actions.Set_status import set_everyone_offline
from cmd import Cmd as konzole
import os
import json

try:
    with open('database.json', 'r') as file:
        database_conf:Dict[str,Union[str,int]] = json.load(file)
except:
    input("Při otevírání souboru \"database.json\" nastala chyba, zkontrolujte jestli existuje a jestli máte všechna práva")
    sys.exit(0)

try:
    with open('server.json', 'r') as file:
        server_conf:Dict[str,Union[str,int]] = json.load(file)
except:
    input("Při otevírání souboru \"server.json\" nastala chyba, zkontrolujte jestli existuje a jestli máte všechna práva")
    sys.exit(0)

MAX_HOSTS:int=server_conf["max_hosts"]
clients:list=[]

semaphore:threading.Semaphore = threading.Semaphore(1)

ip_adresa:str=server_conf["ip_adress"]
port_number:int=server_conf["port"]

def handle_client(connection:Connection)->None:
    """
    Funkce pro obsluhu konkrétního klienta.

    Parametry:
    ----------
    connection: Connection 
        Instance třídy Connection, která reprezentuje spojení s klientem.
    """
    try:
        with semaphore:
            if len(clients)==MAX_HOSTS:
                connection.send("Server je zaneprázdněn",next_message=Next_message.PRIJMI,prompt="")
                connection.send("kill_client",next_message=Next_message.PRIJMI,prompt="")
                connection.client_socket.close()
                return None
            else:
                clients.append(connection.ip_adress)
                connection.set_ip_list(clients)
        interface:First_view=First_view(connection)
        interface.loop()
    except NotImplementedError as e:
        connection.close_connection()
        raise NotImplementedError(e)
    except ConnectionResetError:
        pass#uživatel se odpojil
    except ConnectionAbortedError:
        print(f'{connection.ip_adress}-Sever spadnul')
    except BaseException as be:
        print(be)
    finally:
        connection.close_connection()
    with semaphore:
        try:
            clients.remove(connection.ip_adress)
        except:
            pass

# definice funkce pro start serveru
def start_server()->None:
    """
    Spustí server pro síťovou aplikaci a čeká na připojení klientů.
    """
    try:
        database:Database = Database(database_conf["host"],database_conf["user"],database_conf["password"],database_conf["database"],database_conf["auth_plugin"])
    except:
        input("Při připojování na databázi nastala chyba")
        sys.exit(0)
    set_everyone_offline(database)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    server_socket.bind((ip_adresa, port_number))
    server_socket.listen(MAX_HOSTS)
    
    while True:
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(target=handle_client, args=(Connection(client_address[0],client_socket,database),))
        client_thread.start()

if __name__=="__main__":
    try:
        start_server()
    except socket.error as error:
        if error.errno == 10048:
            input("Protokol, síťová adresa a portu socketu jsou obsazeny")
            sys.exit()