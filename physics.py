import math

class Proton():
    def __init__(self):
        self.rest_mass = 1.673E-27 #[kg]
        self.charge = 1.602E-19

class Electron():
    def __init__(self):
        self.rest_mass = 9.109E-31 #[kg]
        self.charge = -1.602e-19 #[C]

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
        self.position_x = 0.0 #Współrzędna określająca położenie wiązki wzdłuż osi akceleratora (wymóg dwuwymiarowego świata).  
        self.position_y = 0.0 #Współrzędna określająca poprzeczne odchylenie wiązki od idealnego środka rury (wymóg dwuwymiarowego świata).  
        self.angle = 0.0 #Kąt lotu wiązki wyrażony w stopniach, gdzie 0 oznacza lot idealnie na wprost (wymóg kąta startowego).  
        
        self.energy = 4.5E-2 #[MeV] # Aktualna energia kinetyczna wiązki wyrażona w MeV (wartość startowa po ekstrakcji ze źródła). -> na podstawie dokumentów z cern 
        self.current = None #Prąd wiązki w miliamperach (mA), który wyliczasz na podstawie wydajności cezu i limitu dyszy. funkcja: _> apply_child_langmuir_limit
        self.N_Intensity = None #Liczba cząstek w paczce (Twój główny zasób ilościowy, który decyduje o szansie na odkrycie bozonu Higgsa). -> funkcja: I_S_calculate_H2_destruction_rate
        self.epsilon = None #Emitancja (miara chaosu i rozbieżności wiązki), którą wyliczasz z ciśnienia i mocy RF.  -> funkcja: I_S_calculate_beam_emittance
        
        self.is_alive = True #Flaga logiczna sprawdzająca, czy wiązka nie uległa zniszczeniu (warunek końca symulacji). -> funkcja: dopiero w RFQ
        


