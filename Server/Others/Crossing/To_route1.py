from Others.Connection import Connection

def to_route1(connect:Connection)->None:
    from Gameobjects.Map.Route1.Route1 import Route1
    Route1(connect).loop()