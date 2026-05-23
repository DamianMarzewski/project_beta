"""
+=======================================+
ZAIMPORTOWANIE: 
a) bibliotek:
        math - możliwość korzystania z bardziej zaawansowanej matematyki
+=======================================+
"""

import math

#Klasa stałych fizycznych - definiuje najważniejsze stałe potrzebne do wyliczeń
class PhysicalConstants():
    def __init__(self):
        self.SPEED_OF_LIGHT = 299792458 # [m/s]
        self.BOLTZMANN_CONSTANT = 1.380649E-23 # [J/K]
        self.AVOGARD_CONSTANT = 6.022E23 #[1/mol]

#Klasa elektronu - definiuje stałe dla tego obiektu
class Electron():
    def __init__(self):
        self.rest_mass_kg = 9.109E-31 #[kg]
        self.rest_mass_mev = 0.511 # [MeV/c^2]
        self.charge = -1.602176634E-19 #[C]

#Klasa protonu - definiuje stałe dla tego obiektu
class Proton():
    def __init__(self):
        self.rest_mass_kg = 1.67E-27 #[kg]
        self.rest_mass_mev = 938.27 #[MeV/c^2]
        self.charge = 1.602E-19 #[C]

#Klasa wodoru - definiuje stałe dla tego obiektu
class Hydrogen():
    def __init__(self):
        self.atom_rest_mass_kg = 1.6737236E-27 #[kg]
        self.atom_rest_mass_mev = 938.783  # [MeV/c^2]

        self.molecular_rest_mass_kg = 2 * self.atom_rest_mass_kg #[kg] 
        self.molecular_rest_mass_mev = 2 * self.atom_rest_mass_mev #[mev/c^2]
        
        self.atom_molar_mass = 1.008E-3 #[kg/mol] #masa molowa jednego atomu wodoru (H)
        self.molecular_molar_mass = 2.016E-3 #[kg/mol] # masa molowa H2

        self.molecular_diameter = 2.89E-10 #[m] #efektywna średnica cząsteczki wodoru (H2)


#Klasa anionu wodoru - definiuje stałe dla tego obiektu
class Hydride_ion():
    def __init__(self):
        self.rest_mass_kg = 1.674278E-27 #[kg]
        self.rest_mass_mev = 939.294 #[mev/c^2]
        self.charge = -1.602176634E-19 #[C]
        self.binding_energy_ev = 0.754 #[eV]
        self.max_safe_magnetic_field = 0.3 #[T]
        
