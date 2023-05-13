from Others.Connection import Connection
   
def to_capital_city(connect:Connection):
    from Gameobjects.Map.Capital_city.Capital_city import Capital_city
    Capital_city(connect).loop()
    
def to_route1(connect:Connection):
    from Gameobjects.Map.Route1.Route1 import Route1
    Route1(connect).loop()