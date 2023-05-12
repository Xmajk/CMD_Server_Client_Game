from Others.Connection import Connection

def to_capital_city(connect:Connection)->None:
    from Gameobjects.Map.Capital_city.Capital_city import Capital_city
    Capital_city(connect).loop()