#Klasa odcinka w systemie akceleartorów (butla z H2 -> koniec Linac4) - zawiera wszystkie metody fizyczne dla tego odcinka
class Linac4():

    def __init__(self, PhysicalConstants, Electron, Proton, Hydrogen, Hydride_ion):
        #zdefiniowanie obiektów
        self.PhysicalConstants = PhysicalConstants
        self.Electron = Electron
        self.Proton = Proton
        self.Hydrogen = Hydrogen
        self.Hydride_ion = Hydride_ion
        
        #cała długość odcinka (butla z H2 -> koniec Linac4)
        self.overall_length = None #[m]
        
        #ION Source
        self.HYDROGEN_FLOW_RATE = 8.7E-7 #[kg/s] #natężenie wodoru z zaworu piezoelektrycznego
        self.I_S_CHAMBER_VOLUME = 2.46E-4 #[m^3] #objętość komory
        self.I_S_CHAMBER_TEMPERATURE = 300 #[K] #temperatura w komorze
        self.I_S_EXTRACTION_ELECTRODE_VOLTAGE = 4.5E4 #[V] #siła, z jaką zasilacz w CERN ciągnie jony z komory ION Source
        self.I_S_AP_AREA_CS = 174e-6 #[m^2] #rzeczywista powierzchnia cezowa wewnątrz komory na której zachodzi jonizacja
        self.I_S_AP_RADIUS = 3.25E-3 #[m] #promień otworu wylotowego
        self.I_S_hole_area = math.pi * (self.I_S_AP_RADIUS ** 2) #[m^2] #powierzchnia otworu, z którego wypływają cząsteczki

        #stałe wodoru
        self.hydrogen_v_avg = math.sqrt((2 * self.PhysicalConstants.BOLTZMANN_CONSTANT * self.I_S_CHAMBER_TEMPERATURE) / self.Hydrogen.molecular_rest_mass_kg) #[m/s]

        #stałe anionu wodoru
        self.I_S_ION_TEMPERATURE = 1.0 #[eV] #temperatura jonu wodoru wzięta z dokumentacji CERN
        self.hydride_v_term = math.sqrt((2 * self.I_S_ION_TEMPERATURE * abs(self.Electron.charge)) / (self.Hydride_ion.rest_mass_kg)) #[m/s] #najprawdopodobniejsza prędkość jonów wodoru
        
    """
    -+/=============================================================/+-
        ION Source - Wszsytkie metody dątyczące tego odcinka Linac4
    -+/=============================================================/+-
    """

    #Metoda wyliczająca mase wszystkich cząsteczek wodoru znajdującego się w komorze ION Source
    def I_S_calculate_mass_hydrogen(self, previous_mass, time_us):
        if 200 < time_us < 500:
            time_s = time_us*1e-6 #[us] #zmiana jednostki: us -> s
            dt = 1E-7
            current_time = 0.0
            total_hydrogen_mass = previous_mass
            while current_time < time_s:
                if total_hydrogen_mass <= 0:
                    mass_loss_rate = 0.0
                else:
                    #gęstość masowa gazu w komorze
                    gas_density = total_hydrogen_mass / self.I_S_CHAMBER_VOLUME
                    
                    #efuzja, czyli ile kg gazu na sekundę ucieka przez otwór
                    mass_loss_rate = 0.25 * gas_density * self.hydrogen_v_avg * self.I_S_hole_area
                
                #zmiana masy 
                mass_change = (self.HYDROGEN_FLOW_RATE - mass_loss_rate) * dt
                    

                #obliczamy nową masę
                total_hydrogen_mass = max(0.0, total_hydrogen_mass + mass_change)
                    
                #zmieniamy czas o dt sekeund
                current_time += dt
        else:
            print("System nie wykonał operacji, nie odpowiedni zakres czasowy")
        return total_hydrogen_mass

    #Metoda obliczająca gęstość liczbową (koncentracje) cząsteczek wodoru (H2)
    def I_S_calculate_number_density(self, total_hydrogen_mass):
        n = (total_hydrogen_mass / ((self.Hydrogen.molecular_molar_mass) * self.I_S_CHAMBER_VOLUME)) * self.PhysicalConstants.AVOGARD_CONSTANT 
        
        return n
    
    #Metoda obliczająca ciśnienie panujące w komorze ION Source
    def I_S_calculate_chamber_pressure(self, n): 
        p = n * self.PhysicalConstants.BOLTZMANN_CONSTANT * self.I_S_CHAMBER_TEMPERATURE 
        
        #ograniczenie ciśnienia [Pa] w komorze
        if 149.02 < p <  500.02:
            return p
        else:
            print("nieodpowiednie cisnienie")
            return p
            
    #Metoda obliczająca wydajność jonizacji na podstawie mocy startowej RF
    def I_S_calculate_ionization_efficiency(self, I_S_rf_peak_power):
        p_threshold = 32.5  
        k_steepness = 0.6   
        try:
            #współczynnik wskazujący ile % atomów zmieni się w plazme
            ionization_efficiency = 1.0 / (1.0 + math.exp(-k_steepness * (I_S_rf_peak_power - p_threshold)))
        except OverflowError:
            ionization_efficiency = 0.0

        #zabezpieczenie przed wyjściem poza logiczny zakres sprawności [0.01 do 1.0]
        ionization_efficiency = max(0.01, min(1.0, ionization_efficiency))
        return ionization_efficiency, I_S_rf_peak_power

    #Metoda oblicząjąca energie wytworzoną przez pole magnetyczne fal radiowych
    def I_S_calculate_RF_field_energy(self, n, I_S_rf_power):
         #średnia droga swobodna
        lambda_path = 1 / (math.sqrt(2) * math.pi * n * (self.Hydrogen.molecular_diameter**2))
        
        #wzór na podstawie danych z dokumentacji CERN i relacji: natężenie pole elektrycznego a moc w układach rezonansowych/antnowych
        max_electric_field = 77513.2 * math.sqrt(I_S_rf_power/30) 

        #energia przekazana przez pole RF - energia jaką zyskuje elektron 
        #(jeśli energia jest wieksza od energii wiazania atomu dojdzie do rozbicia i jonizacji H2)
        rf_work = abs(self.Electron.charge)*max_electric_field*lambda_path 
        
        return rf_work, I_S_rf_power

    #Metoda obliczająca koncentrację elektronów w plazmie, która jest równa koncentracji protonów w plazmie
    def I_S_calculate_electron_density(self, I_S_rf_power, ionization_efficiency):
        I_S_rf_power = I_S_rf_power * 1000 #[w] #zamiana jednostki: kW -> W
        
        #obliczenie czystej mocy pola magnetycznego, gdzie współczynnik 0,65 to procent mocy, która wpływa na elektrony, 
        I_S_net_rf_power = I_S_rf_power * 0.65 * ionization_efficiency 
        
        #koszt zerwania energetyczny wiązań między atomami i nie udanych prób wcześniejszych
        ionization_energy_cost = 40 * abs(self.Electron.charge) 

        #współczynnik objętościowy 
        alpha_recombination = 1.0e-13 

        #obliczenie koncentracji dla jonow o takim samym ladunku z równania bilansu mocy i objętościowej rekombinacji plazmy w stanie ustalonym
        ne = math.sqrt(I_S_net_rf_power / (self.I_S_CHAMBER_VOLUME * alpha_recombination * ionization_energy_cost))

        return ne

    #Metoda obliczająca prąd wiązki anionów wodoru wychodzącej z ION Source
    def I_S_calculate__beam_current(self, T_ces, ne):
        #zasada quasi-neutralności plazmy, czyli można przyjąc, że gestość jonów dodatnich jest równa gestości elektronów
        np = ne 
        
        #wzór Gaussa na sprawność cezu (eta) reprezentuje wydajność, z jaką powierzchnia elektrody przekształca uderzające w nią cząsteczki w jony ujemne wodoru
        eta_ces = math.exp(-((T_ces - 60) ** 2) / 50)
        
        #całkowita liczbę anionów wodoru, jaka rodzi się w ciągu jednej sekundy na cezowej elektrodzie
        hydride_production_rate = np* self.hydride_v_term * self.I_S_AP_AREA_CS * eta_ces 
        
        #wylicza ile jaki prąd został wygenerowany w wiązcę, która opuści ION Source
        I_gen = abs(self.Electron.charge) * hydride_production_rate 
        
        #wynik działania prawa Childa-Langmuira (pokazuje maksymalną przepustowość)
        I_limit = 4.71E-10 * (self.I_S_EXTRACTION_ELECTRODE_VOLTAGE ** 1.5) 
        
        #sprawdzenie i wybór miejszej wartości (prad ma ograniczoną przepustowość)
        I_final = min(I_gen, I_limit)
        
        return I_final
    
    #Metoda licząca ilość jonów, które wypłyneły z ION source na podstawie ilosci ladunków elektrycznych
    def I_S_calculate_beam_intensity(self, I_final):
        #czas trwania impulsu w CERN (600 mikrosekund)
        t_pulse = 0.0006 
        
        #liczba cząstek w wiązce
        N_Intensity = (I_final * t_pulse) / abs(self.Electron.charge) 
        
        return N_Intensity
        
    #Metoda obliczająca znormalizowaną emitancję termiczną (epsilon) wiązki
    def I_S_calculate_beam_emittance(self):
        #obliczenie epsilon ze wzoru termicznego
        epsilon = (self.I_S_AP_RADIUS * math.sqrt(self.I_S_ION_TEMPERATURE / (self.Hydride_ion.rest_mass_mev*1E6)))*1E6 #[pi * mm * mrad]
        
        return epsilon
       

    """
    -+/=====================================================/+-
        Radio-Frequency Quadrupole (RFQ) - wszsytkie metody 
    -+/=====================================================/+-
    """
    
    """
    -+/===========================================/+-
        Drift Tube Linac (DTL) - wszsytkie metody 
    -+/===========================================/+-
    """

    """
    -+/==========================================================/+-
        Cell-Coupled Drift Tube Linac (CCDTL) - wszsytkie metody 
    -+/==========================================================/+-
    """

    """
    -+/=============================================/+-
        Pi-Mode Structure (PIMS) - wszsytkie metody 
    -+/=============================================/+-
    """


#CERN Document Server (CDS) - informacje o akceleratorach

#Rzeczy, które się wykonają kiedy użytkownik odpali ten plik w konsoli
if __name__ == "__main__":
    print("Jesteś w pliku physics!")