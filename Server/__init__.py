import socket
import threading
import time
from Others.Connection import Connection
from Interfaces.First_view import Login_int
from Database.Database import Database
from Enums.Next_message import Next_message

MAX_HOSTS:int=2
clients:list=[]

semaphore:threading.Semaphore = threading.Semaphore(1)

ip_adresa:str="localhost"
port_number:int=5000

# definice funkce pro obsluhu klienta
def handle_client(connection:Connection)->None:
    try:
        with semaphore:
            if len(clients)==MAX_HOSTS:
                connection.send("Server je zaneprázdněn",next_message=Next_message.PRIJMI,prompt="")
                connection.send("kill_client",next_message=Next_message.PRIJMI,prompt="")
                connection.client_socket.close()
                return None
            else:
                clients.append(connection.ip_adress)
        
        Login_int(connection).loop()
        # uzavření spojení s klientem
    except ConnectionResetError:
        print(f'{connection.ip_adress}-uživatel se odpojil')
    except ConnectionAbortedError:
        print(f'{connection.ip_adress}-Sever spadnul nebo se uživatel odpojil')
    finally:
        connection.client_socket.close()
    with semaphore:
        clients.remove(connection.ip_adress)

# definice funkce pro start serveru
def start_server():
    database:Database = Database()   
    database.set_everyone_offline()
    
    # vytvoření nového socketu
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # nastavení parametrů socketu
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    server_socket.bind((ip_adresa, port_number))
    server_socket.listen(MAX_HOSTS) # maximální počet připojených klientů

    # vytvoření nekonečné smyčky pro přijímání připojení od klientů
    while True:
        # přijetí nového spojení od klienta
        client_socket, client_address = server_socket.accept()

        # spuštění nového vlákna pro obsluhu klienta
        client_thread = threading.Thread(target=handle_client, args=(Connection(client_address[0],client_socket,database),))
        client_thread.start()

if __name__=="__main__":
    # spuštění serveru
    start_server()