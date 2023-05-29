from lib.ICommand import ICommand
from Others.Connection import Connection
from Enums.Next_message import Next_message
from Database.Actions.Authentication import username_exists
from Others.Help_methods import edit_response
from Database.Actions.Registration import get_info_classes,get_info_class,register
import mysql.connector
from Interfaces.Profil.Profile import Profil_view
from typing import Dict
from Interfaces.CMD_level import CMD_level

class Register_view(CMD_level):
    """
    CMD level, který slouží k registraci uživatele
    
    Atributy
    --------
    connect : Connection
        Instance třídy Connection, která reprezentuje spojení s klientem.
    prompt : str
        Prompt CMD levelu.
    commands : Dict[str,ICommand]
        Příkazy, které se budou spouštět.
    trida : str|None
        Třída, kterou si uživatel vybere.
    username : str|None
        Uživatelské jméno, které si uživatel vybere.
    password : str|None
        Heslo, které si uživatel vybere.
    """
    
    def __init__(self,connect:Connection) -> None:
        super().__init__(connect=connect,
                         prompt="registrace>",
                         commands={
                            "help":Help_command(),
                            "back":Exit_command(),
                            "info":Info_command(),
                            "select":Select_command(),
                            "show_all":Show_all_command(),
                            "finish":Finich_command()
                        })
        self.trida:str=None
        self.username:str=None
        self.password:str=None
        
    def loop(self):
        """
        Loop, který slouží jako interface.
        """
        self.connect.send("",next_message=Next_message.POSLI,prompt="Username:")
        self.username:str=self.connect.recieve(next_message=Next_message.PRIJMI)
        if username_exists(self.connect.databaze,self.username):
            self.connect.send(f'Uživatelské jméno \"{self.username}\" už existuje',next_message=Next_message.PRIJMI)
            return
        if len(self.username)>240:
            self.connect.send(f'Uživatelské jméno nesmí mít více jak 240 znaků',next_message=Next_message.PRIJMI)
            return
        self.connect.send("",next_message=Next_message.POSLI,prompt="Heslo:",typ="heslo")
        self.password:str=self.connect.recieve(next_message=Next_message.PRIJMI)
        if len(self.password)>240:
            self.connect.send(f'Heslo nesmí mít více jak 240 znaků',next_message=Next_message.PRIJMI)
            return
        valid,error=valid_password(self.password)
        if not valid:
            self.connect.send(error,next_message=Next_message.PRIJMI)
            return
        self.connect.send("",next_message=Next_message.POSLI,prompt="Opakujte heslo:",typ="heslo")
        password_sc:str=self.connect.recieve(next_message=Next_message.PRIJMI)
        if not self.password==password_sc:
            self.connect.send(f'Hesla se neshodují',next_message=Next_message.PRIJMI)
            return
        self.connect.send("Nyní dokončete registraci",next_message=Next_message.POSLI,prompt=self.prompt)
        while True:
            client_response:str=self.connect.recieve(next_message=Next_message.PRIJMI)
            client_command,options=edit_response(client_response)
            client_command:ICommand=self.commands.get(client_command,Neznamy_command())
            continue_loop:bool=client_command.execute(self,options)
            if not continue_loop:
                return
            self.connect.send("",next_message=Next_message.POSLI,prompt=self.prompt)
            
def valid_password(password:str)->tuple:
    """
    Metoda, která zjišťuje jestli je heslo validní.
    
    Parametry
    ---------
    password : str
        Heslo zadané uživatelem.
    
    Returns
    -------
    tuple[bool,str]
        Tuple o dvou elementech, první je jestli je heslo validní a druhý je chyba pokud není validní
    """
    return (True,"")

class Exit_command(ICommand):
    """
    ICommand příkazu opuštění registrace.
    """
    
    def __init__(self) -> None:
        pass
    
    def execute(self,rv:Register_view,options:list)->bool:
        if not len(options)==0:
            rv.connect.send("Příkaz \"back\" nemá žádné argumenty",next_message=Next_message.PRIJMI)
            return True
        return False

class Help_command(ICommand):
    """
    ICommand příkazu, který vypíše všechny dostupné příkazy.
    """
    
    def __init__(self) -> None:
        pass
    
    def execute(self,rv:Register_view,options:list)->bool:
        if not len(options)==0:
            rv.connect.send("Příkaz \"help\" nemá žádné argumenty",next_message=Next_message.PRIJMI)
            return True
        rv.connect.send("",next_message=Next_message.PRIJMI)
        rv.connect.send("----------------------",next_message=Next_message.PRIJMI)
        rv.connect.send("-show_all=>vypíšou se všechny třídy, které si můžete vybrat",next_message=Next_message.PRIJMI)
        rv.connect.send("-info --[název třídy]=>vypíšou se informace o třídě",next_message=Next_message.PRIJMI)
        rv.connect.send("-select --[název třídy]=>vyberete si třídu",next_message=Next_message.PRIJMI)
        rv.connect.send("-finish=>ukončíte registraci",next_message=Next_message.PRIJMI)
        rv.connect.send("-back=>odejdete z registrace",next_message=Next_message.PRIJMI)
        rv.connect.send("-help=>vypíšou se všechny příkazy, které můžete aktuálně použít",next_message=Next_message.PRIJMI)
        rv.connect.send("----------------------",next_message=Next_message.PRIJMI)
        rv.connect.send("",next_message=Next_message.PRIJMI)
        return True
    
