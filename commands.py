"""
+=======================================+
ZAIMPORTOWANIE: 
a) bibliotek:
        os - możliwość używania funkcjonalności systemu operacyjnego komputera
        cmd - pisanie szybciej i wydajniej poleceń dotyczących programu
        time - opóźnianie procesów w terminalu
b) plików/funkcjonalności z innych plików
        utils - import stylów
        object - import obiektów
+=======================================+
"""

import os
import cmd
import time

from utils import Styling, Create_progress_bar 
from cern_map import map_main

#Dostęp do orgazinera stylami
style = Styling()
 
"""
+=======================================+
KONSOLA POLECEŃ SŁUŻĄCA DO STEROWANIA GRĄ
+=======================================+
"""
#KLasa będąca podstawą innych konsoli wykorzystywanych w programie
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
    
    #Komendy systemowe tzn. nie wpływające na rozgrywkę
    def do_mapa(self, arg):
        """Wyświetla mapę ośrodka i obiekty aktywne. \nUżycie: mapa"""
        map_main()
    
    def do_clear(self, arg):
        """Czyści konsolę. \nUżycie: clear"""
        if os.name == 'nt':
            os.system('cls')  
        else:
            os.system('clear')
    
    do_cls = do_clear
    do_wyczysc = do_clear

    def do_exit(self, arg):  
            """Zamyka konsole. \nUżycie: exit"""
            
            print("Anulowanie procesu autoryzacji...")
            time.sleep(2)
            print("Wyłączenie systemu...")
            return True  
    
    def default(self, line):
        """Wywołuje się, gdy gracz wpisze nieznaną komendę."""
        
        title="-BŁĄD SYSTEMU CERN-"
        spaces_count = int((80-(len(title)))/2)
        
        print(f"{style.errors}" + "=" * spaces_count + title + "=" * (spaces_count+1) + "\n")
        print(f"Komenda '{line}' nie została rozpoznana przez system.\n")
        print("="*80 + "\n" + f"{style.clear}")

    def handling_an_exception(self, text):
        title="-BŁĄD SYSTEMU CERN-"
        spaces_count = int((80-(len(title)))/2)
        
        print(f"{style.errors}" + "=" * spaces_count + title + "=" * (spaces_count+1) + "\n")
        print(text + "\n")
        print("="*80 + "\n" + f"{style.clear}")

    def do_help(self, arg):
        """Wyświetla spersonalizowane menu pomocy."""
       
        if arg:
            return super().do_help(arg)
        
        lenght_decoration = 80
        print(f"{style.bold}{style.help}" + "\n" + "=" * lenght_decoration)
        print(f"{self.HELP_TITLE:^{lenght_decoration}}")
        print(f"=" * lenght_decoration + f"{style.clear}")
        
        print(f"{style.help2}\n[ {self.HELP_SUBTITLE} ]{style.clear}")
        for cmd_name, cmd_desc in self.HELP_COMMANDS.items():
                print(f"  {cmd_name:<25} - {cmd_desc}")
        
        print(f"{style.help2}\n[ KOMENDY SYSTEMOWE ]{style.clear}")
        print(f"  {'mapa':<25} - Wyświetla mape ośrodka CERN.")
        print(f"  {'clear / cls / wyczysc':<25} - Czyszczenie ekranu konsoli.")
        print(f"  {'help':<25} - Wyświetla menu pomocy.")
        print(f"  {'exit':<25} - Zamknięcie konsoli CERN'U! Nie programu!.")
        
        print(f"{style.bold}{style.help}" + "\n" + "-" * lenght_decoration + f"{style.clear}")
        print(" Wskazówka: Wpisz 'help <nazwa_komendy>', aby uzyskać szczegóły.")
        print(f"{style.bold}{style.help}"+"=" * lenght_decoration + "\n" + f"{style.clear}")

"""
+==============================================+
KONSOLA POLECEŃ SŁUŻĄCA DO AUTORYZACJI PRZED GRĄ
+==============================================+
"""

