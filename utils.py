"""
+=======================================+
ZAIMPORTOWANIE: 
a) bibliotek:
        os - możliwość używania funkcjonalności systemu operacyjnego komputera
        sys - możliwosć niskopoziomowego sterowanie tekstem
        time - opóźnianie procesów w terminalu
+=======================================+
"""
import os
import sys
import time


class Styling:
    #Metoda przekonwertująca kolor HEX na formatowanie ANSII
    def convert_hex_to_ansii(hex_color):
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"\033[38;2;{r};{g};{b}m"
    
    #Restart formatu ANSII
    clear = "\033[0m"
    
    #Zarządzanie pojawianiem się kursora w konsoli
    hide_cursor = "\033[?25l"
    show_cursor = "\033[?25h"

    #Formatowanie tekstu ANSII
    bold = "\033[1m"
    bold_off = "\033[22m"
    cursive = "\033[3m"
    underline = "\033[4m"
    pulse = "\033[5m"
    strike = "\033[9m"
    
    #Kolory zdefiniowane w postaci formatowania ANSII
    title_game_color1 = convert_hex_to_ansii("#1A44AD")
    title_game_color2= convert_hex_to_ansii("#F09B08")
    bar_color = convert_hex_to_ansii("#FFF75A")
    
    welcome_color_1 = convert_hex_to_ansii("#5293F4")
    welcome_color_2 = convert_hex_to_ansii("#3DD0DE")

    prefix_cmd = convert_hex_to_ansii("#1648C6")
    
    errors = convert_hex_to_ansii("#B11616")
    valid = convert_hex_to_ansii("#15A817")
    help_color = convert_hex_to_ansii("#087C1F")
    help_2_color = convert_hex_to_ansii("#0CDA32")

    color_1 = convert_hex_to_ansii("#0BCDCD")
    status_2_color = convert_hex_to_ansii("#76FBFB")

    map_background_color = "#CAECF3"

    map_controllable_beam_color = "#6114D4"
    map_automated_beam_color = "#BE87F4"

    map_controllable_beam_thickness = 18
    map_automated_beam_thickness = 18

    map_linac4_color =  "#D01010"
    map_bst_color = "#E09808"
    map_ps_color = "#F5F906"
    map_sps_color = "#18C91B"
    map_lhc_color = "#003DF4"
    map_detectors_color = "#9211D3"
    map_trn_line_color = "#7B8183"

    map_linac4_thickness =  6
    map_bst_thickness = 5
    map_ps_thickness =  5
    map_sps_thickness = 7
    map_lhc_thickness = 8
    map_trn_line_thickness = 4

    background_detectors_thickness = 40
    detectors_thickness = 30
    text_thickness = 12

'''
+=======================================+
PRZYDATNE FUNKCJE
+=======================================+
'''      

#Funkcja służąca czyszczeniu 
def Console_clear():
    os.system('cls' if os.name == 'nt' else 'clear')

'''
+=======================================+
FUNKCJE SŁUŻĄCE DO UPIĘKSZENIA UI
+=======================================+
'''
#Zdefiniowanie klasy
colors = Styling()

