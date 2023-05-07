from lib.ICommand import ICommand
from Others.Connection import Connection
from Enums.Next_message import Next_message
from Database.Actions.Authentication import username_exists
from Others.Help_methods import edit_response
from Database.Actions.Registration import get_info_classes,get_info_class,register

class Register_view:
    
    def __init__(self,connect:Connection) -> None:
        self.connect:Connection=connect
        self.prompt:str="registrace>"
        self.commands:dict={
            "help":Help_command,
            "exit":Exit_command,
            "info":Info_command,
            "select":Select_command,
            "show_all":Show_all_command,
            "finish":Finich_command
        }
        self.trida:str=None
        self.username:str=None
        self.password:str=None
        
    def loop(self):
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
            client_command:ICommand|None=self.commands.get(client_command,None)
            if not client_command==None:
                continue_loop:bool=client_command(self.connect,options,self).execute()
                if not continue_loop:
                    return
            else:
                self.connect.send("Neznámý příkaz",next_message=Next_message.PRIJMI,prompt=self.prompt)
            self.connect.send("",next_message=Next_message.POSLI,prompt=self.prompt)
            
def valid_password(password:str)->tuple:
    return (True,"")

class Exit_command(ICommand):
    def __init__(self,connect:Connection,options:list,rv:Register_view) -> None:
        self.connect:Connection=connect
        self.options:list=options
    
    def execute(self)->bool:
        if not len(self.options)==0:
            self.connect.send("Příkaz \"exit\" nemá žádné argumenty",next_message=Next_message.PRIJMI)
            return True
        return False

class Help_command(ICommand):
    
    def __init__(self,connect:Connection,options:list,rv:Register_view) -> None:
        self.connect:Connection=connect
        self.options:list=options
    
    def execute(self)->bool:
        if not len(self.options)==0:
            self.connect.send("Příkaz \"help\" nemá žádné argumenty",next_message=Next_message.PRIJMI)
            return True
        self.connect.send("",next_message=Next_message.PRIJMI)
        self.connect.send("----------------------",next_message=Next_message.PRIJMI)
        self.connect.send("-show_all=>vypíšou se všechny třídy, které si můžete vybrat",next_message=Next_message.PRIJMI)
        self.connect.send("-info --[název třídy]=>vypíšou se informace o třídě",next_message=Next_message.PRIJMI)
        self.connect.send("-select --[název třídy]=>vyberete si třídu",next_message=Next_message.PRIJMI)
        self.connect.send("-finish=>ukončíte registraci",next_message=Next_message.PRIJMI)
        self.connect.send("-exit=>odejdete z registrace",next_message=Next_message.PRIJMI)
        self.connect.send("-help=>vypíšou se všechny příkazy, které můžete aktuálně použít",next_message=Next_message.PRIJMI)
        self.connect.send("----------------------",next_message=Next_message.PRIJMI)
        self.connect.send("",next_message=Next_message.PRIJMI)
        return True
    
class Show_all_command(ICommand):
    
    def __init__(self,connect:Connection,options:list,rv:Register_view) -> None:
        self.connect:Connection=connect
        self.options:list=options
        
    def execute(self)->bool:
        if not len(self.options)==0:
            self.connect.send("Příkaz \"show_all\" nemá žádné argumenty",next_message=Next_message.PRIJMI)
            return True
        self.connect.send("",next_message=Next_message.PRIJMI)
        self.connect.send("----------------------",next_message=Next_message.PRIJMI)
        for nazev,info in get_info_classes(self.connect.databaze):
            self.connect.send(f'{nazev}: {info}',next_message=Next_message.PRIJMI)
        self.connect.send("----------------------",next_message=Next_message.PRIJMI)
        self.connect.send("",next_message=Next_message.PRIJMI)
        return True
    
class Info_command(ICommand):
    
    def __init__(self,connect:Connection,options:list,rv:Register_view) -> None:
        self.connect:Connection=connect
        self.options:list=options
        
    def execute(self)->bool:
        if not len(self.options)==1:
            self.connect.send("Příkaz \"info\" má pouze jeden argument [název třídy]",next_message=Next_message.PRIJMI)
            return True
        if not self.options[0] in [nazev for nazev,info in get_info_classes(self.connect.databaze)]:
            self.connect.send(f'Název třídy \"{self.options[0]}\" neexistuje',next_message=Next_message.PRIJMI)
            return True
        nazev,hp,atk,speed,mana,info = get_info_class(self.connect.databaze,self.options[0])
        self.connect.send("",next_message=Next_message.PRIJMI)
        self.connect.send("----------------------",next_message=Next_message.PRIJMI)
        self.connect.send(f'název:{nazev}',next_message=Next_message.PRIJMI)
        self.connect.send(f'životy:{hp}',next_message=Next_message.PRIJMI)
        self.connect.send(f'útok:{atk}',next_message=Next_message.PRIJMI)
        self.connect.send(f'rychlost:{speed}',next_message=Next_message.PRIJMI)
        self.connect.send(f'mana:{mana}',next_message=Next_message.PRIJMI)
        self.connect.send(f'informace:{info}',next_message=Next_message.PRIJMI)
        self.connect.send("----------------------",next_message=Next_message.PRIJMI)
        self.connect.send("",next_message=Next_message.PRIJMI)
        return True
    
class Select_command(ICommand):
    
    def __init__(self,connect:Connection,options:list,rv:Register_view) -> None:
        self.connect:Connection=connect
        self.options:list=options
        self.rv:Register_view=rv
        
    def execute(self)->bool:
        if not len(self.options)==1:
            self.connect.send("Příkaz \"select\" má pouze jeden argument [název třídy]",next_message=Next_message.PRIJMI)
            return True
        if not self.options[0] in [nazev for nazev,info in get_info_classes(self.connect.databaze)]:
            self.connect.send(f'Název třídy \"{self.options[0]}\" neexistuje',next_message=Next_message.PRIJMI)
            return True
        self.connect.send(f'Vybrali jste si třídu \"{self.options[0]}\"',next_message=Next_message.PRIJMI)
        self.rv.trida=self.options[0]
        return True
    
class Finich_command(ICommand):
    
    def __init__(self,connect:Connection,options:list,rv:Register_view) -> None:
        self.connect:Connection=connect
        self.options:list=options
        self.rv:Register_view=rv
        
    def execute(self)->bool:
        if not len(self.options)==0:
            self.connect.send("Příkaz \"finish\" nemá žádné argumenty",next_message=Next_message.PRIJMI)
            return True
        if self.rv.trida==None:
            self.connect.send("Musíte si vybrat třídu",next_message=Next_message.PRIJMI)
            return True
        try:
            register(self.connect.databaze,self.rv.username,self.rv.trida,self.rv.password)
        except:
            self.connect.send("Při registraci nastala chyba",next_message=Next_message.PRIJMI)
            return False
        self.connect.send(f'Úspěšně jste se zaregistroval \"{self.rv.username}\"',next_message=Next_message.PRIJMI)
        return False