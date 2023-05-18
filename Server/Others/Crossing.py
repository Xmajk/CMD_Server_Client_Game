from Others.Connection import Connection
   
def to_capital_city(connect:Connection):
    from Gameobjects.Map.Capital_city.Capital_city import Capital_city
    Capital_city(connect).loop()
    
def to_route1(connect:Connection):
    from Gameobjects.Map.Route1.Route1 import Route1
    Route1(connect).loop()
    
def to_life_of_forest(connect:Connection):
    from Gameobjects.Map.Forest_of_life.Forest_of_life import Forest_of_life
    Forest_of_life(connect).loop()
    
def to_route2(connect:Connection):
    from Gameobjects.Map.Route2.Route2 import Route2
    Route2(connect).loop()
    
def to_gem_town(connect:Connection):
    from Gameobjects.Map.Gem_town.Gem_town import Gem_town
    Gem_town(connect).loop()