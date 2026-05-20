"""
+=======================================+
ZAIMPORTOWANIE: 
a) bibliotek:
        cmd - pisanie szybciej i wydajniej poleceń dotyczących programu
        os - możliwość używania funkcjonalności systemu operacyjnego komputera
        time - opoźnianie procesów w terminalu
b) plików/funkcjonalności z innych plików
        untils->Colors - łatwe zarządzanie barwami w konsoli
+=======================================+
"""

import cmd
import os
import time

from untils import Colors
from objects import User #TYMCZASOWE

colors=Colors()
user=User() #TYMCZASOWE

"""
+=======================================+
KONSOLA POLECEŃ SŁUŻĄCA DO STEROWANIA GRĄ
+=======================================+
"""

class FunctionalCommands(cmd.Cmd):
    #Zmienne służące do wyświetlania czytelnego panelu pomocy
    HELP_TITLE = "SYSTEM POMOCY"
    HELP_SUBTITLE = "KOMENDY"
    HELP_COMMANDS = {} 
    
    #Metody biblioteki cmd, które powodują puste miejsca po wykonanej komendzie
    def precmd(self, line):
        """Wywołuje się automatycznie TUŻ PRZED każdą komendą."""
        print()  
        return line 
    
    def postcmd(self, stop, line):
        """Wywołuje się automatycznie PO każdej wykonanej komendzie."""
        print()  
        return stop
    
    #Komendy systemowe tj. nie wpływające na rozgrywkę
    def do_clear(self, arg):
        """Czyści konsolę."""
        if os.name == 'nt':
            os.system('cls')  
        else:
            os.system('clear')
    
    do_cls = do_clear
    do_wyczysc = do_clear

    def do_exit(self, arg):  
            """Zamyka panel autoryzacji."""
            
            print("Anulowanie procesu autoryzacji...")
            time.sleep(2)
            print("Wyłączenie systemu...")
            return True  
    
    def default(self, line):
        """Wywołuje się, gdy gracz wpisze nieznaną komendę."""
        
        print(f"=== BŁĄD SYSTEMU CERN ===")
        print(f"Komenda '{line}' nie została rozpoznana przez system.")

    def do_help(self, arg):
        """Wyświetla spersonalizowane menu pomocy."""
       
        if arg:
            return super().do_help(arg)
        
        lenght_decoration = 80
        print(f"{colors.bold}{colors.help}" + "\n" + "=" * lenght_decoration)
        print(f"{self.HELP_TITLE:^{lenght_decoration}}")
        print(f"=" * lenght_decoration + f"{colors.clear}")
        
        print(f"{colors.help2}\n[ {self.HELP_SUBTITLE} ]{colors.clear}")
        for cmd_name, cmd_desc in self.HELP_COMMANDS.items():
                print(f"  {cmd_name:<25} - {cmd_desc}")
        
        print(f"{colors.help2}\n[ KOMENDY SYSTEMOWE ]{colors.clear}")
        print(f"  {'clear / cls / wyczysc':<25} - Czyszczenie ekranu konsoli.")
        print(f"  {'help':<25} - Wyświetla menu pomocy.")
        print(f"  {'exit':<25} - Anulowanie procesu autoryzacji.")
        
        print(f"{colors.bold}{colors.help}" + "\n" + "-" * lenght_decoration + f"{colors.clear}")
        print(" Wskazówka: Wpisz 'help <nazwa_komendy>', aby uzyskać szczegóły.")
        print(f"{colors.bold}{colors.help}"+"=" * lenght_decoration + "\n" + f"{colors.clear}")

"""
+==============================================+
KONSOLA POLECEŃ SŁUŻĄCA DO AUTORYZACJI PRZED GRĄ
+==============================================+
"""