class AuthorizationPanel(FunctionalCommands):
    #Zdefiniowanie: prefixu wykonywanych komend, krótkiego przywitania użytkownika
    prompt = f"{style.bold}{style.prefix_cmd}CERN_AUTORYZACJA>>> {style.clear}"
    title_intro =f"{'WITAJ W "CERN: MISJA HIGGS" ':^80}"
    intro = f"{style.bold}{style.welcome_color_1}" + "=" * 80 + f"{style.welcome_color_2}\n{title_intro}\n" + f"{style.welcome_color_1}" + "=" * 80 + "\n\n" + f"{style.clear}{style.welcome_color_2}Witaj, Inżynierze! Jesteś jednym krokiem od uruchomienia największego \neksperymentu w historii nauki.  \n\nPrzejdź weryfikację, aby uzyskać dostęp do układu akceleratorów CERN. \n\n" + f"{style.bold}{style.welcome_color_1}" + "-" * 80 + "\n" + f"{style.clear}{style.welcome_color_2}Wpisz {style.bold}'help'{style.bold_off}, aby zobaczyć komendy.\n" + f"{style.bold}{style.welcome_color_1}" + "=" * 80 + f"{style.clear}\n\n"
    
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
        """Autoryzacja użytkownika. \nUżycie: login <nazwa>"""
        try:
            name = arg.strip()  
        
            if name == "":
                print("Nie podano nazwy użytkownika! Autoryzacja zakończona niepowodzeniem.")
                print("Spróbuj jeszcze raz, wpisując: login <nazwa użytkownika>")
                return 
            
            self.nickname = name
            self.uzytkownik.nickname = name
            print(f"Znaleziono użytkownika w bazie danych! \n\nWitaj {style.bold}{style.welcome_color_2}{self.nickname}!{style.clear} \n\nKontynuuj swoją autoryzacje: password <hasło>")
        
        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd:{type(e).__name__}"
            self.handling_an_exception(text)

    def do_password(self, arg):
        """Weryfikacja hasła. Hasło podane jest w dokumentacji \nUżycie: password <hasło>"""
        try: 
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
            
        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd:{type(e).__name__}"
            self.handling_an_exception(text)

"""
+=======================================+
KONSOLA POLECEŃ SŁUŻĄCA DO STEROWANIA GRĄ
+=======================================+
"""

