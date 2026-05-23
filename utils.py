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
    help = convert_hex_to_ansii("#087C1F")
    help2 = convert_hex_to_ansii("#0CDA32")


    map_background_color = "#CAECF3"

    map_controllable_beam_color = "#6114D4"
    map_automated_beam_color = "#BE87F4"

    map_controllable_beam_thickness = 18
    map_automated_beam_thickness = 18

    map_linac4_color =  "#6C14E6"
    map_bst_color = "#136A8C"
    map_ps_color = "#3EE692"
    map_sps_color = "#AF19E2"
    map_lhc_color = "#0009F4"
    map_detectors_color = "#D31172"
    map_trn_line_color = "#888B8C"

    map_linac4_thickness =  6
    map_bst_thickness = 5
    map_ps_thickness =  5
    map_sps_thickness = 7
    map_lhc_thickness = 8
    map_trn_line_thickness = 4

'''
+=======================================+
PRZYDATNE FUNKCJE
+=======================================+
'''      

#Funkcja służąca czyszczeniu 
def Console_clear():
    if os.name == 'nt':
        os.system('cls')  
    else:
        os.system('clear')

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
    #uzyskanie szerokości terminala
    console_width=os.get_terminal_size().columns

    #zmiana wielkości okna, zabezpieczenie przed zepsuciem napisu
    if console_width <= 111:
        if os.name == 'nt':
            os.system('mode con: cols=112 lines=12')
        else:
            os.system(r"printf '\e[8;12;112t'")
    
    console_width=os.get_terminal_size().columns
    
    #zapobiegnięcie przed duża wartością paska (wiekszą niż rozmiar konsoli)
    lenght_bar = min(lenght_bar, (console_width-20))
    
    #lista z ilością spacji dla każdego elementu
    spaces_count = [int((console_width-104)/2), int((console_width-4)/2), int((console_width-lenght_bar)/2)]
    
    #podzielenia i wypisanie loga
    lines = logo.split('\n')
    for i in lines:
        print(" " * spaces_count[0] + i)
    
    #ustawienie specjalnego formatowania dla paska i ukrycie kursora w konsoli
    print(f"\n{colors.hide_cursor}{colors.bar_color}")
    
    #utworzenie paska
    for i in range(lenght_bar + 1):
        percent = int((i / lenght_bar) * 100)
        
        blocks = "█" * i + "░" * (lenght_bar - i)
        
        #wypisywanie paska ładowania i procentów
        sys.stdout.write(f"\033[A\r"+ (" " * spaces_count[1]) + f"{percent}%")
        sys.stdout.flush()
        
        sys.stdout.write(f"\033[B\r"+ (" " * spaces_count[2]) + f"[{blocks}]")
        sys.stdout.flush()
        
        time.sleep(display_time / lenght_bar)

    time.sleep(1)
    #powrót do zwykłego formatowania i pojawienie kursora w konsoli
    print(f"{colors.clear}{colors.show_cursor}")

#Funkcja służąca jako szablon do tworzenia różnych pasków proporcjonalnych wartość/maksymalna wartość
def Create_progress_bar(current_value, min_value, max_value, lenght_bar, display_time, unit, color_target_value, color_undesired_value, color_text, prefix="", subfix=""):
    #ustalenie proporcji
    percent = current_value/max_value
    percent = min(percent, 1)
    
    #dlugość paska reprezentująca pasek zamalowany czyli posiadaną wartość
    full_length = int(percent*lenght_bar)
    
    #tworzenie paska
    for length in range(full_length + 1):
        blocks = "█" * length + "░" * (lenght_bar - length)
        
        #wypisywanie paska i danych obok niego
        if full_length > 0:
            animated_value = (length / full_length) * current_value
        else:
            animated_value = 0.0
        decimal_places =len(str(current_value).split('.')[1])
        animated_value = f"{animated_value:.{decimal_places}f}"

        if float(animated_value) <= float(min_value): 
            color_bar = color_undesired_value
        elif float(animated_value) >= float(max_value):
            color_bar=color_undesired_value
        else:
            color_bar = color_target_value
        
        sys.stdout.write(f"\r{prefix}{colors.hide_cursor}{color_bar}{blocks}{colors.clear} {color_text}{animated_value} {unit} {subfix}")
        sys.stdout.flush()

        time.sleep(display_time / lenght_bar)
    
    #czyszczenie formatowania
    print(f"{colors.clear}{colors.show_cursor}")

#Sekcja do sprawdzania wyglądu kolorów
if __name__ == "__main__":
    print(f"{colors.welcome_color_1}TO JEST TEKST TESTOWY/to jest tekst testowy")
    print(f"{colors.welcome_color_2}TO JEST TEKST TESTOWY/to jest tekst testowy")
    