import socket
import threading
from Others.Connection import Connection
from Interfaces.First_view import First_view
from Database.Database import Database
from Enums.Next_message import Next_message
import sys
from Database.Actions.Set_status import set_everyone_offline

MAX_HOSTS:int=2
clients:list=[]

semaphore:threading.Semaphore = threading.Semaphore(1)

ip_adresa:str="localhost"
port_number:int=5000

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
        print(f'{connection.ip_adress}-uživatel se odpojil')
    except ConnectionAbortedError:
        print(f'{connection.ip_adress}-Sever spadnul')
    finally:
        connection.client_socket.close()
    with semaphore:
        clients.remove(connection.ip_adress)

# definice funkce pro start serveru
def start_server()->None:
    """
    Spustí server pro síťovou aplikaci a čeká na připojení klientů.
    """
    database:Database = Database()
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