class ControlPanel(FunctionalCommands):
    #Zdefiniowanie: prefixu wykonywanych komend, krotkiego wytłumaczenia uzżytkonikowi do czego jest dana konsola
    prompt = f"{style.bold}{style.prefix_cmd}CERN_CMD>>> {style.clear}"
    title_intro =f"{'PANEL ZARZĄDZANIA CERN - WITAJ PONOWNIE!':^80}"
    intro = f"{style.bold}{style.welcome_color_1}" + "=" * 80 + f"{style.welcome_color_2}\n{title_intro}\n" + f"{style.welcome_color_1}" + "=" * 80 + "\n\n" + f"{style.clear}{style.welcome_color_2}Etap weryfikacji dla użytkownika zakończony pomyślnie!\n\n" + "System zarządzania akceleratorami zainicjowany pomyślnie! \n\n" + "Użytkownik posiada wszystkie uprawnienia zarządzaniem akceleratorem! \n\n" + f"{style.bold}{style.welcome_color_1}" + "-" * 80 + "\n" + f"{style.clear}{style.welcome_color_2}Wpisz {style.bold}'help'{style.bold_off}, aby zobaczyć komendy.\n" + f"{style.bold}{style.welcome_color_1}" + "=" * 80 + f"{style.clear}\n\n" 
    
    def __init__(self, accelerator, beam):
        super().__init__()
        self.accelerator = accelerator 
        self.beam = beam

        #zdefiniowanie globalnych zmiennych dla tej klasy
        self.total_hydrogen_mass = 0
        self.n = 0
        self.p = 0
        self.ionization_efficiency = 0
        self.I_S_rf_start_power = 0
        self.I_S_rf_power = 0
        self.rf_work = 0
        self.ne = 0
        self.T_cez = 0

    #Zmienne służące do wyświetlania czytelnego panelu pomocy
    HELP_TITLE = "PANEL ZARZĄDZANIA CERN - SYSTEM POMOCY"
    HELP_SUBTITLE = "KOMENDY ZARZĄDZANIA"
    HELP_COMMANDS = {
        "otworz_zawor": "Otwiera zawór piezoelektryczny.",
        "moc_startowa_RF": "Ustawia moc szczytową fal radiowych (RF)",
        "moc_RF": "Ustawia moc roboczą fal radiowych (RF).",
        "temp_cezu" : "Ustawia temperature pieca, który podgrzewa Cez."
    }
    
    #Komendy wpływające na rozgrywkę
    def do_otworz_zawor(self, arg):
        '''Otwiera zawór piezoelektryczny wtrysku wodoru. \nUżycie: otworz_zawor <czas otwarcia w mikrosekundach>'''
        try: 
            self.total_hydrogen_mass = self.total_hydrogen_mass + (self.accelerator.I_S_calculate_mass_hydrogen(0, int(arg)))
            self.n = self.accelerator.I_S_calculate_number_density(self.total_hydrogen_mass)
            self.p = self.accelerator.I_S_calculate_chamber_pressure(self.n)
            print(f"n wynosi: {self.n}")
            print(f"Ciśnienie w komorze wynosi: {self.p} Pa")
            Create_progress_bar(self.p, 1, 4, 20, 5, "Pa", style.welcome_color_1, style.errors, style.welcome_color_2)
        
        except ValueError:
            text = f"Nie możesz: \n- zostawić pustego pola\n- wpisywać liter \n- podawać wielu argumentów komendzie np. otworz_zawor <argument1> <argument2> \n\nPodaj liczbę całkowitą (czas otwarcia zaworu w ms)!"
            self.handling_an_exception(text)
        
        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd:{type(e).__name__}"
            self.handling_an_exception(text)
        
    def do_moc_szczytowa_RF(self, arg):
        '''Ustawia moc szczytową fal radiowych (RF) wymaganą do zapłonu plazmy. \nUżycie: moc_szczytowa_RF <moc w kW>'''
        try: 
            self.ionization_efficiency, self.I_S_rf_start_power = self.accelerator.I_S_calculate_ionization_efficiency(int(arg))
            print(f"Efektywność jonizacji wynosi {self.ionization_efficiency}, moc szczytowa RF wynosi {self.I_S_rf_start_power}")
        
        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd:{type(e).__name__}"
            self.handling_an_exception(text)

    def do_moc_RF(self, arg):
        '''Ustawia moc roboczą fal radiowych (RF) potrzebną do stabilnego podtrzymania plazmy. \nUżycie: moc_RF <moc w kW>'''
        try:
            self.rf_work, self.I_S_rf_power = self.accelerator.I_S_calculate_RF_field_energy(self.n, int(arg))
            self.ne = self.accelerator.I_S_calculate_electron_density(self.I_S_rf_power, self.ionization_efficiency)
            print(f"Rf ma energie: {self.rf_work}, koncentracja jonów ujemnych wynosi: {self.ne}, moc robocza wynosi: {self.I_S_rf_power}")
        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd:{type(e).__name__}"
            self.handling_an_exception(text)

    def do_temp_cezu(self, arg):
        '''Ustawia temperature na jaką piec ma grzać Cez. \nUżycie: temp_cesu <temperatura w c>'''
        try:
            self.T_cez = int(arg)
            if self.T_cez < 40:
                raise ValueError(
                    f"Temperatura {self.T_cez}°C jest ZA NISKA!\n"
                    "Cez nie odparowuje. Brak efektywnej produkcji jonów H-."
                )

            # 2. Walidacja: Za wysoka temperatura (powyżej 100°C)
            elif self.T_cez > 100:
                raise ValueError(
                    f"BŁĄD KRYTYCZNY: Temperatura {self.T_cez}°C jest ZA WYSOKA!\n"
                    "Gwałtowny wyrzut cezu wywołał przebicie elektryczne na elektrodach 45 kV."
                )

            # 3. Reżim ostrzegawczy (wygrzewanie), ale program działa dalej
            elif 80 < self.T_cez <= 100:
                print(f"OSTRZEŻENIE: Temperatura {self.T_cez}°C przekracza normę operacyjną. Wydajność źródła drastecznie spada.!")

            # 4. Prawidłowy zakres operacyjny Linac4
            else:
                print(f"STATUS: Temperatura {self.T_cez}°C w normie. Stabilna praca źródła.")
            self.beam.current = self.accelerator.I_S_calculate__beam_current(self.T_cez, self.ne)
            self.beam.N_Intensity = self.accelerator.I_S_calculate_beam_intensity(self.beam.current)
            self.beam.epsilon = self.accelerator.I_S_calculate_beam_emittance()    
        
        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd:{type(e).__name__}"
            self.handling_an_exception(text)

#Rzeczy, które się wykonają kiedy użytkownik odpali ten plik w konsoli
if __name__ == "__main__":
    print("Jesteś w pliku commands!")