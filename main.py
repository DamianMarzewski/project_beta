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
from physics import NegativeIonSource, PhysicalConstants, Electron, Proton, Hydrogen, HydrideIon

#Funkcja główna - odpowiadająca za działanie programu w konsoli
def main():
    #zdefiniowanie obiektów potrzebnych do działania programu
    player = User()
    login = AuthorizationPanel(player)
    ion_source = NegativeIonSource(PhysicalConstants(), Electron(), Proton(), Hydrogen(), HydrideIon())
    l4 = Linac4(PhysicalConstants(), Electron(), Proton(), Hydrogen(), HydrideIon())
    acc_env, beam = AcceleratorEnvironment(), Beam() 
    panel_ion_source = ControlPanelIonSource(acc_env, beam, ion_source)
    panel_l4 = ControlPanelLinac4(acc_env, beam, l4)
    
    #wyświetlenie ekranu tytułowego
    Console_clear()
    Print_title_screen()
    
    #wyświetlenie cmd odpowiedzialnego za autoryzacje
    Console_clear()
    login.cmdloop()
    time.sleep(2)

    #wyświetlenie cmd odpowiedzialnego za sterowanie Linac4
    Console_clear()
    panel_ion_source.cmdloop()

    #wyświetlenie cmd odpowiedzialnego za sterowanie Linac4
    Console_clear()
    panel_l4.cmdloop()
    
    #wyświetlenie raportu na temat wiązki
    Console_clear()
    panel_l4.do_status_wiazki()

#Uruchomienie programu
if __name__ == "__main__":
    main()