"""
+=======================================+
ZAIMPORTOWANIE: 
a) bibliotek:
        time - opóźnianie procesów w terminalu
b) plików/funkcjonalności z innych plików
        utils - import stylów
        object - import obiektów
        physics - import mechanik fizycznych i obiektów   
+=======================================+
"""

import time

from commands import *
from utils import Console_clear, Print_title_screen
from objects import User, Beam
from physics import Linac4, PhysicalConstants, Electron, Proton, Hydrogen, Hydride_ion

#Funkcja główna - odpowiadająca za działanie programu w konsoli
def main():
    #zdefiniowanie obiektów potrzebnych do działania programu
    player = User()
    login = AuthorizationPanel(player)
    l4 = Linac4(PhysicalConstants(), Electron(), Proton(), Hydrogen(), Hydride_ion())
    beam = Beam()
    panel = ControlPanel(l4, beam)
    
    #wyświetlenie ekranu tytułowego
    Console_clear()
    Print_title_screen()
    
    #wyświetlenie cmd odpowiedzialnego za autoryzacje
    Console_clear()
    login.cmdloop()
    time.sleep(2)
    
    #wyświetlenie cmd odpowiedzialnego za sterowanie Linac4
    Console_clear()
    panel.cmdloop()
    
    #wyświetlenie raportu na temat wiązki
    Console_clear()
    print(f"Energia wiązki {beam.energy}")
    print(f"Prąd w wiązce {beam.current}") 
    print(f"ilość jonów w wiązce tak zwana koncentracja jonów {beam.N_Intensity}") 
    print(f"emitacja wiązki {beam.epsilon}")

#Uruchomienie programu
if __name__ == "__main__":
    main()