class Show_all_command(ICommand):
    """
    ICommand příkazu, který zobrazí všechny dostupné třídy.
    """
    
    def __init__(self) -> None:
        pass
        
    def execute(self,rv:Register_view,options:list)->bool:
        if not len(options)==0:
            rv.connect.send("Příkaz \"show_all\" nemá žádné argumenty",next_message=Next_message.PRIJMI)
            return True
        rv.connect.send("",next_message=Next_message.PRIJMI)
        rv.connect.send("----------------------",next_message=Next_message.PRIJMI)
        for nazev,info in get_info_classes(rv.connect.databaze):
            rv.connect.send(f'{nazev}: {info}',next_message=Next_message.PRIJMI)
        rv.connect.send("----------------------",next_message=Next_message.PRIJMI)
        rv.connect.send("",next_message=Next_message.PRIJMI)
        return True
    
class Info_command(ICommand):
    """
    ICommand příkazu, který zobrazuje informace o zadané třídě.
    """
    
    def __init__(self) -> None:
        pass
        
    def execute(self,rv:Register_view,options:list)->bool:
        if not len(options)==1:
            rv.connect.send("Příkaz \"info\" má pouze jeden argument [název třídy]",next_message=Next_message.PRIJMI)
            return True
        if not options[0] in [nazev for nazev,info in get_info_classes(rv.connect.databaze)]:
            rv.connect.send(f'Název třídy \"{options[0]}\" neexistuje',next_message=Next_message.PRIJMI)
            return True
        nazev,hp,atk,speed,mana,info = get_info_class(rv.connect.databaze,options[0])
        rv.connect.send("",next_message=Next_message.PRIJMI)
        rv.connect.send("----------------------",next_message=Next_message.PRIJMI)
        rv.connect.send(f'název:{nazev}',next_message=Next_message.PRIJMI)
        rv.connect.send(f'životy:{hp}',next_message=Next_message.PRIJMI)
        rv.connect.send(f'útok:{atk}',next_message=Next_message.PRIJMI)
        rv.connect.send(f'rychlost:{speed}',next_message=Next_message.PRIJMI)
        rv.connect.send(f'mana:{mana}',next_message=Next_message.PRIJMI)
        rv.connect.send(f'informace:{info}',next_message=Next_message.PRIJMI)
        rv.connect.send("----------------------",next_message=Next_message.PRIJMI)
        rv.connect.send("",next_message=Next_message.PRIJMI)
        return True
    
class Select_command(ICommand):
    """
    ICommand příkazu, kterým uživatel vybere třídu.
    """
    
    def __init__(self) -> None:
        pass
        
    def execute(self,rv:Register_view,options:list)->bool:
        if not len(options)==1:
            rv.connect.send("Příkaz \"select\" má pouze jeden argument [název třídy]",next_message=Next_message.PRIJMI)
            return True
        if not options[0] in [nazev for nazev,info in get_info_classes(rv.connect.databaze)]:
            rv.connect.send(f'Název třídy \"{options[0]}\" neexistuje',next_message=Next_message.PRIJMI)
            return True
        rv.connect.send(f'Vybrali jste si třídu \"{options[0]}\"',next_message=Next_message.PRIJMI)
        rv.trida=options[0]
        return True
    
class Finich_command(ICommand):
    """
    ICommand příkazu, který potvrdí registraci
    """
    
    def __init__(self) -> None:
        pass
        
    def execute(self,rv:Register_view,options:list)->bool:
        if not len(options)==0:
            rv.connect.send("Příkaz \"finish\" nemá žádné argumenty",next_message=Next_message.PRIJMI)
            return True        
        if rv.trida==None:
            rv.connect.send("Musíte si vybrat třídu",next_message=Next_message.PRIJMI)
            return True
        try:
            rv.connect.send("Prosím vyčkejte než vás zaregistrujeme",next_message=Next_message.PRIJMI)
            register(rv.connect.databaze,rv.username,rv.trida,rv.password)
        except mysql.connector.Error as error:
            print(error.sqlstate)
            if error.sqlstate=="45000":
                rv.connect.send(f'Během vaší registrace si username \"{rv.username}\" někdo zaregistroval',next_message=Next_message.PRIJMI)
                return False
            rv.connect.send("Při registraci nastala chyba",next_message=Next_message.PRIJMI)
            return False
        except Exception as e:
            print(e)
            rv.connect.send("Při registraci nastala chyba",next_message=Next_message.PRIJMI)
            return False
        rv.connect.send(f'Úspěšně jste se zaregistroval \"{rv.username}\"',next_message=Next_message.PRIJMI)
        return False
    
class Neznamy_command(ICommand):
    """
    ICommand příkazu, který vypíše pokud je příkaz neznámý.
    """

    def __init__(self) -> None:
        pass
        
    def execute(self,rv:Register_view,options:list)->bool:
        rv.connect.send("Neznánmý příkaz",next_message=Next_message.PRIJMI,prompt=rv.prompt)
        return True

