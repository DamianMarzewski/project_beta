import math

#Klasa stałych fizycznych - definiuje najważniejsze stałe potrzebne do wyliczeń
class PhysicalConstants():
    def __init__(self):
        self.SPEED_OF_LIGHT = 299792458 # [m/s]
        self.BOLTZMANN_CONSTANT = 1.380649e-23 # [J/K]
        self.AVOGARD_CONSTANT = 6.022E23 #[1/mol]

#Klasa elektronu - definiuje stałe dla tego obiektu
class Electron():
    def __init__(self):
        self.rest_mass_kg = 9.109E-31 #[kg]
        self.rest_mass_mev = 5.11e-1 # [MeV/c^2]
        self.charge = -1.602176634e-19 #[C]

#Klasa protonu - definiuje stałe dla tego obiektu
class Proton():
    def __init__(self):
        self.rest_mass_kg = 1.673E-27 #[kg]
        self.rest_mass_mev = 9.3827E2 #[MeV/c^2]
        self.charge = 1.602E-19 #[C]

#Klasa wodoru - definiuje stałe dla tego obiektu
class Hydrogen():
    def __init__(self):
        self.rest_mass_kg = 1.6737236E-27 #[kg]
        self.rest_mass_mev = 9.38783E2  # [MeV/c^2]

        self.molar_mass = 1.008E-3 #[kg/mol] #masa molowa jednego atomu wodoru (H)

        self.molecular_diameter = 2.89E-10 #[m] #efektywna średnica cząsteczki wodoru (H2)

#Klasa anionu wodoru - definiuje stałe dla tego obiektu
class Hydride_ion():
    def __init__(self):
        self.rest_mass_kg = 1.674278E-27 #[kg]
        self.rest_mass_mev = 939.294 #[mev/c^2]
        self.charge = -1.602176634E-19 #[C]
        self.energia_wiazania_ev = 0.754 #[eV]
        self.max_safe_magnetic_field = 0.3 #[T]
    
#Klasa wiązki - głównego obiektu, który będzie sterowany przez użytkownika
class Beam():
    def __init__(self):
        self.position_x = 0.0 #współrzędna określająca położenie wiązki wzdłuż osi akceleratora  
        self.position_y = 0.0 #Współrzędna określająca poprzeczne odchylenie wiązki od idealnego środka rury   
        self.angle = 0.0 #kąt lotu wiązki wyrażony w stopniach, gdzie 0 oznacza lot idealnie na wprost i równolegle do ścian akceleratora  
        
        self.energy = 4.5E-2 #[MeV] #aktualna energia kinetyczna wiązki
        self.current = None #[mA] #prąd wiązki wyliczony na podstawie wydajności cezu i limitu otworu
        self.N_Intensity = None #liczba cząstek w "paczce" wiązki
        self.epsilon = None #emitancja (miara chaosu i rozbieżności wiązki)
        
        self.is_alive = True #flaga logiczna sprawdzająca, czy wiązka nie uległa zniszczeniu 
        
