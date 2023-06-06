from Others.Connection import Connection
   
def to_capital_city(connect:Connection):
    """
    Metoda sloužící k přechodu na lokaci Hlavní město

    Parametry
    ---------
    connect : Connection
        Instance třídy Connection, která reprezentuje spojení s klientem.
    """
    from Gameobjects.Map.Capital_city.Capital_city import Capital_city
    Capital_city(connect).loop()
    
def to_route1(connect:Connection):
    """
    Metoda sloužící k přechodu na lokaci Route1

    Parametry
    ---------
    connect : Connection
        Instance třídy Connection, která reprezentuje spojení s klientem.
    """
    from Gameobjects.Map.Route1.Route1 import Route1
    Route1(connect).loop()
    
def to_forest(connect:Connection):
    """
    Metoda sloužící k přechodu na lokaci Lesa

    Parametry
    ---------
    connect : Connection
        Instance třídy Connection, která reprezentuje spojení s klientem.
    """
    from Gameobjects.Map.Forest.Forest import Forest
    Forest(connect).loop()
    
def to_route2(connect:Connection):
    """
    Metoda sloužící k přechodu na lokaci Route2

    Parametry
    ---------
    connect : Connection
        Instance třídy Connection, která reprezentuje spojení s klientem.
    """
    from Gameobjects.Map.Route2.Route2 import Route2
    Route2(connect).loop()
    
def to_gem_town(connect:Connection):
    """
    Metoda sloužící k přechodu na lokaci Rubínové město

    Parametry
    ---------
    connect : Connection
        Instance třídy Connection, která reprezentuje spojení s klientem.
    """
    from Gameobjects.Map.Gem_town.Gem_town import Gem_town
    Gem_town(connect).loop()