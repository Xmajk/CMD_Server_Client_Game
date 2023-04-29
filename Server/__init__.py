import socket
import threading
import time
from Others.Connection import Connection
from Interfaces.First_view import Login_int
from Database.Database import Database

MAX_HOSTS:int=25


ip_adresa:str="localhost"
port_number:int=5000

# definice funkce pro obsluhu klienta
def handle_client(connection:Connection):
    try:
        Login_int(connection).loop()
        # uzavření spojení s klientem
    except (ConnectionResetError, ConnectionAbortedError):
        print(f'{connection.ip_adress}-Sever spadnul nebo se uživatel odpojil')
    finally:
        connection.client_socket.close()

# definice funkce pro start serveru
def start_server():
    database:Database = Database()
    
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