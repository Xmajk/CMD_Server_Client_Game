from typing import List,Union,Tuple
from Gameobjects.Item import Item
from Database.Database import Database

class Player:
    """
    Třída která představuje uživatele.
    
    Atributy
    --------
    username : str
        Přezdívka uživatele.
    current_hp : int
        Aktuální životy.
    trida : str|None
        Třída uživatele.
    base_hp : int
        Základní počet životů.
    base_atk : int
        Základní hodnota útoku.
    base_speed : int
        Základní rychlost.
    base_mana : int
        Základní hodnota many.
    add_hp : int
        Přídavek na životy.
    add_atk : int
        Přídavek na útok.
    add_speed : int
        Přídavek na rychlost.
    add_mana : int
        Přídavek na manu.
    items_hp : int
        Celkový přídavek na životy z předmětů.
    items_atk : int
        Celkový přídavek na útok z předmětů.
    items_speed : int
        Celková přídavek na rychlost z předmětů.
    items_mana : int
        Celkový přídavek na manu z předmětů.
    coins : int
        Počet mincí.
    inventory : List[Item]
        Inventář předmětů.
    current_mana : int
        Aktuální hodnota many.
    """
    
    def __init__(self,username) -> None:
        self.username:str=username
        self.current_hp:int=0
        self.trida:Union[str,None]=None
        self.base_hp:int=0
        self.base_atk:int=0
        self.base_speed:int=0
        self.base_mana:int=0
        self.add_hp:int=0
        self.add_atk:int=0
        self.add_speed:int=0
        self.add_mana:int=0
        self.items_hp:int=0
        self.items_atk:int=0
        self.items_speed:int=0
        self.items_mana:int=0
        self.coins:int=0
        self.inventory:List[Item]=[]
        self.current_mana:int=0
    
    def load(self,db:Database)->None:
        """
        Načte data uživatele ze zadané databáze.
        
        Parametry
        ---------
        db : Database
            Databáze, ze které se načítají data.
        """
        from Database.Actions.Load_player import load_base,get_inventory
        data:Tuple[int,int,int,int,int,int,int,int,int,str,int,int]=load_base(db,self.username)
        self.base_hp=data[0]
        self.base_atk=data[1]
        self.base_speed=data[2]
        self.base_mana=data[3]
        self.add_hp=data[4]
        self.add_atk=data[5]
        self.add_speed=data[6]
        self.add_mana=data[7]
        self.coins=data[8]
        self.trida=data[9]
        self.current_hp=data[10]
        self.current_mana=data[11]
        
        self.inventory:List[Item]=[]
        
        for item in get_inventory(db,self.username):
            tmp:Item=Item(item)
            if tmp.is_using:
                self.items_atk+=tmp.add_atk
                self.items_hp+=tmp.add_hp
                self.items_mana+=tmp.add_mana
                self.items_speed+=tmp.add_speed
            self.inventory.append(tmp)
            
    def update_item_stats(self)->None:
        """
        Aktualizují se staty, které dávají itemy z inventáře
        """
        self.items_atk=0
        self.items_hp=0
        self.items_mana=0
        self.items_speed=0
        for tmp in self.inventory:
            if tmp.is_using:
                self.items_atk+=tmp.add_atk
                self.items_hp+=tmp.add_hp
                self.items_mana+=tmp.add_mana
                self.items_speed+=tmp.add_speed
            
    def save(self,db:Database)->None:
        """
        Uloží data uživatele do zadané databáze.
        
        Parametry
        ---------
        db : Database
            Databáze, do které se ukládají data.
        """
        from Database.Actions.Load_player import save_stats
        from Database.Actions.Inventory_db import get_inventory_2,change_owning_put_on,get_item,create_owning,delete_owning
        if not self.get_full_hp()>=self.current_hp:
            self.current_hp=self.get_full_hp()
        if not self.get_full_mana()>=self.current_mana:
            self.current_hp=self.get_full_mana()
        save_stats(db,self)
        database:List[Tuple[str,str,bool]]=[(nazev,kod,bool(is_using)) for nazev,kod,is_using in get_inventory_2(db,self.username)]
        my_inventory:List[Tuple[str,str,bool]]=[(element.nazev,element.code,element.is_using) for element in self.inventory]
        for tup in database:
            if tup in my_inventory:
                database.remove(tup)
                my_inventory.remove(tup)
        for tup in my_inventory:
            if tup in database:
                database.remove(tup)
                my_inventory.remove(tup)
        #kontrola změny
        if not len(database)==0 and not len(my_inventory)==0:
            common_tuples:List[Tuple[str,str,bool]] = [t for t in my_inventory if any(t[:2] == x[:2] for x in database)]
            for common_nazev,common_kod,common_is_using in common_tuples:
                for index,tup in enumerate(database,start=0):
                    db_nazev,db_kod,db_is_using=tup
                    if db_nazev==common_nazev and db_kod==common_kod:
                        database.pop(index)
                        break
                for index,tup in enumerate(my_inventory,start=0):
                    mi_nazev,mi_kod,mi_is_using=tup
                    if mi_nazev==common_nazev and mi_kod==common_kod:
                        my_inventory.pop(index)
                change_owning_put_on(db,self.username,common_kod,common_is_using)
        #kontrola existence
        for name,code,is_using in database:
            delete_owning(db,self.username,code)
        for name,code,is_using in my_inventory:
            create_owning(db,self.username,code)
        
    def get_full_hp(self)->int:
        """
        Vrátí celkový počet životů uživatele (základní + přídavek z předmětů).
        
        Returns
        -------
        int
            Celkový počet životů uživatele.
        """
        return self.base_hp+self.add_hp+self.items_hp
    
    def get_full_mana(self)->int:
        """
        Vrátí celkovou hodnotu many uživatele (základní + přídavek z předmětů).
        
        Returns
        -------
        int
            Celková hodnota many uživatele.
        """
        return self.base_mana+self.add_mana+self.items_mana
    
    def get_full_atk(self)->int:
        """
        Vrátí celkovou hodnotu atk uživatele (základní + přídavek z předmětů).
        
        Returns
        -------
        int
            Celková hodnota atk uživatele.
        """
        return self.base_atk+self.add_atk+self.items_atk
    
    def get_full_speed(self)->int:
        """
        Vrátí celkovou hodnotu speed uživatele (základní + přídavek z předmětů).
        
        Returns
        -------
        int
            Celková hodnota speed uživatele.
        """
        return self.base_speed+self.add_speed+self.items_speed