#Klasa odcinka w systemie akceleartorów (butla z H2 -> koniec Linac4) - zawiera wszystkie metody fizyczne dla tego odcinka
class Linac4():

    def __init__(self, PhysicalConstants, Electron, Proton, Hydrogen, Hydride_ion):
        #Zdefiniowanie obiektów
        self.PhysicalConstants = PhysicalConstants
        self.Electron = Electron
        self.Proton = Proton
        self.Hydrogen = Hydrogen
        self.Hydride_ion = Hydride_ion
        
        #cała długość odcinka (butla z H2 -> koniec Linac4)
        self.overall_length = None #[m]
        
        #Stałe fizyczne
        self.KB = self.PhysicalConstants.BOLTZMANN_CONSTANT # [J/K]
        self.NA = self.PhysicalConstants.AVOGARD_CONSTANT #[1/mol]

        #Stałe elektronu
        self.electron_charge = self.Electron.charge #[C]

        #Stałe protonu
        self.proton_rest_mass_kg = self.Proton.rest_mass_kg #[kg]
        self.proton_rest_mass_mev = self.Proton.rest_mass_mev #[MeV/c^2]

        #Stałe wodoru
        self.h2_molecular_diameter = self.Hydrogen.molecular_diameter  #[m] 
        self.hydrogen_molar_mass = self.Hydrogen.molar_mass #[kg/mol]

        #Stałe anionu wodoru
        self.hydride_rest_mass_kg = self.Hydride_ion.rest_mass_kg #[kg]

        #ION Source
        self.HYDROGEN_FLOW_RATE = 5E-7 #[kg/s] #natężenie wodoru z zaworu piezoelektrycznego
        self.I_S_CHAMBER_VOLUME = 2.46E-4 #[m^3] #objętość komory
        self.I_S_CHAMBER_TEMPERATURE = 300 #[K] #temperatura w komorze
        self.I_S_EXTRACTION_ELECTRODE_VOLTAGE = 4.5E4 #[V] #siła, z jaką zasilacz w CERN ciągnie jony z komory ION Source
        self.I_S_ION_TEMPERATURE = 1.0 #[eV] #temperatura jonu wodoru wzięta z dokumentacji CERN
        self.I_S_AP_AREA_CS = 174e-6 #[m^2] #rzeczywista powierzchnia cezowa wewnątrz komory na której zachodzi jonizacja
        self.I_S_AP_RADIUS = 3.25 #[mm] #promień otworu wylotowego
        
    """
    -+/=============================================================/+-
        ION Source - Wszsytkie metody dątyczące tego odcinka Linac4
    -+/=============================================================/+-
    """

    #Metoda wyliczająca mase wszystkich cząsteczek wodoru znajdującego się w komorze ION Source
    def I_S_calculate_mass_hydrogen(self, time_ms):
        time_s = time_ms*1e-3 #[s] #zmiana jednostki: ms -> s
        total_hydrogen_mass = self.HYDROGEN_FLOW_RATE * time_s  
        
        return total_hydrogen_mass

    #Metoda obliczająca gęstość liczbową cząsteczek wodoru 
    def I_S_calculate_number_density(self, total_hydrogen_mass):
        #koncentracja cząsteczek H2 w komorze ION
        n = (total_hydrogen_mass / ((2*self.hydrogen_molar_mass) * self.I_S_CHAMBER_VOLUME)) * self.NA 
        
        return n
    
    #Metoda obliczająca ciśnienie panujące w komorze ION Source
    def I_S_calculate_chamber_pressure(self, n): 
        p = n * self.KB * self.I_S_CHAMBER_TEMPERATURE 
        
        return p
    
    #Metoda oblicząjąca energie wytworzoną przez pole magnetyczne fal radiowych i wydajność jonizacji
    def I_S_calculate_RF_field_energy(self, n, I_S_rf_power_start, I_S_rf_power):
        lambda_path = 1 / (math.sqrt(2) * math.pi * n * (self.h2_molecular_diameter**2)) #średnia droga swobodna
        
        #wzór na podstawie danych z documentacji CERN i relacji: natężenie pole elektrycznego a moc w układach rezonansowych/antnowych
        max_electric_field = 77513.2 * math.sqrt(I_S_rf_power/30) 

        #energia przekazana przez pole RF - energia jaką zyskuje elektron 
        #(jeśli energia jest wieksza od energii wiazania atomu dojdzie do rozbicia i jonizacji H2)
        rf_work = abs(self.electron_charge)*max_electric_field*lambda_path 

        if I_S_rf_power_start < 40.0: 
            #współczynnik wskazujący, że tylko 10% atomów zmieni się w plazme
            ionization_efficiency = 0.1  
        else:
            ionization_efficiency = 1.0 

        return rf_work, ionization_efficiency, I_S_rf_power
    
    #Metoda obliczająca koncentrację elektronów w plazmie, która jest równa koncentracji protonów w plazmie
    def I_S_calculate_electron_density(self, I_S_rf_power, ionization_efficiency):
        I_S_rf_power = I_S_rf_power * 1000 #[w] #zamiana jednostki: kW -> W
        
        #obliczenie czystej mocy pola magnetycznego, gdzie współczynnik 0,65 to procent mocy, która wpływa na elektrony, 
        I_S_net_rf_power = I_S_rf_power * 0.65 * ionization_efficiency 
        
        #koszt zerwania energetyczny wiązań między atomami i nie udanych prób wcześniejszych
        ionization_energy_cost = 40 * abs(self.electron_charge) 

        #ilość elektronów, które podczas jednej sekundy są neutralizowane
        recombination_rate = 1e5 

        #stała ilość elektronów w plazmie, jest to koncentracja elektronów 
        ne = I_S_net_rf_power / (self.I_S_CHAMBER_VOLUME * recombination_rate * ionization_energy_cost) 

        return ne

    #Metoda obliczająca prąd wiązki anionów wodoru wychodzącej z ION Source
    def I_S_calculate__beam_current(self, ne):
        #zasada quasi-neutralności plazmy, czyli można przyjąc, że gestość jonów dodatnich jest równa gestości elektronów
        np = ne 

        #średnia prędkość jonów wodoru
        hydride_vterm = math.sqrt((8 * self.I_S_ION_TEMPERATURE * abs(self.electron_charge)) / (math.pi * self.hydride_rest_mass_kg)) 
        
        T_ces = float(input("Podaj temperaturę pieca cezu w °C (100 - 180): ")) #[°C] <--------tymczasowe
        
        #wzór Gaussa na sprawność cezu (eta) reprezentuje wydajność, z jaką powierzchnia elektrody przekształca uderzające w nią cząsteczki w jony ujemne wodoru
        eta_ces = math.exp(-((T_ces - 150) ** 2) / 200)
        
        #całkowita liczbę anionów wodoru, jaka rodzi się w ciągu jednej sekundy na cezowej elektrodzie
        hydride_production_rate = np* hydride_vterm * self.I_S_AP_AREA_CS * eta_ces 
        
        #wylicza ile jaki prąd został wygenerowany w wiązcę, która opuści Ion Source
        I_gen = abs(self.electron_charge) * hydride_production_rate 
        
        #wynik działania prawa Childa-Langmuira - pokazuje maksymalną przepustowość
        I_limit = 4.71E-10 * (self.I_S_EXTRACTION_ELECTRODE_VOLTAGE ** 1.5) 
        
        #sprawdzenie i wybór miejszej wartości (prad ma ograniczoną przepustowość)
        I_final = min(I_gen, I_limit)
        
        return I_final
    
    #metoda licząca ilość jonów, które wypłyneły z ion source na podstawie ilosci ladunków elektrycznych
    def I_S_calculate_beam_intensity(self, I_final):
        #czas trwania impulsu w CERN (600 mikrosekund)
        t_pulse = 0.0006 
        
        #liczba cząstek w wiązce
        N_Intensity = (I_final * t_pulse) / abs(self.electron_charge) 
        
        return N_Intensity
        
    #Metoda obliczająca znormalizowaną emitancję termiczną (epsilon) wiązki
    def I_S_calculate_beam_emittance(self):
        #obliczenie epsilon ze wzoru termicznego
        epsilon = self.I_S_AP_RADIUS * math.sqrt(self.I_S_ION_TEMPERATURE / (self.proton_rest_mass_mev * 1e6)) #[pi * mm * mrad]
        
        return epsilon
       

    """
    -+/=====================================================/+-
        Radio-Frequency Quadrupole (RFQ) - wszsytkie metody 
    -+/=====================================================/+-
    """
    #CERN Document Server (CDS)
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

