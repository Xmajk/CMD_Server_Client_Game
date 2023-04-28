from enum import Enum

class Next_message(Enum):
    """
    Enum jakého typu (jestli přijímání, nebo posílání) bude další zpráva    
    """
    PRIJMI="prijmi"
    POSLI="posli"
    