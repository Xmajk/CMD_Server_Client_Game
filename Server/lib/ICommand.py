from abc import ABC,abstractmethod

class ICommand(ABC):
    """
    Abstraktní třída pro příkaz
    """
    @abstractmethod
    def execute(self)->bool:
        """
        Metoda, která souží k provedení příkazu
        
        Return
        ------
        bool
            Vrací jestli má daný level interfacu pokračovat
        """
        pass