'''
Przeprowadzenie testowej symulacji

'''

l4 = Linac4(PhysicalConstants(), Electron(), Proton(), Hydrogen(), Hydride_ion())

wiazka = Beam()

time_ms = float(input("Podaj czas otwarcia zaworu w milisekundach: "))
total_hydrogen_mass=l4.I_S_calculate_mass_hydrogen(time_ms)

n=l4.I_S_calculate_number_density(total_hydrogen_mass)

p=l4.I_S_calculate_chamber_pressure(n)

I_S_rf_power_start = float(input("Podaj moc startowa fal radiowych zakres 40-50 maks 100 kw:")) 
I_S_rf_power= float(input("Podaj moc fal radiowych zakres 10-50 maks 50 kw:")) 

rf_work, ionization_efficiency, I_S_rf_power = l4.I_S_calculate_RF_field_energy(n, I_S_rf_power_start, I_S_rf_power)

ne = l4.I_S_calculate_electron_density( I_S_rf_power, ionization_efficiency)

I_final = l4.I_S_calculate__beam_current(ne)
N_Intensity = l4.I_S_calculate_beam_intensity(I_final)
epsilon = l4.I_S_calculate_beam_emittance()

wiazka.energy = 4.5E-2
wiazka.current = I_final  
wiazka.N_Intensity =  N_Intensity 
wiazka.epsilon = epsilon

print(f"Informacje o wiązce:\n-energia wiązki {wiazka.energy}, \n-prąd w wiązce {wiazka.current}, \n-ilość jonów w wiązce tak zwana koncentracja jonów {wiazka.N_Intensity} \n-emitacja wiązki {wiazka.epsilon}")


        
        