#Funkcja służąca do wyświetlania ekranu tytułowego
def Print_title_screen(display_time=8, lenght_bar=106):
    logo=fr'''{colors.bold}
{colors.title_game_color1}  _____ ______ _____  _   _       {colors.title_game_color2} __  __ _____  _____      _            _    _ _____ _____  _____  _____ 
{colors.title_game_color1} / ____|  ____|  __ \| \ | |  _   {colors.title_game_color2}|  \/  |_   _|/ ____|    | |  /\      | |  | |_   _/ ____|/ ____|/ ____|
{colors.title_game_color1}| |    | |__  | |__) |  \| | (_)  {colors.title_game_color2}| \  / | | | | (___      | | /  \     | |__| | | || |  __| |  __| (___  
{colors.title_game_color1}| |    |  __| |  _  /| . ` |      {colors.title_game_color2}| |\/| | | |  \___ \ _   | |/ /\ \    |  __  | | || | |_ | | |_ |\___ \ 
{colors.title_game_color1}| |____| |____| | \ \| |\  |  _   {colors.title_game_color2}| |  | |_| |_ ____) | |__| / ____ \   | |  | |_| || |__| | |__| |____) |
{colors.title_game_color1} \_____|______|_|  \_\_| \_| (_)  {colors.title_game_color2}|_|  |_|_____|_____/ \____/_/    \_\  |_|  |_|_____\_____|\_____|_____/ {colors.clear}
'''
    #pod funkcja rysująca klatki
    def print_frame(i, max_bar_lenght, clear=False):
        
        if clear:
            Console_clear() 
        else:
            sys.stdout.write("\033[H")  
            sys.stdout.flush()
        
        
        current_console_width = os.get_terminal_size().columns

        spaces_count = [int((current_console_width-104)/2), int((current_console_width-4)/2), int((current_console_width-lenght_bar)/2), int((current_console_width-17)/2), int((current_console_width - 40)/2)]
        
        if current_console_width >= 111:
           
            lines = logo.split('\n')
            for line in lines:
                if line.strip():  # Pomija puste linie na końcach
                    print(" " * spaces_count[0] + line)
            
            #wypisanie paska ładowania
            percent = int((i / max_bar_lenght) * 100)
            blocks = "█" * i + "░" * (max_bar_lenght - i)

            sys.stdout.write(f"\n{colors.bar_color}\033[K\n")
            sys.stdout.write(" " * spaces_count[1] + f"{percent}%\033[K\n")
            sys.stdout.write(" " * spaces_count[2] + f"[{blocks}]{colors.clear}\033[K\n")
        else:
            #wypisywanie dla zbyt małego okna
            percent = int((i / max_bar_lenght) * 100)
            print(f"{colors.bar_color}\n" * 2)
            print(" " * spaces_count[3] + "CERN: MISJA HIGGS\n")
            print(" " * spaces_count[1] + f"{percent}%")
            print(f"{colors.errors}\n" + " " * spaces_count[4] + "(Okno jest za małe, rozszerz je myszką!)")

    console_width = os.get_terminal_size().columns

    #zabezpieczenie przed zbyt małym rozmiarem
    if console_width <= 111:
        if os.name == 'nt':
            os.system('mode con: cols=112 lines=14')
        else:
            sys.stdout.write(r"\e[8;14;112t")
            sys.stdout.flush()
        
        time.sleep(0.1) 
        
        console_width = os.get_terminal_size().columns

    #obliczenie ostatecznej długości paska
    lenght_bar = min(lenght_bar, (console_width - 20))
    if lenght_bar < 10: lenght_bar = 10 # Zabezpieczenie przed ujemną długością

    #ukrycie kursora na początku wyrysowaniu
    sys.stdout.write(colors.hide_cursor) 

    previous_console_width = console_width

    #pętla tworząca animacje paska
    for i in range(lenght_bar + 1):
        console_width = os.get_terminal_size().columns
        clear = False
        #sprawdzanie czy nie doszło do zmiany rozmiarów okna
        if console_width != previous_console_width:
            clear = True
            # Dopasowujemy długość paska do nowych wymiarów okna, żeby nie wyszedł poza ekran
            lenght_bar = min(106, (console_width - 20))
            if lenght_bar < 10: lenght_bar = 10
            previous_console_width = console_width
        
        print_frame(min(i, lenght_bar), lenght_bar, clear=clear)

        time.sleep(display_time / lenght_bar)

    time.sleep(1)
    #przywrócenie kursora i czyszczenie formatowania
    sys.stdout.write(f"{colors.clear}{colors.show_cursor}")
    Console_clear()

#Funkcja służąca jako szablon do tworzenia różnych pasków proporcjonalnych wartość/maksymalna wartość
def Create_progress_bar(current_value, total_value, min_value, max_value, lenght_bar, display_time, color_target_value, color_undesired_value, color_text=colors.prefix_cmd,  prefix="", subfix="", print_value = False, unit=""):
    #ustalenie proporcji
    percent = current_value/total_value
    percent = min(percent, 1)
    
    #dlugość paska reprezentująca pasek zamalowany czyli posiadaną wartość
    full_length = max(int(percent*lenght_bar), 1)
    
    #tworzenie paska
    for length in range(full_length + 1):
        blocks = "█" * length + "░" * (lenght_bar - length)
        
        if full_length > 0:
            animated_value = (length / full_length) * current_value
        else:
            animated_value = 0.0
        if float(animated_value) <= float(min_value): 
            color_bar = color_undesired_value
        elif float(animated_value) >= float(max_value):
            color_bar=color_undesired_value
        else:
            color_bar = color_target_value
        
        if print_value == False:
            sys.stdout.write(f"\r{prefix}{colors.hide_cursor}{color_bar}{blocks}{colors.clear} {color_text} {subfix}")
            sys.stdout.flush()
        
        elif print_value == True:
            decimal_places = len(str(current_value).split('.')[1])
            animated_value = f"{animated_value:.{decimal_places}f}"

            sys.stdout.write(f"\r{prefix}{colors.hide_cursor}{color_bar}{blocks}{colors.clear} {color_text}{animated_value} {unit} {subfix}")
            sys.stdout.flush()
        
        else:
            raise ValueError ("Żle wpisałeś wartość print_value")
        
        time.sleep(display_time / lenght_bar)
    
    #czyszczenie formatowania
    print(f"{colors.clear}{colors.show_cursor}")

#Sekcja do sprawdzania wyglądu kolorów
if __name__ == "__main__":
    print(f"{colors.welcome_color_1}TO JEST TEKST TESTOWY/to jest tekst testowy")
    print(f"{colors.welcome_color_2}TO JEST TEKST TESTOWY/to jest tekst testowy")

logo=222
    