
def edit_response(client_response:str)->tuple:
    """
    Rozdělí vstupní řetězec na příkaz a jeho argumenty a vrátí je jako tuple.
    Vstupní řetězec musí být ve formátu:
    'příkaz --argument1 --argument2 ...'

    Argumenty jsou odděleny '--' a mohou být dále rozděleny mezerou.
    Pokud neexistují žádné argumenty, vrátí se prázdný seznam.

    Příklady:
    edit_response('help --jedna --dva') => ('help', ['jedna', 'dva'])
    edit_response('help --jedna--dva') => ('help', ['jedna--dva'])
    edit_response('help--jedna') => ('help--jedna', [])
    edit_response('help') => ('help', [])
    edit_response('help --jedna') => ('help', ['jedna'])
    edit_response('help --jedna dva --tri') => ('help', ['jedna dva', 'tri'])
    """
    parts = client_response.split(" --")
    command = parts[0].strip()
    args = []
    for part in parts[1:]:
        arg = part.strip().split(" ")[0]
        args.append(arg)
    return (command, args)