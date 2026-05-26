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
import turtle

from utils import Styling, Create_progress_bar 
from cern_map import map_main

from physics import *

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
    def __init__(self, completekey = "tab", stdin = None, stdout = None):
        super().__init__(completekey, stdin, stdout)
        self.map_activated = False
    
    #Metody biblioteki cmd, które powodują puste miejsca po wykonanej komendzie
    def precmd(self, line):
        """Wywołuje się automatycznie TUŻ PRZED każdą komendą."""
        
        #odświeżanie okna turtle, aby się nie zawiesiło
        if self.map_activated == True:
            try:
                turtle.update()
            except turtle.Terminator:
                pass
        print()  
        return line 
    
    def postcmd(self, stop, line):
        """Wywołuje się automatycznie PO każdej wykonanej komendzie."""
        
        #odświeżanie okna turtle, aby się nie zawiesiło
        if self.map_activated == True:
            try:
                turtle.update()
            except turtle.Terminator:
                pass
        print()  
        return stop
    
    #Metoda będąca szablonem ładnego wypisywania informacji w konsoli
    def _show_status (self, text_status, bar = None, bar_next_to_text = None, title = "RAPORT PO WYKONANEJ OPERACJI", color_1 = style.status_1_color, color_2 = style.status_2_color):
        lenght_decoration = style.DECORATE_LENGHT
        print(f"{style.bold}{color_1}" + "\n" + "=" * lenght_decoration)
        print(f"{title:^{lenght_decoration}}")
        print(f"=" * lenght_decoration + f"{style.clear}")
        print("")
       
        if bar_next_to_text is not None:
            print(f"{color_2}{text_status} {bar_next_to_text}")
            if bar is not None:
                bar()          
       
        elif bar is not None:
            print(f"{color_2}{text_status}")
            bar()
 
        else:
            print(f"{color_2}{text_status}")
        
        print("")
        print(f"{style.bold}{color_1}"+"=" * lenght_decoration + "\n" + f"{style.clear}")
    
    #Przypisywanie stage każdemu akceleartorowi jako blokada wykonywania niedozwolonych komend w danym ticku gry
    def _set_stage(self, accelerator_environment):
        if accelerator_environment.active == accelerator_environment.negative_ion_source:
            accelerator_environment.active.stage = 2
        elif accelerator_environment.active == accelerator_environment.linac4:
            accelerator_environment.active.stage = 3
        elif accelerator_environment.active == accelerator_environment.booster:
            accelerator_environment.active.stage = 4
        elif accelerator_environment.active == accelerator_environment.ps:
            accelerator_environment.active.stage = 5
        elif accelerator_environment.active == accelerator_environment.sps:
            accelerator_environment.active.stage = 6
        elif accelerator_environment.active == accelerator_environment.lhc:
            accelerator_environment.active.stage = 7

    #Ukryta metoda skracająca zapis powtarzającej się rzczy
    def _print_step_error(self):
        text = f"Nie możesz wykonać tego polecenia! Wcześniejsze prametry są ustawione nieprawidłowo lub wogóle nie są ustawione! \n\nUżyj najperw komendy: poprzedzającą, której użyłeś (są ustawione w odpwoeidniej koeljności w help)"
        self._handling_an_exception(text)
    
    #Metoda wyświetlająca okno z mapą
    def do_mapa(self, arg):
        """Wyświetla mapę ośrodka i obiekty aktywne. \nUżycie: mapa"""
        self.map_activated = True
        map_main()
    
    #Metoda czyszcząca konsole
    def do_clear(self, arg):
        """Czyści konsolę. \nUżycie: clear"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    do_cls = do_clear
    do_wyczysc = do_clear

    #Metoda zamykająca dany panel sterowania
    def do_exit(self, arg):  
            """Zamyka konsole. \nUżycie: exit"""
            
            print(f"{style.bold}{style.prefix_cmd}CERN>>> {style.clear}Zamykam obecny panel sterowania...")
            time.sleep(2)
            return True  
    
    #Metoda obsługująca błąd z nieorzpoznaniem komendy
    def default(self, line):
        """Wywołuje się, gdy gracz wpisze nieznaną komendę."""
        
        title="-BŁĄD SYSTEMU CERN-"
        spaces_count = int((style.DECORATE_LENGHT-(len(title)))/2)
        
        print(f"{style.errors}" + "=" * spaces_count + title + "=" * (spaces_count+1) + "\n")
        print(f"Komenda '{line}' nie została rozpoznana przez system.\n")
        print("="*style.DECORATE_LENGHT + "\n" + f"{style.clear}")

    #Ukryta metoda wypisująca błąd władny sposób
    def _handling_an_exception(self, text):
        title="-BŁĄD SYSTEMU CERN-"
        spaces_count = int((style.DECORATE_LENGHT-(len(title)))/2)
        
        print(f"{style.errors}" + "=" * spaces_count + title + "=" * (spaces_count+1) + "\n")
        print(text + "\n")
        print("="*style.DECORATE_LENGHT + "\n" + f"{style.clear}")

    #Metoda wyśwtlająca menu pomocy
    def do_help(self, arg):
        """Wyświetla spersonalizowane menu pomocy."""
       
        if arg:
            return super().do_help(arg)
        
        lenght_decoration = style.DECORATE_LENGHT
        print(f"{style.bold}{style.help_color}" + "\n" + "=" * lenght_decoration)
        print(f"{self.HELP_TITLE:^{lenght_decoration}}")
        print(f"=" * lenght_decoration + f"{style.clear}")
        
        print(f"{style.help_2_color}\n[ {self.HELP_SUBTITLE} ]{style.clear}")
        for cmd_name, cmd_desc in self.HELP_COMMANDS.items():
                print(f"  {cmd_name:<35} - {cmd_desc}")
        
        print(f"{style.help_2_color}\n[ KOMENDY SYSTEMOWE ]{style.clear}")
        print(f"  {'mapa':35} - Wyświetla mape ośrodka CERN.")
        print(f"  {'podpowiedz':<35} - Wyświetla małą podpowiedź co w danym kroku gry trzeba zrobić.")
        print(f"  {'':<35}   (dostępna dopiero od włączenia systemu!)")
        print(f"  {'help':<35} - Wyświetla menu pomocy.")
        print(f"  {'clear / cls / wyczysc':<35} - Czyszczenie ekranu konsoli.")
        print(f"  {'exit':<35} - Zamknięcie konsoli CERN'U! Nie programu!.")
        
        print(f"{style.bold}{style.help_color}" + "\n" + "-" * lenght_decoration + f"{style.clear}")
        print(" Wskazówka: Wpisz 'help <nazwa_komendy>', aby uzyskać szczegóły.")
        print(f"{style.bold}{style.help_color}"+"=" * lenght_decoration + "\n" + f"{style.clear}")
"""
+==============================================+
KONSOLA POLECEŃ SŁUŻĄCA DO AUTORYZACJI PRZED GRĄ
+==============================================+
"""

class AuthorizationPanel(FunctionalCommands):
    #Zdefiniowanie: prefixu wykonywanych komend, krótkiego przywitania użytkownika
    prompt = f"{style.bold}{style.prefix_cmd}CERN_AUTORYZACJA>>> {style.clear}"
    title_intro =f"{'WITAJ W CERN: MISJA HIGGS':^100}"
    intro = \
    f"{style.bold}{style.welcome_color_1}" + "=" * style.DECORATE_LENGHT \
    + f"{style.welcome_color_2}\n{title_intro}\n" \
    + f"{style.welcome_color_1}" + "=" * style.DECORATE_LENGHT + "\n\n" \
    + f"{style.clear}{style.welcome_color_2}Witaj, Inżynierze! Jesteś jednym krokiem od uruchomienia największego eksperymentu w historii nauki.  \n\nPrzejdź weryfikację, aby uzyskać dostęp do układu akceleratorów CERN. \n\n" \
    + f"{style.bold}{style.welcome_color_1}" + "-" * style.DECORATE_LENGHT + "\n" \
    + f"{style.clear}{style.welcome_color_2}Wpisz {style.bold}'help'{style.bold_off}, aby zobaczyć komendy.\n" + f"{style.bold}{style.welcome_color_1}" \
    + "=" * style.DECORATE_LENGHT + f"{style.clear}\n\n"\
    
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
            self._handling_an_exception(text)

    def do_password(self, arg):
        """Weryfikacja hasła. Hasło podane jest w dokumentacji \nUżycie: password <hasło>"""
        try: 
            if self.nickname != "":
                self.password_auth = arg.strip()
                if self.password_auth != self.uzytkownik.password:
                    print("Błędne hasło! Autoryzacja zakończona niepowodzeniem.")
                    print("Spróbuj jeszcze raz, wpisując: password <password")
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
            self._handling_an_exception(text)

"""
+=========================================================+
KONSOLA POLECEŃ SŁUŻĄCA DO STEROWANIA NEGATIVE ION SOURCE
+=========================================================+
"""

class ControlPanelIonSource(FunctionalCommands):
    #Zdefiniowanie: prefixu wykonywanych komend, krotkiego wytłumaczenia użytkonikowi do czego jest dana konsola
    prompt = f"{style.bold}{style.prefix_cmd}CERN_CMD>>>ION_SOURCE>>> {style.clear}"
    title_intro =f"{'PANEL ZARZĄDZANIA CERN - WITAJ PONOWNIE!':^100}"
    intro = \
    f"{style.bold}{style.welcome_color_1}" + "=" * style.DECORATE_LENGHT \
    + f"{style.welcome_color_2}\n{title_intro}\n" + f"{style.welcome_color_1}" \
    + "=" * style.DECORATE_LENGHT + "\n\n" + f"{style.clear}{style.welcome_color_2}Etap weryfikacji dla użytkownika zakończony pomyślnie!\n\n" \
    + "System zarządzania akceleratorami zainicjowany pomyślnie! \n\n" \
    + "Użytkownik posiada wszystkie uprawnienia zarządzaniem akceleratorem! \n\n" \
    + f"{style.bold}{style.welcome_color_1}" + "-" * style.DECORATE_LENGHT + "\n" \
    + f"{style.clear}{style.welcome_color_2}Wpisz {style.bold}'help'{style.bold_off}, aby zobaczyć komendy.\n" \
    + f"{style.bold}{style.welcome_color_1}" + "=" * style.DECORATE_LENGHT + f"{style.clear}\n\n" 
    
    def __init__(self, accelerator_environment, beam, accelerator,):
        super().__init__()
        self.acc_env = accelerator_environment
        self.accelerator = accelerator 
        self.beam = beam

        #zdefiniowanie obecnego akceleratora
        self.acc_env.set_accelerator("Negative Ion Source")
        #zdefiniowanie początkowej wartości kroku dla gry w danym akceleratorze
        self.acc_env.active.step_game = 0

    #Zmienne służące do wyświetlania czytelnego panelu pomocy
    HELP_TITLE = "PANEL ZARZĄDZANIA NEGATIVE ION SOURCE - SYSTEM POMOCY"
    HELP_SUBTITLE = "KOMENDY ZARZĄDZANIA"
    HELP_COMMANDS = {
        "otworz_zawor": "Otwiera zawór piezoelektryczny.",
        "moc_startowa_RF": "Ustawia moc szczytową fal radiowych (RF)",
        "moc_RF": "Ustawia moc roboczą fal radiowych (RF).",
        "temp_cezu" : "Ustawia temperature pieca, który podgrzewa Cez.",
        "gotowe": "Kończy działania na danym odcinku, w tym przypaduku w Ion Source"
    }
    
    #zdefiniowanie podpowiedzi dla każdego kroku gry
    def do_podpowiedz(self, arg):
        if self.acc_env.active.step_game == 0:
            text_status = f"Twoim zadnaiem jest ustawienie poprawnej wartości ciśnienia. \n\nZakres poprawnego ciśnienia wynosi: [2.8, 4.2] Pa \n\nJeśli pasek zmieni kolor z czerwonego na zielony możesz przejść dalej, \njeśli nie bedzie zielony otwieraj zawór dopóki nie dobijesz do właściwych \nwartości." 
            self._show_status(text_status, title="PODPOWIEDŹ", color_1=style.hint_color_1, color_2=style.hint_color_2)
        elif self.acc_env.active.step_game == 1:
            text_status = f"Twoim zdaniem jest ustawienie mocy szczytowa RF w komorze na odpowiednią wartość. \nTa wartość będzie miała duży wpływ na sworzenie się wiązki. \n\nZakres mocy szcytowej RF wynosi: [20, 100] kW" 
            self._show_status(text_status, title="PODPOWIEDŹ", color_1=style.hint_color_1, color_2=style.hint_color_2)
        elif self.acc_env.active.step_game == 2:
            text_status = f"Twoim zdaniem jest ustawienie mocy robocza RF w komorze na odpowiednią wartość. \n\nZakres mocy RF wynosi: [10, 50] kW" 
            self._show_status(text_status, title="PODPOWIEDŹ", color_1=style.hint_color_1, color_2=style.hint_color_2)
        elif self.acc_env.active.step_game == 3:
            text_status = f"Twoim zadaniem jest ustawić poprawną temperature pieca. \n\nZakres temperatury wynosi: [40, 100] °C" 
            self._show_status(text_status, title="PODPOWIEDŹ", color_1=style.hint_color_1, color_2=style.hint_color_2)
        elif self.acc_env.active.step_game == 4:
            text_status = f"Wpisz gotowe, aby przejść do następnego etapu przygotowywania wiązki." 
            self._show_status(text_status, title="PODPOWIEDŹ", color_1=style.hint_color_1, color_2=style.hint_color_2)

    #Metody wpływające na rozgrywkę

    def do_otworz_zawor(self, arg):
        '''Otwiera zawór piezoelektryczny wtrysku wodoru. \nUżycie: otworz_zawor <czas otwarcia w mikrosekundach>'''
        try: 
            if self.acc_env.active.step_game == 0:
                self.acc_env.active.total_time_open_valve += int(arg)
                self.acc_env.active.total_hydrogen_mass = self.acc_env.active.total_hydrogen_mass + (self.accelerator.I_S_calculate_mass_hydrogen(0, int(arg)))
                self.acc_env.active.n = self.accelerator.I_S_calculate_number_density(self.acc_env.active.total_hydrogen_mass)
                self.acc_env.active.p = self.accelerator.I_S_calculate_chamber_pressure(self.acc_env.active.n)
                
                text_status = (
                    f"Zawór został otwarty na {arg} mikrosekund.\n"
                    f"Masa wodoru wynosi: {self.acc_env.active.total_hydrogen_mass}, \n" 
                    f"Koncentracja H2 w komorze wynosi: {self.acc_env.active.n}," 
                )

                bar_p = lambda: Create_progress_bar(self.acc_env.active.p, 7.0, 2.8, 4.2, 20, 5, style.valid, style.errors, style.status_2_color, prefix=f"Ciśnienie w komorze wynosi: {self.acc_env.active.p:.2f} Pa ")
                self._show_status(text_status, bar=bar_p)
                
                if  2.5 <= self.acc_env.active.p <= 4.5:
                    self.acc_env.active.step_game = 1
                    text_status = f"Wszystko się zgadza! Możesz przejść do następnego kroku: moc_szczytowa_RF" 
                    self._show_status(text_status, title="INFORMACJA", color_1=style.hint_color_1, color_2=style.hint_color_2)
                else:
                    print(f"{style.bold}{style.prefix_cmd}CERN_CMD>>>ION_SOURCE>>> {style.clear}Jeśli czegoś nie rozumiesz użyj: podpowiedz")
            else:
                self._print_step_error()
               
        except ValueError:
            text = f"Nie możesz: \n- zostawić pustego pola\n- wpisywać liter \n- podawać wielu argumentów komendzie np. otworz_zawor <argument1> <argument2> \n\nPodaj liczbę całkowitą (czas otwarcia zaworu w mikrosekundach)!"
            self._handling_an_exception(text)
        
        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd: {type(e).__name__} \n{str(e)}"
            self._handling_an_exception(text)
      
    def do_moc_szczytowa_RF(self, arg):
        '''Ustawia moc szczytową fal radiowych (RF) wymaganą do zapłonu plazmy. \nUżycie: moc_szczytowa_RF <moc w kW>'''
        try: 
            if self.acc_env.active.step_game == 1:
                self.acc_env.active.ionization_efficiency, self.acc_env.active.I_S_rf_peak_power = self.accelerator.I_S_calculate_ionization_efficiency(int(arg))
                
                text_status = (
                    f"Moc szczytowa RF ustawiona na: {self.acc_env.active.I_S_rf_peak_power}, \n"
                    f"Efektywność jonizacji wynosi: {self.acc_env.active.ionization_efficiency},"
                )
                self._show_status(text_status)
            
                if  20 <= self.acc_env.active.I_S_rf_peak_power <= 100:
                    self.acc_env.active.step_game = 2
                    text_status = f"Wszystko się zgadza! Możesz przejść do następnego kroku: moc_RF" 
                    self._show_status(text_status, title="INFORMACJA", color_1=style.hint_color_1, color_2=style.hint_color_2)
                else: 
                    print(f"{style.bold}{style.prefix_cmd}CERN_CMD>>>ION_SOURCE>>> {style.clear}Jeśli czegoś nie rozumiesz użyj: podpowiedz")
            else:
                self._print_step_error()

        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd: {type(e).__name__} \n{str(e)}"
            self._handling_an_exception(text)

    def do_moc_RF(self, arg):
        '''Ustawia moc roboczą fal radiowych (RF) potrzebną do stabilnego podtrzymania plazmy. \nUżycie: moc_RF <moc w kW>'''
        try:
            if self.acc_env.active.step_game == 2:
                self.acc_env.active.rf_work, self.acc_env.active.I_S_rf_power = self.accelerator.I_S_calculate_RF_field_energy(self.acc_env.active.n, int(arg))
                self.acc_env.active.ne = self.accelerator.I_S_calculate_electron_density(self.acc_env.active.I_S_rf_power, self.acc_env.active.ionization_efficiency)
                
                text_status= (
                    f"Moc robocza ustawiona na: {self.acc_env.active.I_S_rf_power}, \n"
                    f"RF dostarcza energii: {self.acc_env.active.rf_work:.2f}, \n"
                    f"Koncentracja jonów o identycznym ładunku wynosi: {self.acc_env.active.ne:.4f},"
                )
                self._show_status(text_status)

                if  10 <= self.acc_env.active.I_S_rf_power <= 50:
                    self.acc_env.active.step_game = 3
                    text_status = f"Wszystko się zgadza! Możesz przejść do następnego kroku: temp_cezu" 
                    self._show_status(text_status, title="INFORMACJA", color_1=style.hint_color_1, color_2=style.hint_color_2)
                else:
                    print(f"{style.bold}{style.prefix_cmd}CERN_CMD>>>ION_SOURCE>>> {style.clear}Jeśli czegoś nie rozumiesz użyj: podpowiedz")
            else:
                self._print_step_error()
            
        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd: {type(e).__name__} \n{str(e)}"
            self._handling_an_exception(text)

    def do_temp_cezu(self, arg):
        '''Ustawia temperature na jaką piec ma grzać Cez. \nUżycie: temp_cesu <temperatura w c>'''
        try:
            if self.acc_env.active.step_game == 3:
                self.acc_env.active.T_cez = int(arg)

                self.beam.current = self.accelerator.I_S_calculate__beam_current(self.acc_env.active.T_cez, self.acc_env.active.ne)
                self.beam.N_Intensity = self.accelerator.I_S_calculate_beam_intensity(self.beam.current)
                self.beam.epsilon = self.accelerator.I_S_calculate_beam_emittance()    

                text_status = (
                    f"Temperature pieca cezu ustawiono na: {self.acc_env.active.T_cez}°C \n"
                    f"RF dostarcza energii: {self.acc_env.active.rf_work}, \n"
                    f"Koncentracja jonów o identycznym ładunk uwynosi: {self.acc_env.active.ne},"
                )
                self._show_status(text_status)

                if  40 < self.acc_env.active.T_cez < 100:
                    self.acc_env.active.step_game = 4
                    text_status = f"Wszystko się zgadza! Możesz przejść do następnego kroku: gotowe" 
                    self._show_status(text_status, title="INFORMACJA", color_1=style.hint_color_1, color_2=style.hint_color_2)
                else:
                    print(f"{style.bold}{style.prefix_cmd}CERN_CMD>>>ION_SOURCE>>> {style.clear}Jeśli czegoś nie rozumiesz użyj: podpowiedz")
            else:
                self._print_step_error()
        
        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd:{type(e).__name__} \n{str(e)}"
            self._handling_an_exception(text)
    
    #sprawdza czy można przejść do kolejnej części symulatora
    def do_gotowe(self, arg):
        try:
            if self.acc_env.active.step_game == 4: 
                a = self.acc_env.active
                if all([a.total_hydrogen_mass, a.n, a.p, a.ionization_efficiency, a.I_S_rf_peak_power, a.rf_work, a.I_S_rf_power, a.ne, a.T_cez, self.beam.current, self.beam.N_Intensity, self.beam.epsilon]):
                    self._set_stage(self.acc_env)
                    text_status = (
                        f"Zawór został otwarty na {self.acc_env.active.total_time_open_valve} mikrosekund. \n"
                        f"Masa wodoru wynosi: {self.acc_env.active.total_hydrogen_mass}. \n"
                        f"Koncentracja H2 w komorze wynosi: {self.acc_env.active.ne}. \n"
                        f"Ciśnienie w komorze wynosi: {self.acc_env.active.p:.2f} Pa.\n"
                        f"Moc szczytowa RF ustawiona na: {self.acc_env.active.I_S_rf_peak_power}\n"
                        f"Moc robocza RF wynosi: {self.acc_env.active.I_S_rf_power}. \n"
                        f"Temperatura pieca cezu wynosi:{self.acc_env.active.T_cez}°C. \n"
                        f"RF dostarcza energii: {self.acc_env.active.rf_work}. \n"
                        f"Koncentracja jonów o identycznym ładunku wynosi: {self.acc_env.active.ne}."
                    )
                    self._show_status(text_status)
                    self.do_exit("")
                    time.sleep
                    return True
                else: 
                    self._print_step_error()
            else: 
                self._print_step_error()    

        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd:{type(e).__name__} \n{str(e)}"
            self._handling_an_exception(text)

"""
+=========================================================+
KONSOLA POLECEŃ SŁUŻĄCA DO STEROWANIA LiNAC4
+=========================================================+
"""

class ControlPanelLinac4(FunctionalCommands):
    #Zdefiniowanie: prefixu wykonywanych komend, krotkiego wytłumaczenia uzżytkonikowi do czego jest dana konsola
    prompt = f"{style.bold}{style.prefix_cmd}CERN_CMD>>>Linac4>>>LEBT>>> {style.clear}"
    title_intro =f"{'PANEL ZARZĄDZANIA CERN - Linac4 LEBT':^100}"
    intro = (
        f"{style.bold}{style.welcome_color_1}" + "=" *style.DECORATE_LENGHT 
        + f"{style.welcome_color_2}\n{title_intro}\n" + f"{style.welcome_color_1}" 
        + "=" * style.DECORATE_LENGHT + "\n\n" + f"{style.clear}{style.welcome_color_2}" 
        + f"{'Obecnie zarządzasz akceleratorem Linac! A dokładnie odcinkiem LEBT.':^100}\n" 
        + f"{style.bold}{style.welcome_color_1}" + "\n" +"-" * style.DECORATE_LENGHT + "\n" 
        + f"{style.clear}{style.welcome_color_2}Wpisz {style.bold}'help'{style.bold_off}, aby zobaczyć komendy.\n" 
        + f"{style.bold}{style.welcome_color_1}" + "=" * style.DECORATE_LENGHT + f"{style.clear}\n\n" 
    )
    def __init__(self, accelerator_environment, beam, accelerator,):
        super().__init__()
        self.acc_env = accelerator_environment
        self.accelerator = accelerator 
        self.beam = beam
        self.lebt_lenght = 1.8
        self.current_lebt_lenght = 0
        
        #zdefiniowanie w którym akceleratorze jesteśmy
        self.acc_env.set_accelerator("Linac4")
        #kopia parametrów z poprzedniego akceleratora na obecny
        self.acc_env.copy_data("Negative Ion Source", "Linac4")
        #ustawienie kroku gry
        self.acc_env.active.step_game = 0

    #Zmienne służące do wyświetlania czytelnego panelu pomocy
    HELP_TITLE = "PANEL ZARZĄDZANIA LINAC4 - SYSTEM POMOCY"
    HELP_SUBTITLE = "KOMENDY ZARZĄDZANIA"
    HELP_COMMANDS = {
        "status_wiazki": "Wyświetla informacje o stanie wiązki.",
        "prad_solenoidu": "Ustawia prąd przepływający przez solenoid.",
        "napiecie_magnesu_korekcyjnego": "Ustawia napięcie magnesu korekcyjnego (sterera).",
        "pompa_prozni": "Włacza pompę, która odpompowuje gaz tworząc próżnie.",
        "gotowe": "Kończy działania na danym odcinku, w tym przypaduku w Linac4 LEBT"
    }

    #Metoda wyświetlająca okno z mapą
    def do_mapa(self, arg):
        """Wyświetla mapę ośrodka i obiekty aktywne. \nUżycie: mapa"""
        self.map_activated = True
        map_main("Linac4")


    #Metoda służaca do udzielania podpwoeidzi by użytkownikowi wskazać co powinien robić 
    def do_podpowiedz(self, arg):
        if self.acc_env.active.step_game == 0:
            text_status = f"Używaj tych komend aby zarządzać wiązką poruszającą się w akceleratorze: \n\n- prad_solenoidu: głównie wpływa na ustawienie odpowiedniego odchylenia od środka przekroju \noczekiwana wartość: [200, 300] \n\n- napiecie_magnesu_korekcyjnego: głównie wpływa na kąt poruszania się wiązki \noczekiwana wartość:  [-50, 50] \n- pompa_prozni: wpływa głównie na utratę prądu w wiązce czym wieksza wartość ciśnienia tym gorzej \noczekiwana wartość: on \n\nTwoim zadaniem jest sterować parametrami aby wiązka pokonała dystans LEBT'u \nnie rozbijając się o ściane i nie tracąc prądu." 
            self._show_status(text_status, title="PODPOWIEDŹ", color_1=style.hint_color_1, color_2=style.hint_color_2)
        elif self.acc_env.active.step_game == 1:
            text_status = f"Wpisz gotowe, aby przejść do następnego etapu przygotowywania wiązki." 
            self._show_status(text_status, title="PODPOWIEDŹ", color_1=style.hint_color_1, color_2=style.hint_color_2)

    #Metoda służąca do wypisania informacji o wiązce
    def do_status_wiazki(self, arg):
        
        self.beam_position_y_covert_to_mm   = self.beam.position_y * 1000          
        self.beam_angle_conevrt_to_mrad= self.beam.angle * 1000            

        """Komenda wyświetla zaawansowany raport o stanie wiązki. \nUżycie: status_wiazki""" 
        raport = (
            f"{'--- GEOMETRIA WIAZKI ---':^100}\n\n"
            f"{'Pozycja X (droga w tunelu):':<40} {self.beam.position_x:.4f} m\n"
            f"{'Odchylenie Y od osi (cel: 0 mm):':<40} {self.beam_position_y_covert_to_mm:.4f} mm   [{self.beam.caluclate_percent_pos_y(0.01, 2)}]\n"
            f"{'Kąt trajektorii (cel: 0 mrad):':<40} {self.beam_angle_conevrt_to_mrad:.4f} mrad\n"
            f"\n"
            f"{'--- ENERGIA I PREDKOSC ---':^100}\n\n"
            f"{'Energia kinetyczna:':<40} {self.beam.energy:.4f} MeV\n"
            f"{'Rozrzut energii:':<40} {self.beam.energy_spread:.2f} %\n"
            f"{'Prędkość (% prędkości światła):':<40} {self.beam.percent_light_speed:.2f} % c\n"
            f"\n"
            f"{'--- PARAMETRY WIAZKI ---':^100}\n\n"
            f"{'Prąd wiązki:':<40} {str(round(self.beam.current, 4)) + ' mA' if self.beam.current is not None else 'nie ustawiono'}\n"
            f"{'Intensywność (N cząstek):':<40} {self.beam.N_Intensity if self.beam.N_Intensity is not None else 'nie ustawiono'}\n"
            f"{'Emitancja (chaos trajektorii):':<40} {str(round(self.beam.epsilon, 4)) + ' mm*mrad' if self.beam.epsilon is not None else 'nie ustawiono'}\n"
            f"{'Świetlność potencjalna:':<40} {self.beam.luminosity_potential:.1f} %\n"
            f"{'Profil (promień wiązki) (x, y)':<40} {self.beam.profile if self.beam.profile is not None else 'nie ustawiono'}\n"
            f"{'Faza pola RF:':<40} {self.beam.RF_phase if self.beam.profile is not None else 'nie ustawiono'}\n"
            f"{'Struktura wiązki:':<40} {self.beam.bunch_structure if self.beam.profile is not None else 'nie ustawiono'}"
        )
         
        # Wywołanie wyświetlenia na ekranie
        self._show_status(raport, title="OBECNY STAN WIĄZKI")

    #Komendy wpływające na rozgrywkę:

    #Metoda ustawiająca prąd w solenoidzie
    def do_prad_solenoidu(self, arg):
        '''Komenda ustawiająca prąd przepływający przez solenoid, aby skupiać wiązkę anionów wodoru. \nUżycie: prad_solenoidu <nateżenie pradu w Amperach [A]>'''
        try: 
            self.beam_position_y_covert_to_mm   = self.beam.position_y * 1000          
            self.beam_angle_conevrt_to_mrad = self.beam.angle * 1000            
            
            self.prev_current = self.beam.current or 0.0
            self.prev_position_y = self.beam.position_y or 0.0
            self.prev_angle = self.beam.angle or 0.0
            if self.acc_env.active.step_game == 0:    
                self.acc_env.active.current_solenoid = float(arg)
                
                if self.acc_env.active.current_solenoid < 200:
                    raise ValueError("Zbyt niski prąd! Solenoid nie będzie skutecznie skupiał wiązki.")
                elif self.acc_env.active.current_solenoid > 300:
                    raise ValueError("Zbyt wysoki prąd! Solenoid ulegnie uszkodzeniu. Maksymalny bezpieczny prąd to 300 A.")
                
                remaining_distance = self.lebt_lenght - self.current_lebt_lenght
                self.acc_env.active.dx = random.uniform(0.10, 0.28)
                if self.acc_env.active.dx >= remaining_distance:
                    self.acc_env.active.dx = remaining_distance
                self.acc_env.active.path_length += self.acc_env.active.dx
                self.current_lebt_lenght += self.acc_env.active.dx

                self.acc_env.active.focusing_force = self.accelerator.lebt_calculate_solenoid_focus(self.acc_env.active.current_solenoid, self.beam.energy)
                self.acc_env.active.current_solenoid, self.acc_env.active.current_vacuum = self.accelerator.lebt_process_automatic_step(self.beam, self.acc_env.active.current_solenoid, self.acc_env.active.current_vacuum, self.acc_env.active.steerer_voltage, self.acc_env.active.dx)
 
                if abs(self.beam_position_y_covert_to_mm) < 2.0 and  self.acc_env.active.focusing_force > 0.001:
                    rate = "DOBRY - wiązka skupiona i wycentrowana"
                elif abs(self.beam_position_y_covert_to_mm) < 5.0:
                    rate = "ŚREDNI - odchylenie, użyj magnesu korekcyjnego"
                else:
                    rate = "ZŁY - wiązka uderza w ścianki! Zmień parametry!"

                text_status = (f"Prąd solenoidu ustawiony na:        {float(arg):.1f} A\n"
                    f"Prąd solenoidu po degradacji:       {self.acc_env.active.current_solenoid:.2f} A\n"
                    f"\n"
                    f"\n"
                    f"Siła ogniskowania:                  {self.acc_env.active.focusing_force:.6f} 1/m²\n"
                    f"\n"
                    f"\n"
                    f"Odchylenie Y wiazki:                {(self.beam.position_y * 1000):.4f} mm  (cel: blisko 0)\n"
                    f"Kat trajektorii:                    {(self.beam.angle * 1000):.4f} mrad (cel: blisko 0)\n"
                    f"Cisnienie prozni:                   {self.acc_env.active.current_vacuum:.3e} Pa\n\n"
                    f"      (im wieksze odchylenie -> tym bliżej do starcenia wiązki (przegrana))\n"
                    f"      (im wiekszy kąt -> tym wiązka bardziej stara się uderzyć w ściane (przegrana))\n\n"
                    f"\n"
                    f"Obecna cała droga wiązki w LEBT:    {self.current_lebt_lenght} m"
                    f"\n"
                    f"OCENA STANU:  {rate}\n\n"
                    f"WSKAZÓWKA: Jeśli Y rośnie, zwiększ prąd solenoidu lub\n"
                    f"           dostosuj steerer (napiecie_magnesu_korekcyjnego)."
                )

                self._show_status(text_status, title="SOLENOID - WYNIK OPERACJI")
                        
                if round(self.lebt_lenght, 1) != round(self.current_lebt_lenght, 1):
                    self.acc_env.active.step_game = 0
                elif round(self.lebt_lenght, 1) == round(self.current_lebt_lenght, 1): 
                    self.acc_env.active.step_game = 1
            else:
                self._print_step_error()   

        except ValueError:
            text = "Wartość prądu musi być liczbą w przedziale [200, 300]"
            self._handling_an_exception(text)

        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd: {type(e).__name__} \n{str(e)}"
            self._handling_an_exception(text)

    def do_napiecie_magnesu_korekcyjnego(self, arg):
        '''Komenda ustawiająca napięcie magnesu korekcyjnego (sterera), by kontrolować odchylenie wiązki od środka przekroju akceleratora. \nUżycie: napiecie_magnesu_korekcyjnego <napiecie pradu w Voltach [V]>'''
        try:
            self.prev_current = self.beam.current or 0.0
            self.prev_position_y = self.beam.position_y or 0.0
            self.prev_angle = self.beam.angle or 0.0
            if self.acc_env.active.step_game == 0:    
                self.acc_env.active.steerer_voltage = float(arg)
                if not (-50 <= self.acc_env.active.steerer_voltage <= 50) :
                    raise ValueError
                
                remaining_distance = self.lebt_lenght - self.current_lebt_lenght
                self.acc_env.active.dx = random.uniform(0.10, 0.28)
                if self.acc_env.active.dx >= remaining_distance:
                    self.acc_env.active.dx = remaining_distance
                self.acc_env.active.path_length += self.acc_env.active.dx
                self.current_lebt_lenght += self.acc_env.active.dx


                self.acc_env.active.focusing_force = self.accelerator.lebt_calculate_solenoid_focus(self.acc_env.active.current_solenoid, self.beam.energy)
                self.acc_env.active.current_solenoid, self.acc_env.active.current_vacuum = self.accelerator.lebt_process_automatic_step(self.beam, self.acc_env.active.current_solenoid, self.acc_env.active.current_vacuum, self.acc_env.active.steerer_voltage, self.acc_env.active.dx)

                delta_y = (self.beam.position_y*1000) - (self.prev_position_y*1000)
                direction_change = "wiązka przesuneła sie w górę (+Y)" if delta_y > 0 else "wiązka przesuneła się w dół (-Y)"
                
                if abs(self.prev_position_y) < abs(self.beam.position_y):
                    rate = "POPRAWA - wiązka blizej osi"
                elif abs(delta_y) < 0.001:
                    rate = "BRAK ZMIAN - wiązka juz w pobliżu osi lub prąd solenoidu=0"
                else:
                    rate = "POGORSZENIE - wiązka bardziej odchylona. Spróbuj odwrotnego znaku."

                text_status = (
                f"Napięcie steerera ustawione na:     {float(arg):+.1f} V\n"
                f"\n"
                f"Odchylenie Y PRZED:                 {(self.prev_position_y*1000):+.4f} mm\n"
                f"Odchylenie Y PO:                    {(self.beam.position_y*1000):+.4f} mm\n"
                f"Zmiana:                             {delta_y:+.4f} mm  ({direction_change})\n"
                f"Kąt trajektorii:                    {self.beam.angle * 1000:.4f} mrad\n"
                f"\n"
                f"Obecna cała droga wiązki w LEBT:    {self.current_lebt_lenght} m"
                f"\n"
                f"OCENA:    {rate}\n\n"
                f"WSKAZÓWKA: Cel to Y jak najblizej 0 mm.\n"
                f"           Jesli Y jest dodatni -> uzyj ujemnego napiecia.\n"
                f"           Jesli Y jest ujemny -> uzyj ujemnego napiecia."
                )
                self._show_status(text_status, title="STEERER - WYNIK OPERACJI")

                if round(self.lebt_lenght, 1) != round(self.current_lebt_lenght, 1):
                    self.acc_env.active.step_game = 0
                elif round(self.lebt_lenght, 1) == round(self.current_lebt_lenght, 1): 
                    self.acc_env.active.step_game = 1
            else:
                self._print_step_error()
        
        except ValueError:
            text = "Wartość napięcia musi być liczbą należącą do przedziału [-50, 50] V."
            self._handling_an_exception(text)

        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd: {type(e).__name__} \n{str(e)}"
            self._handling_an_exception(text)
    
    def do_pompa_prozni(self, arg):
        '''Komenda włacza pompę, która odpompowuje gaz tworząc próżnie. \nUżycie: pompa_prozni <on/off>'''
        try: 
            self.prev_vacuum = self.acc_env.active.current_vacuum or 0.0
            if self.acc_env.active.step_game == 0:
                if arg == "on":
                    self.acc_env.active.pomp_vacuum_status = True
                elif arg == "off":
                    self.acc_env.active.pomp_vacuum_status = False
                else: 
                    raise ValueError

                self.acc_env.active.current_vacuum = self.accelerator.lebt_calculate_vacuum(self.acc_env.active.pomp_vacuum_status, self.acc_env.active.current_vacuum)
                
                self.acc_env.active.focusing_force = self.accelerator.lebt_calculate_solenoid_focus(self.acc_env.active.current_solenoid, self.beam.energy)
                self.acc_env.active.current_solenoid, self.acc_env.active.current_vacuum = self.accelerator.lebt_process_automatic_step(self.beam, self.acc_env.active.current_solenoid, self.acc_env.active.current_vacuum, self.acc_env.active.steerer_voltage, self.acc_env.active.dx)

                # Ocena ciśnienia
                if self.acc_env.active.current_vacuum < 1e-4:
                    rate = "DOSKONAŁA - bezpieczny transport wiązki"
                elif  self.acc_env.active.current_vacuum < 1e-3:
                    rate = "WYSTARCZAJĄCA - można próbować, będą straty"
                else:
                    rate = "ZŁA - zbyt dużo gazu! Wiązka zostanie zniszczona!"

                text_status = (
                    f"Pompa próżniowa:                    {arg}\n"
                    f"\n"
                    f"Ciśnienie PRZED:                    {self.prev_vacuum:.3e} Pa\n"
                    f"Ciśnienie PO:                       {self.acc_env.active.current_vacuum:.3e} Pa\n"
                    f"\n"
                    f"Poziomy odniesienia:\n"
                    f"      Atmosfera:                    1013 Pa   (powietrze w pokoju)\n"
                    f"      Zla proznia:                  > 1E-3 Pa (za duzo gazu!)\n"
                    f"      Cel LEBT:                     < 1E-4 Pa (jony moga przejsc)\n"
                    f"      Idealna:                      ~ 1E-6 Pa (CERN operacyjne)\n"
                    f"\n"
                    f"Całkowita droga wiązki w LEBT:      {self.current_lebt_lenght} m"
                    f"\n"
                    f"OCENA:    {rate}\n\n"
                    f"WSKAZOWKA: Wywołaj 'pompa_prozni on' wielokrotnie aż\n"
                    f"           ciśnienie spadnie ponizej 1E-4 Pa."
                )
                self._show_status(text_status, title="POMPA PRÓŻNI - WYNIK OPERACJI")
                self.acc_env.active.step_game == 1
                
                if round(self.lebt_lenght, 1) != round(self.current_lebt_lenght, 1):
                    self.acc_env.active.step_game = 0
                elif round(self.lebt_lenght, 1) == round(self.current_lebt_lenght, 1): 
                    self.acc_env.active.step_game = 1
            else:
                self._print_step_error()

        except ValueError:
            text = "Wartość logiczna działania pompy została podana nieprawidłowo! Dostepne wartości to: <on/off>."
            self._handling_an_exception(text)

        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd: {type(e).__name__} \n{str(e)}"
            self._handling_an_exception(text)

        #sprawdza czy można przejść do kolejnej części symulatora
    def do_gotowe(self, arg):
        try:
            if self.acc_env.active.step_game == 1: 
                a = self.acc_env.active  
                text_status = (
                f"Całkowita droga wiązki:               {self.acc_env.active.path_length} m \n"
                f"\n"
                f"Odchylenie Y wiazki:                  {(self.beam.position_y * 1000):.4f} mm  (cel: blisko 0)\n"
                f"Kat trajektorii:                      {(self.beam.angle * 1000):.4f} mrad (cel: blisko 0)\n"
                f"Cisnienie prozni:                     {self.acc_env.active.current_vacuum:.3e} Pa\n"
                f"\n"
                f"Napięcie steerera ustawione na:       {self.acc_env.active.steerer_voltage:+.1f} V\n"
                f"Prąd solenoidu:                       {self.acc_env.active.current_solenoid:.2f} A\n"
                f"Siła ogniskowania:                    {self.acc_env.active.focusing_force:.6f} 1/m²\n"
                )
                self.do_clear("")
                self._show_status(text_status,  title="RAPORT Z ODCINKA LEBT W LINAC4")
                self.do_status_wiazki("")
                self._set_stage(self.acc_env)
                time.sleep(5)
                self.do_exit("")
                return True
            else: 
                text="Nie można przejśc do kolejnej części akcelartora! \nWiązka nie dotarła jescze do końca LEBT!"
                self._handling_an_exception(text)        

        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd:{type(e).__name__} \n{str(e)}"
            self._handling_an_exception(text)

#Rzeczy, które się wykonają kiedy użytkownik odpali ten plik w konsoli
if __name__ == "__main__":
    print("Jesteś w pliku commands!")
   