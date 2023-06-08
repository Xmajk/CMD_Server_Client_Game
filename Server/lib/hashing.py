import hashlib

def hash_string(string):
    """
    Metoda, která zahešuje vstup a vrátí jej
    
    Parametry
    ---------
    string : str
        Vstupní string
    
    Returns
    -------
    str :
        Zahešovaný vstupní parametr
    """
    encoded_string = string.encode('utf-8')
    hash_object = hashlib.sha256(encoded_string)
    return hash_object.hexdigest()