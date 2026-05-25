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

from objects import AcceleratorEnvironment, Beam #TYMCZASOWE
from physics import *

#Dostęp do orgazinera stylami
style = Styling()
acc_env, beam = AcceleratorEnvironment(), Beam() 
l4 = Linac4(PhysicalConstants(), Electron(), Proton(), Hydrogen(), HydrideIon())
ion_source = NegativeIonSource(PhysicalConstants(), Electron(), Proton(), Hydrogen(), HydrideIon())
 
"""
+=======================================+
KONSOLA POLECEŃ SŁUŻĄCA DO STEROWANIA GRĄ
+=======================================+
"""
#KLasa będąca podstawą innych konsoli wykorzystywanych w programie
class FunctionalCommands(cmd.Cmd):
    def __init__(self, completekey = "tab", stdin = None, stdout = None):
        super().__init__(completekey, stdin, stdout)
        self.map_activated = False
    #Zmienne służące do wyświetlania czytelnego panelu pomocy
    HELP_TITLE = "SYSTEM POMOCY"
    HELP_SUBTITLE = "KOMENDY"
    HELP_COMMANDS = {} 
    
    #Metody biblioteki cmd, które powodują puste miejsca po wykonanej komendzie
    def precmd(self, line):
        """Wywołuje się automatycznie TUŻ PRZED każdą komendą."""
        #Odświeżanie okna turtle aby się nie zawiesiło
        if self.map_activated == True:
            try:
                turtle.update()
            except turtle.Terminator:
                pass
        print()  
        return line 
    
    def postcmd(self, stop, line):
        """Wywołuje się automatycznie PO każdej wykonanej komendzie."""
        #Odświeżanie okna turtle aby się nie zawiesiło
        if self.map_activated == True:
            try:
                turtle.update()
            except turtle.Terminator:
                pass
        print()  
        return stop
    
    def _show_status (self, text_status, bar = None, bar_next_to_text = None, title = "RAPORT PO WYKONANEJ OPERACJI", color_1 = style.color_1, color_2 = style.status_2_color):
        lenght_decoration = 80
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
    
    #Komendy systemowe tzn. nie wpływające na rozgrywkę
    def do_mapa(self, arg):
        """Wyświetla mapę ośrodka i obiekty aktywne. \nUżycie: mapa"""
        self.map_activated = True
        map_main()
    
    def do_clear(self, arg):
        """Czyści konsolę. \nUżycie: clear"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
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
        print(f"{style.bold}{style.help_color}" + "\n" + "=" * lenght_decoration)
        print(f"{self.HELP_TITLE:^{lenght_decoration}}")
        print(f"=" * lenght_decoration + f"{style.clear}")
        
        print(f"{style.help_2_color}\n[ {self.HELP_SUBTITLE} ]{style.clear}")
        for cmd_name, cmd_desc in self.HELP_COMMANDS.items():
                print(f"  {cmd_name:<25} - {cmd_desc}")
        
        print(f"{style.help_2_color}\n[ KOMENDY SYSTEMOWE ]{style.clear}")
        print(f"  {'mapa':<25} - Wyświetla mape ośrodka CERN.")
        print(f"  {'clear / cls / wyczysc':<25} - Czyszczenie ekranu konsoli.")
        print(f"  {'help':<25} - Wyświetla menu pomocy.")
        print(f"  {'exit':<25} - Zamknięcie konsoli CERN'U! Nie programu!.")
        
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
            arg_pass = input(f"{style.bold}{style.prefix_cmd}CERN_AUTORYZACJA>>> {style.clear}password ")
            self.do_password(arg_pass)
        
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

class ControlPanelIonSource(FunctionalCommands):
    #Zdefiniowanie: prefixu wykonywanych komend, krotkiego wytłumaczenia użytkonikowi do czego jest dana konsola
    prompt = f"{style.bold}{style.prefix_cmd}CERN_CMD>>>ION_SOURCE>>> {style.clear}"
    title_intro =f"{'PANEL ZARZĄDZANIA CERN - WITAJ PONOWNIE!':^80}"
    intro = f"{style.bold}{style.welcome_color_1}" + "=" * 80 + f"{style.welcome_color_2}\n{title_intro}\n" + f"{style.welcome_color_1}" + "=" * 80 + "\n\n" + f"{style.clear}{style.welcome_color_2}Etap weryfikacji dla użytkownika zakończony pomyślnie!\n\n" + "System zarządzania akceleratorami zainicjowany pomyślnie! \n\n" + "Użytkownik posiada wszystkie uprawnienia zarządzaniem akceleratorem! \n\n" + f"{style.bold}{style.welcome_color_1}" + "-" * 80 + "\n" + f"{style.clear}{style.welcome_color_2}Wpisz {style.bold}'help'{style.bold_off}, aby zobaczyć komendy.\n" + f"{style.bold}{style.welcome_color_1}" + "=" * 80 + f"{style.clear}\n\n" 
    
    def __init__(self, accelerator_environment, beam, accelerator,):
        super().__init__()
        self.acc_env = accelerator_environment
        self.accelerator = accelerator 
        self.beam = beam
    
        #zdefiniowanie w którym akceleratorze jesteśmy
        self.acc_env.set_accelerator("Negative Ion Source")

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
            self.acc_env.active.total_hydrogen_mass = self.acc_env.active.total_hydrogen_mass + (self.accelerator.I_S_calculate_mass_hydrogen(0, int(arg)))
            self.acc_env.active.n = self.accelerator.I_S_calculate_number_density(self.acc_env.active.total_hydrogen_mass)
            self.acc_env.active.p = self.accelerator.I_S_calculate_chamber_pressure(self.acc_env.active.n)
            
            text_status = f"Zawór został otwarty na {arg} mikrosekund. \nMasa wodoru wynosi: {self.acc_env.active.total_hydrogen_mass}, \nKoncentracja H2 w komorze wynosi: {self.acc_env.active.n}," 
            bar_p = lambda: Create_progress_bar(self.acc_env.active.p, 7.0, 3.0, 4.0, 20, 5, style.valid, style.errors, style.status_2_color, prefix=f"Ciśnienie w komorze wynosi: {self.acc_env.active.p:.2f} Pa ")
            self._show_status(text_status, bar=bar_p)
        except ValueError:
            text = f"Nie możesz: \n- zostawić pustego pola\n- wpisywać liter \n- podawać wielu argumentów komendzie np. otworz_zawor <argument1> <argument2> \n\nPodaj liczbę całkowitą (czas otwarcia zaworu w ms)!"
            self.handling_an_exception(text)
        
        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd: {type(e).__name__} \n{str(e)}"
            self.handling_an_exception(text)
      
    def do_moc_szczytowa_RF(self, arg):
        '''Ustawia moc szczytową fal radiowych (RF) wymaganą do zapłonu plazmy. \nUżycie: moc_szczytowa_RF <moc w kW>'''
        try: 
            self.acc_env.active.ionization_efficiency, self.acc_env.active.I_S_rf_start_power = self.accelerator.I_S_calculate_ionization_efficiency(int(arg))
            
            text_status = f"Moc szczytowa RF ustawiona na: {self.acc_env.active.I_S_rf_start_power}, \nEfektywność jonizacji wynosi {self.acc_env.active.ionization_efficiency},"
            self._show_status(text_status)
        
        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd: {type(e).__name__} \n{str(e)}"
            self.handling_an_exception(text)

    def do_moc_RF(self, arg):
        '''Ustawia moc roboczą fal radiowych (RF) potrzebną do stabilnego podtrzymania plazmy. \nUżycie: moc_RF <moc w kW>'''
        try:
            self.acc_env.active.rf_work, self.acc_env.active.I_S_rf_power = self.accelerator.I_S_calculate_RF_field_energy(self.acc_env.active.n, int(arg))
            self.acc_env.active.ne = self.accelerator.I_S_calculate_electron_density(self.acc_env.active.I_S_rf_power, self.acc_env.active.ionization_efficiency)
            
            text_status=f"Moc robocza ustawiona: {self.acc_env.active.I_S_rf_power}, \nRF dostarcza energii: {self.acc_env.active.rf_work}, \nKoncentracja jonów o identycznym ładunkuwynosi: {self.acc_env.active.ne},"
            self._show_status(text_status)
        
        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd: {type(e).__name__} \n{str(e)}"
            self.handling_an_exception(text)

    def do_temp_cezu(self, arg):
        '''Ustawia temperature na jaką piec ma grzać Cez. \nUżycie: temp_cesu <temperatura w c>'''
        try:
            self.acc_env.active.T_cez = int(arg)
            if self.acc_env.active.T_cez < 40:
                raise ValueError(
                    f"Temperatura {self.acc_env.active.T_cez}°C jest ZA NISKA!\n"
                    "Cez nie odparowuje. Brak efektywnej produkcji jonów H-."
                )

            #zwróenie błędów/informacji o nie poprawnej temperaturze
            elif self.acc_env.active.T_cez > 100:
                raise ValueError(
                    f"BŁĄD KRYTYCZNY: Temperatura {self.acc_env.active.T_cez}°C jest ZA WYSOKA!\n"
                    "Gwałtowny wyrzut cezu wywołał przebicie elektryczne na elektrodach 45 kV."
                )

            elif 80 < self.acc_env.active.T_cez <= 100:
                print(f"OSTRZEŻENIE: Temperatura {self.acc_env.active.T_cez}°C przekracza normę operacyjną. Wydajność źródła drastecznie spada.!")


            else:
                print(f"STATUS: Temperatura {self.acc_env.active.T_cez}°C w normie. Stabilna praca źródła.")
            self.beam.current = self.accelerator.I_S_calculate__beam_current(self.acc_env.active.T_cez, self.acc_env.active.ne)
            self.beam.N_Intensity = self.accelerator.I_S_calculate_beam_intensity(self.beam.current)
            self.beam.epsilon = self.accelerator.I_S_calculate_beam_emittance()    
        
        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd:{type(e).__name__} \n{str(e)}"
            self.handling_an_exception(text)

class ControlPanelLinac4(FunctionalCommands):
    #Zdefiniowanie: prefixu wykonywanych komend, krotkiego wytłumaczenia uzżytkonikowi do czego jest dana konsola
    prompt = f"{style.bold}{style.prefix_cmd}CERN_CMD>>>Linac4>>> {style.clear}"
    title_intro =f"{'PANEL ZARZĄDZANIA CERN - Linac4':^80}"
    intro = f"{style.bold}{style.welcome_color_1}" + "=" * 80 + f"{style.welcome_color_2}\n{title_intro}\n" + f"{style.welcome_color_1}" + "=" * 80 + "\n\n" + f"{style.clear}{style.welcome_color_2}" + f"{'Obecnie zarządzasz akceleratorem Linac!':^80}" + f"{style.bold}{style.welcome_color_1}" + "\n" +"-" * 80 + "\n" + f"{style.clear}{style.welcome_color_2}Wpisz {style.bold}'help'{style.bold_off}, aby zobaczyć komendy.\n" + f"{style.bold}{style.welcome_color_1}" + "=" * 80 + f"{style.clear}\n\n" 
    
    def __init__(self, accelerator_environment, beam, accelerator,):
        super().__init__()
        self.acc_env = accelerator_environment
        self.accelerator = accelerator 
        self.beam = beam

        #zdefiniowanie w którym akceleratorze jesteśmy
        self.acc_env.set_accelerator("Linac4")
        #kopia parametrów z poprzedniego akceleratora na obecny
        self.acc_env.copy_data("Negative Ion Source", "Linac4")

    #Zmienne służące do wyświetlania czytelnego panelu pomocy
    HELP_TITLE = "PANEL ZARZĄDZANIA LINAC4 - SYSTEM POMOCY"
    HELP_SUBTITLE = "KOMENDY ZARZĄDZANIA"
    HELP_COMMANDS = {
        "status_wiazki": "Wyświetla informacje o stanie wiązki.",
        "prad_solenoidu": "Ustawia prąd przepływający przez solenoid.",
        "napiecie_magnesu_korekcyjnego": "Ustawia napięcie magnesu korekcyjnego (sterera).",
        "pompa_prozni": "Włacza pompę, która odpompowuje gaz tworząc próżnie.",
    }
    
    def do_status_wiazki(self, arg):
        """Komenda wyświetla zaawansowany raport o stanie wiązki. \nUżycie: status_wiazki""" 
        raport = (
            f"{"Pozycja X (długość w tunelu):":<40} {self.beam.position_x} m\n"
            f"{"Pozycja Y (poprzeczne odchylenie):":<40} {self.beam.position_y} mm\n"
            f"{"Kąt (nachylenie trajektorii):":<40} {self.beam.angle} °\n"
            "\n"
            f"{"Energia kinetyczna:":<40} {self.beam.energy} MeV\n"
            f"{"Rozrzut energii:":<40} {self.beam.energy_spread} %\n"
            f"{"Prędkość światła:":<40} {self.beam.percent_light_speed} % c\n"
            "\n"
            f"{"Prąd:":<40} {self.beam.current} mA\n"
            f"{"Koncentracja cząsteczek:":<40} {self.beam.N_Intensity} 1/m3\n"
            "\n"
            f"{"Emitancja:":<40} {self.beam.epsilon} mm*mrad\n"
            f"{"Świetlność:":<40} {self.beam.luminosity_potential} %\n"
            f"{"Profil (promień wiązki) (x, y):":<40} {self.beam.profile} mm\n"
            "\n"
            f"{"Faza pola RF:":<40} {self.beam.RF_phase} \n"
            f"{"Struktura wiązki:":<40} {self.beam.bunch_structure} \n"
        )
         
        # Wywołanie wyświetlenia na ekranie
        self._show_status(raport, title="OBECNY STAN WIĄZKI")



    #Komendy wpływające na rozgrywkę:

    def do_prad_solenoidu(self, arg):
        '''Komenda ustawiająca prąd przepływający przez solenoid, aby skupiać wiązkę anionów wodoru. \nUżycie: prad_solenoidu <nateżenie pradu w Amperach [A]>'''
        try: 
            self.acc_env.active.current_solenoid = float(arg)
            
            self.acc_env.active.dx = random.uniform(0.10, 0.28)

            self.acc_env.active.focusing_force = self.accelerator.lebt_calculate_solenoid_focus(self.acc_env.active.current_solenoid, self.beam.energy)
            self.acc_env.active.current_solenoid, self.acc_env.active.current_vacuum = self.accelerator.lebt_process_automatic_step(self.beam, self.acc_env.active.current_solenoid, self.acc_env.active.current_vacuum, self.acc_env.active.steerer_voltage, self.acc_env.active.dx)

            text_status = f"Prąd przepływający przez solenoid ustawiony na: {arg}, \nPrąd przepływający przez solenoid wynosi obecnie: {self.acc_env.active.current_solenoid}, \nSiła ogniskowania wiązki wynosi: {self.acc_env.active.focusing_force}, \nCiśnienie w próżni wynosi: {self.acc_env.active.current_vacuum}, "
            self._show_status(text_status)
        
        except ValueError:
            text = "Wartość prądu musi być liczbą (np. prad_solenoidu 240)."
            self.handling_an_exception(text)

        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd: {type(e).__name__} \n{str(e)}"
            self.handling_an_exception(text)

    def do_napiecie_magnesu_korekcyjnego(self, arg):
        '''Komenda ustawiająca napięcie magnesu korekcyjnego (sterera), by kontrolować odchylenie wiązki od środka przekroju akceleratora. \nUżycie: napiecie_magnesu_korekcyjnego <napiecie pradu w Voltach [V]>'''
        try: 
            self.acc_env.active.steerer_voltage = float(arg)
            
            self.acc_env.active.dx = random.uniform(0.10, 0.28)

            self.acc_env.active.focusing_force = self.accelerator.lebt_calculate_solenoid_focus(self.acc_env.active.current_solenoid, self.beam.energy)
            self.acc_env.active.current_solenoid, self.acc_env.active.current_vacuum = self.accelerator.lebt_process_automatic_step(self.beam, self.acc_env.active.current_solenoid, self.acc_env.active.current_vacuum, self.acc_env.active.steerer_voltage, self.acc_env.active.dx)

            text_status = f"Napięcie na magnesie korekcyjnym ustawione na: {arg}, \nPrąd przepływający przez solenoid wynosi obecnie: {self.acc_env.active.current_solenoid}, \nSiła ogniskowania wiązki wynosi: {self.acc_env.active.focusing_force}, \nCiśnienie w próżni wynosi: {self.acc_env.active.current_vacuum}, "
            self._show_status(text_status)
        
        except ValueError:
            text = "Wartość napięcia musi być liczbą (np. napiecie_magnesu_korekcyjnego 240)."
            self.handling_an_exception(text)

        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd: {type(e).__name__} \n{str(e)}"
            self.handling_an_exception(text)
    
    def do_pompa_prozni(self, arg):
        '''Komenda włacza pompę, która odpompowuje gaz tworząc próżnie. \nUżycie: pompa_prozni <on/off>'''
        try: 
            if arg == "on":
                self.acc_env.active.pomp_vacuum_status = True
            elif arg == "off":
                self.acc_env.active.pomp_vacuum_status = False
            else: 
               raise ValueError
                
            
            self.acc_env.active.current_vacuum = self.accelerator.lebt_calculate_vacuum(self.acc_env.active.pomp_vacuum_status, self.acc_env.active.current_vacuum)
            
            self.acc_env.active.focusing_force = self.accelerator.lebt_calculate_solenoid_focus(self.acc_env.active.current_solenoid, self.beam.energy)
            self.acc_env.active.current_solenoid, self.acc_env.active.current_vacuum = self.accelerator.lebt_process_automatic_step(self.beam, self.acc_env.active.current_solenoid, self.acc_env.active.current_vacuum, self.acc_env.active.steerer_voltage, self.acc_env.active.dx)

            text_status = f"Status pompy: {arg}, \nPrąd przepływający przez solenoid wynosi obecnie: {self.acc_env.active.current_solenoid}, \nSiła ogniskowania wiązki wynosi: {self.acc_env.active.focusing_force}, \nCiśnienie w próżni wynosi: {self.acc_env.active.current_vacuum}, "
            self._show_status(text_status)
        
        except ValueError:
            text = "Wartość logiczna działania pompy została podana nieprawidłowo! Dostepne wartości to: <on/off>."
            self.handling_an_exception(text)

        except Exception as e:
            text = f"Wykonując komendę system napotkał błąd: {type(e).__name__} \n{str(e)}"
            self.handling_an_exception(text)

#Rzeczy, które się wykonają kiedy użytkownik odpali ten plik w konsoli
if __name__ == "__main__":
    print("Jesteś w pliku commands!")
    panel1=ControlPanelIonSource(acc_env, beam, ion_source)
    panel1.cmdloop()
    panel=ControlPanelLinac4(acc_env, beam, l4)
    panel.cmdloop()
    