class AuthorizationPanel(FunctionalCommands):
    #Zdefiniowanie: prefixu wykonywanych komend, krotkiego wytłumaczenia uzżytkonikowi do czego jest dana konsola
    prompt = f"{colors.bold}{colors.prefix_cmd}CERN_AUTORYZACJA>>> {colors.clear}"
    intro = "Przejdź etap weryfikacji, aby otrzymać dostęp do Panelu Sterowania. \nWpisz 'help', aby zobaczyć komendy.\n"
    
    #Zmienne służące do wyświetlania czytelnego panelu pomocy
    HELP_TITLE = "PANEL AUTORYZACJI CERN - SYSTEM POMOCY"
    HELP_SUBTITLE = "KOMENDY AUTORYZACYJNE"
    HELP_COMMANDS = {
        "login": "Weryfikuje czy użytkownik jest w bazie danych.",
        "password": "Weryfikuje poprawność hasła."
    }

    def __init__(self, uzytkownik):
        super().__init__()
        self.uzytkownik = uzytkownik  
        self.nickname = uzytkownik.nickname 

    #Komendy wpływające na rozgrywkę: pobieranie nazwy od użytkownika, sprawdzenie hasła z dokumentacji
    def do_login(self, arg):
        """Autoryzacja użytkownika. Użycie: login <nazwa>"""
        
        nazwa = arg.strip()  
        
        if nazwa == "":
            print("Nie podano nazwy użytkownika! Autoryzacja zakończona niepowodzeniem.")
            print("Spróbuj jeszcze raz, wpisując: login <nazwa użytkownika>")
            return 
        
        self.nickname = nazwa
        self.uzytkownik.nickname = nazwa
        print(f"Autoryzacja użytkownika zakończona powodzeniem! \nWitaj {self.nickname}!")

    def do_password(self, arg):
        """Weryfikacja hasła. Użycie: password <haslo> \n(hasło podane w dokumentacji)"""
        if self.nickname != "":
            self.password_auth = arg.strip()
            if self.password_auth != self.uzytkownik.password:
                print("Błędne hasło! Autoryzacja zakończona niepowodzeniem.")
                print("Spróbuj jeszcze raz wpisać hasło.")
                return 
            else:
                print(f"Hasło poprawne! Dostęp do systemów CERN został przyznany.")
                self.uzytkownik.auth = True
                return True
        else: 
            print("Nie podano nazwy użytkownika! Autoryzacja zakończona niepowodzeniem.")
            print("Spróbuj jeszcze raz, wpisując: login <nazwa użytkownika>")
            return

"""
+=======================================+
KONSOLA POLECEŃ SŁUŻĄCA DO STEROWANIA GRĄ
+=======================================+
"""

class ControlPanel(FunctionalCommands):
    #Zdefiniowanie: prefixu wykonywanych komend, krotkiego wytłumaczenia uzżytkonikowi do czego jest dana konsola
    prompt = f"{colors.bold}{colors.prefix_cmd}CERN_CMD>>> {colors.clear}"
    intro = "Panel zarządzania maszyną zainicjowany... Wpisz 'help', aby zobaczyć komendy."

    #Zmienne służące do wyświetlania czytelnego panelu pomocy
    HELP_TITLE = "PANEL ZARZĄDZANIA CERN - SYSTEM POMOCY"
    HELP_SUBTITLE = "KOMENDY ZARZĄDZANIA"
    HELP_COMMANDS = {
        "status": "Pokazuje aktualną energię i pozycję wiązki.",
        "wstrzyknij": "Wstrzykuje protony do akceleratora PS."
    }

    #Komendy wpływające na rozgrywkę
    def do_wstrzyknij(self, arg):
        print("Wstrzyknięto protony do PS.")
        """Wstrzykuje protony do akceleratora PS."""

    def do_status(self, arg):
        """Pokazuje aktualną energię i pozycję wiązki."""
        print("Status: Energia = 25 GeV")



# Uruchomienie programu
if __name__ == "__main__":
    AuthorizationPanel(user).cmdloop()