class Linac4():

    def __init__(self):
        self.overall_length = None

    """
    -+/=============================================================/+-
        ION Source - Wszsytkie metody dątyczące tego odcinka Linac4
    -+/=============================================================/+-
    """

    I_S_chamber_volume = 2.46E-4 #[m^3] #Objętość komory
   
    #Metoda wyliczająca mase wszystkich cząsteczek wodoru znajdującego się w komorze ION Source
    def I_S_calculate_mass_hydrogen(self, time_ms=0.5):
        hydrogen_flow_rate = 5E-7 #[kg/s] #Natężenie wodoru z zaworu piezoelektrycznego
        time_ms = float(input("Podaj czas otwarcia zaworu w milisekundach: ")) #<----------------------------------------tymczasowe
        time_s = time_ms*1e-3
        total_hydrogen_mass = hydrogen_flow_rate * time_s #[kg] #ile waży wodór wpuszczony do ION SOURCE
        print(f"masa wodoru:{total_hydrogen_mass}") #<----------------------------------------tymczasowe
        return total_hydrogen_mass

    #Metoda obliczająca gęstość liczbową cząsteczek wodoru 
    def I_S_calculate_number_density(self, mass=0):
        M = 2.016E-3 #[kg/mol] #masa molowa H2
        V = 2.46E-4 #[m^3] #Objętość komory
        NA = 6.022E23 #[1/mol] #Stała Avogarda
        
        #n [m^-3] – koncentracja cząsteczek. 
        n = (mass / (M * V)) * NA
        return n
    
    #Metoda obliczająca ciśnienie panujące w komorze ION Source
    def I_S_calculate_chamber_pressure(self, n=0): 
        kb=1.380649E-23 #[J/K] #Stała Boltzmanna
        T = 300 #[K] #temperatura

        #Ciśnienie wyrażone w pascalach
        p = n * kb * T
        print(f"ciśnienie wynosi: {p}") #<----------------------------------------tymczasowe
        return p

    #Metoda oblicząjąca:
    # - energie wytworzoną przez pole magnetyczne fal radiowych
    # - sprawność plazmy
    # - moc pola magnetycznego fal radiowych 
    def I_S_calculate_RF_field_energy(self, qe, n, P_rf):
        d = 2.89E-10 #[m] 
        lambda_path = 1 / (math.sqrt(2) * math.pi * n * (d**2)) #średnia droga swobodna
        
        P_rf_start = float(input("Podaj moc fal radiowych zakres 40-50 maks 100 kw:")) #<----------------------------------------tymczasowe
        P_rf= float(input("Podaj moc fal radiowych zakres 10-50 maks 50 kw:")) #<----------------------------------------tymczasowe
        
        #Wzór na podstawie danych z documentacji CERN i zasady amplituda pola elektrycznego wewnątrz komory plazmowej jest proporcjonalna 
        #do pierwiastka kwadratowego z mocy dostarczonej do anteny
        Emax = 77513.2 * math.sqrt(P_rf/30) 

        #Energia przekazana przez pole RF - energia jaką zyskuje elektron [J]
        #(jeśli energia jest wieksza od energii wiazania atomu dojdzie do rozbicia i jonizacji H2)
        w = qe*Emax*lambda_path

        if P_rf_start < 40.0:
            #print("UWAHA: Impuls zapłonowy był za słaby! Plazma utknęła w słabym trybie E.")
            sprawnosc_plazmy = 0.1  # Tylko 10% atomów wejdzie w stan plazmy
        else:
            #print("SUKCES: Plazma pomyślnie przeszła w wysokowydajny tryb indukcyjny H!")
            sprawnosc_plazmy = 1.0  # 100% wydajności zapłonu

        print(f"Energia dostarczona przez pole fal radiowych wynosi {Emax} a sprawność magmy wynosi {sprawnosc_plazmy}")
        return w, sprawnosc_plazmy, P_rf
    
    #Metoda obliczająca koncentrację elektronów w plazmie, która jest równa koncentracji protonów w plazmie
    def I_S_calculate_electron_density(self,  qe, P_rf, sprawnosc_plazmy):
        V = 2.46E-4 #[m^3] #Objętość komory
        P_rf = P_rf * 1000 #[w] #kW -> W
        
        #obliczenie czystej mocy pola magnetycznego, gdzie p_rf jest mocą fal radiowych, 0,65 to procent mocy, która wpływa na elektrony, 
        czysta_moc = P_rf * 0.65 * sprawnosc_plazmy 
        E_strat_dzule = 40 * qe #koszt zerwania energetyczny wiązań między atomami i nie udanych prób wcześniejszych
        loss_rate = 1e5 #ilość elektronów, które podczas jednej sekundy są neutralizowane

        ne = czysta_moc / (V * loss_rate * E_strat_dzule) #stała ilość elektronów w plazmie

        return ne

    #Metoda obliczająca prąd wiązki anionów wodoru wychodzącej z ION Source
    def I_S_calculate__beam_current(self, ne, qe):
        S = 174e-6  #[m^2] # Dokładna powierzchnia elektrody plazmowej pokrytej cezem
        np = ne #[m^-3] #Z zasady o neutralnym ładunku plazmy, gestość protonów jest równa gestości elektronów
        
        Ti_ev = 1.0 #[eV] #Temperatura protonu wzięta z dokumentacji CERN
        e_charge = 1.602e-19 # ładunek elektronu (przelicznik eV na Dżule)
        m_p = 1.673e-27 # masa protonu w kg
    
        vterm = math.sqrt((8 * Ti_ev * e_charge) / (math.pi * m_p)) #Średnia prędkość protonu 
        
        T_ces = float(input("Podaj temperaturę pieca cezu w °C (100 - 180): "))
        #Wzór Gaussa na sprawność cezu (eta) reprezentuje wydajność, z jaką powierzchnia elektrody przekształca uderzające w nią cząsteczki w jony ujemne wodoru
        eta_ces = math.exp(-((T_ces - 150) ** 2) / 200)
        
        hydride_production_rate = np* vterm * S * eta_ces #całkowita liczbę anionów wodoru, jaka rodzi się w ciągu jednej sekundy na cezowej elektrodzie

        qe = abs(qe) #wartość bezwzględna z ładunku, ponieważ prąd nie może być ujemny
        I_gen = qe * hydride_production_rate * eta_ces #[A] #wylicza ile jaki prąd został wygenerowany w wiązcę, która opuści Ion Source
        V_extraction = 4.5E4 #siła, z jaką zasilacz w CERN ciągnie jony do przodu
        I_limit = 4.71E-10 * (V_extraction ** 1.5) #Wynik działania prawa Childa-Langmuira. Pokazuje maksymalną przepustowość
        
        # Wybieramy mniejszą wartość
        I_final = min(I_gen, I_limit)
        return I_final
        
    #Metoda obliczająca znormalizowaną emitancję termiczną (epsilon) wiązki
    def I_S_calculate_beam_emittance(self, Ti_ev=0.5):
        Ti_ev = 1.0 #[eV]
        
        #Promień otworu elektrody w milimetrach (standard dla Linac4 to ok. 3 mm)
        r_mm =  3.25
        
        # 2. Energia spoczynkowa protonu w eV (m_p * c^2)
        E_rest_ev = 938.27e6  
        
        # 3. Obliczenie epsilon ze wzoru termicznego
        epsilon = r_mm * math.sqrt(Ti_ev / E_rest_ev) # [pi * mm * mrad]
        
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
    
    
    
    
    #Wszystko dotyczące :
    
    

    #Wszystko dotyczące :



    #Wszystko dotyczące :



    #Wszystko dotyczące :

l4 = Linac4()


print(l4.I_S_calculate_mass_hydrogen())