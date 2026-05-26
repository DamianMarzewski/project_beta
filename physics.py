"""
+=======================================+
ZAIMPORTOWANIE: 
a) bibliotek:
        math - możliwość korzystania z bardziej zaawansowanej matematyki
        random - wprowadzenie systemu losowości do mechanik symulacji
+=======================================+
"""

import math
import random

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
class HydrideIon():
    def __init__(self):
        self.rest_mass_kg = 1.674278E-27 #[kg]
        self.rest_mass_mev = 939.294 #[mev/c^2]
        self.charge = -1.602176634E-19 #[C]
        self.binding_energy_ev = 0.754 #[eV]
        self.max_safe_magnetic_field = 0.3 #[T]
"""
-+/===================================/+-
    Klasa odcinka Negative Ion Source
-+/===================================/+-
"""        
#Klasa odcinka w systemie akceleartorów (butla z H2 -> Linac4) - zawiera wszystkie metody fizyczne dla tego odcinka
class NegativeIonSource():

    def __init__(self, PhysicalConstants, Electron, Proton, Hydrogen, HydrideIon):
        #zdefiniowanie obiektów
        self.PhysicalConstants = PhysicalConstants
        self.Electron = Electron
        self.Proton = Proton
        self.Hydrogen = Hydrogen
        self.HydrideIon = HydrideIon
        
        #cała długość odcinka (butla z H2 -> koniec Linac4)
        self.overall_length = None #[m]
        
        #ION Source
        self.HYDROGEN_FLOW_RATE = 1.794E-7  #[kg/s] #natężenie wodoru z zaworu piezoelektrycznego
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
        self.hydride_v_term = math.sqrt((2 * self.I_S_ION_TEMPERATURE * abs(self.Electron.charge)) / (self.HydrideIon.rest_mass_kg)) #[m/s] #najprawdopodobniejsza prędkość jonów wodoru

    #Metoda wyliczająca mase wszystkich cząsteczek wodoru znajdującego się w komorze ION Source
    def I_S_calculate_mass_hydrogen(self, previous_mass, time_us):
        if not (200 <= time_us <= 500):
             raise OverflowError(f"Czas impulsu {time_us} us poza zakresem [200, 500]")
        time_s = time_us*1e-6 
        dt = 1E-7
        current_time = 0.0
        total_hydrogen_mass = previous_mass
        while current_time < time_s:
            if total_hydrogen_mass <= 0:
                mass_loss_rate = 0.0
            else:
                gas_density = total_hydrogen_mass / self.I_S_CHAMBER_VOLUME
                    
                mass_loss_rate = 0.25 * gas_density * self.hydrogen_v_avg * self.I_S_hole_area
                
            mass_change = (self.HYDROGEN_FLOW_RATE - mass_loss_rate) * dt
                    
            total_hydrogen_mass = max(0.0, total_hydrogen_mass + mass_change)
                    
            current_time += dt    
            
        return total_hydrogen_mass

    #Metoda obliczająca gęstość liczbową (koncentracje) cząsteczek wodoru (H2)
    def I_S_calculate_number_density(self, total_hydrogen_mass):
        n = (total_hydrogen_mass / ((self.Hydrogen.molecular_molar_mass) * self.I_S_CHAMBER_VOLUME)) * self.PhysicalConstants.AVOGARD_CONSTANT 
        
        return n
    
    #Metoda obliczająca ciśnienie panujące w komorze ION Source
    def I_S_calculate_chamber_pressure(self, n): 
        p = n * self.PhysicalConstants.BOLTZMANN_CONSTANT * self.I_S_CHAMBER_TEMPERATURE 
        
        return p
            
    #Metoda obliczająca wydajność jonizacji na podstawie mocy startowej RF
    def I_S_calculate_ionization_efficiency(self, I_S_rf_peak_power):
        if not (20 <= I_S_rf_peak_power <= 80):
            raise ValueError(f"Moc szczytowa RF poza zakresem [20, 80] kW")
       
        p_threshold = 32.5  
        k_steepness = 0.6   
        try:
            #współczynnik wskazujący ile % atomów zmieni się w plazme
            ionization_efficiency = 1.0 / (1.0 + math.exp(-k_steepness * (I_S_rf_peak_power - p_threshold)))
        except ValueError:
            ionization_efficiency = 0.0

        ionization_efficiency = max(0.01, min(1.0, ionization_efficiency))
        return ionization_efficiency, I_S_rf_peak_power

    #Metoda oblicząjąca energie wytworzoną przez pole magnetyczne fal radiowych
    def I_S_calculate_RF_field_energy(self, n, I_S_rf_power):
        if  not (20 <= I_S_rf_power <= 100):
            raise ValueError("Moc RF poza zakresem [10, 50] kW")

        lambda_path = 1 / (math.sqrt(2) * math.pi * n * (self.Hydrogen.molecular_diameter**2))
        
        #wzór na podstawie danych z dokumentacji CERN i relacji: natężenie pole elektrycznego a moc w układach rezonansowych/antnowych
        max_electric_field = 77513.2 * math.sqrt(I_S_rf_power/30) 

        rf_work = abs(self.Electron.charge)*max_electric_field*lambda_path 
        
        return rf_work, I_S_rf_power

    #Metoda obliczająca koncentrację elektronów w plazmie, która jest równa koncentracji protonów w plazmie
    def I_S_calculate_electron_density(self, I_S_rf_power, ionization_efficiency):
        I_S_rf_power = I_S_rf_power * 1000 

        I_S_net_rf_power = I_S_rf_power * 0.65 * ionization_efficiency 
        
        ionization_energy_cost = 40 * abs(self.Electron.charge) 

        alpha_recombination = 1.0e-13 

        ne = math.sqrt(I_S_net_rf_power / (self.I_S_CHAMBER_VOLUME * alpha_recombination * ionization_energy_cost))

        return ne

    #Metoda obliczająca prąd wiązki anionów wodoru wychodzącej z ION Source
    def I_S_calculate__beam_current(self, T_ces, ne):
        if T_ces < 40:
            raise ValueError(
                f"Temperatura {T_ces}°C jest ZA NISKA!\n"
                "Cez nie odparowuje. Brak efektywnej produkcji jonów H-."
                )

        elif T_ces > 100:
            raise ValueError(
                f"BŁĄD KRYTYCZNY: Temperatura {T_ces}°C jest ZA WYSOKA!\n"
                "Gwałtowny wyrzut cezu wywołał przebicie elektryczne na elektrodach 45 kV."
                )

        elif 80 < T_ces <= 100:
            print(f"OSTRZEŻENIE: Temperatura {T_ces}°C przekracza normę operacyjną. Wydajność źródła drastecznie spada.!")
 
        #zasada quasi-neutralności plazmy, czyli można przyjąc, że gestość jonów dodatnich jest równa gestości elektronów
        np = ne 
        
        #wzór Gaussa na sprawność cezu (eta) reprezentuje wydajność, z jaką powierzchnia elektrody przekształca uderzające w nią cząsteczki w jony ujemne wodoru
        eta_ces = math.exp(-((T_ces - 60) ** 2) / 50)
        
        hydride_production_rate = np* self.hydride_v_term * self.I_S_AP_AREA_CS * eta_ces 
        
        I_gen = abs(self.Electron.charge) * hydride_production_rate 
        
        #wynik działania prawa Childa-Langmuira (pokazuje maksymalną przepustowość)
        I_limit = 4.71E-10 * (self.I_S_EXTRACTION_ELECTRODE_VOLTAGE ** 1.5) 
        
        I_final = min(I_gen, I_limit)
        
        return I_final
    
    #Metoda licząca ilość jonów, które wypłyneły z ION source na podstawie ilosci ladunków elektrycznych
    def I_S_calculate_beam_intensity(self, I_final):
        t_pulse = 0.0006 
        
        N_Intensity = (I_final * t_pulse) / abs(self.Electron.charge) 
        
        return N_Intensity
        
    #Metoda obliczająca znormalizowaną emitancję termiczną (epsilon) wiązki
    def I_S_calculate_beam_emittance(self):
        #obliczenie epsilon ze wzoru termicznego
        epsilon = (self.I_S_AP_RADIUS * math.sqrt(self.I_S_ION_TEMPERATURE / (self.HydrideIon.rest_mass_mev*1E6)))*1E6 #[pi * mm * mrad]
        
        return epsilon
"""
-+/=====================================================/+-
    Klasa odcinka Linac4 
-+/=====================================================/+-    
""" 
class Linac4():
    def __init__(self, PhysicalConstants, Electron, Proton, Hydrogen, HydrideIon):
        
        #zdefiniowanie obiektów
        self.PhysicalConstants = PhysicalConstants
        self.Electron = Electron
        self.Proton = Proton
        self.Hydrogen = Hydrogen
        self.HydrideIon = HydrideIon                
 
        #stałe LEBT
        self.LEBT_LENGTH = 1.8    #[m]
        #promień rury — granica śmierci wiązki
        self.LEBT_RADIUS = 0.01   #[m]
        self.NOMINAL_LOSS_PER_M = 0.05 
        self.LEBT_VOLUME = math.pi * (self.LEBT_RADIUS ** 2) * self.LEBT_LENGTH

        #stałe kalibracyjne dla mechaniki gry:
        self.LEBT_SPACE_CHARGE_SCALE = 5.0E-6  
        self.LEBT_SOLENOID_GAME_SCALE = 0.8    
    
    """
    -+/=====================================================/+-
        LEBT (Low Energy Beam Transport) - wszsytkie metody 
    -+/=====================================================/+-
    """

    #Metoda obliczająca aktualne ciśnienie w rurze po jednym ticku (komendzie)
    def lebt_calculate_vacuum(self, pumps_active, current_vacuum, dt=1E-3):
        leak_rate = 1.5E-6  # [Pa*m^3/s] stały napływ gazu przez mikroszczeliny

        if pumps_active:
            pump_efficiency = random.uniform(0.92, 1.08)
            pumping_speed = 120.0 * pump_efficiency
        else:
            pumping_speed = 0.0

        dp = ((leak_rate - (pumping_speed * current_vacuum)) / self.LEBT_VOLUME) * dt
        new_vacuum = current_vacuum + dp

        return max(1.0E-7, min(1.0E-3, new_vacuum))
    
    #Metoda obliczająca straty prądu przez zderzenia jonów
    def lebt_calculate_transmission(self, vacuum, current):
        if current is None or current <= 0:
            return 0.0

        sigma_stripping = 4.2E-19  
        gas_n = vacuum * 2.4E22   

        if gas_n > 0:
            lambda_stripping = 1.0 / (gas_n * sigma_stripping)
            survival_probability = math.exp(-self.LEBT_LENGTH / lambda_stripping)
            return current * survival_probability

        return current

    #Metoda obliczająca siłę skupiającą solenoidu na podstawie prądu gracza
    def lebt_calculate_solenoid_focus(self, current_solenoid, beam_energy_mev):
        if current_solenoid <= 0:
            return 0.0

        thermal_noise = random.gauss(0, 0.02)

        force = ((current_solenoid / 100.0) ** 2) * self.LEBT_SOLENOID_GAME_SCALE
        focusing_force = force * (1.0 + thermal_noise)

        return focusing_force

    #Metoda obliczająca straty prądu przez uderzenia wiązki o ścianki rury + naturalne
    def lebt_calculate_scraping_and_nominal_losses(self, y, current, dx):
        if current <= 0:
            return 0.0

        current -= current * (self.NOMINAL_LOSS_PER_M * dx)

        sigma_beam = 0.0025
        distance_from_wall = self.LEBT_RADIUS - abs(y)

        if distance_from_wall < (3 * sigma_beam):
            proximity_factor = math.exp(-(distance_from_wall ** 2) / (2 * (sigma_beam ** 2)))
            scraping_loss = current * proximity_factor * (dx / self.LEBT_LENGTH)
            current = max(0.0, current - scraping_loss)

        return current
    
    #Metoda symuluje degradację maszyny 
    def lebt_apply_environmental_drift(self, current_solenoid, current_vacuum, beam_angle, dx):
        if dx <= 0:
            return current_solenoid, current_vacuum, 0.0

        cooling_fluctuation = random.uniform(0.95, 1.05)
        thermal_decay = 3.0E-5 * (current_solenoid ** 2) * cooling_fluctuation * dx
        new_solenoid = max(0.0, current_solenoid - thermal_decay)

        desorption_burst = random.uniform(5.0E-7, 2.8E-6)
        new_vacuum = min(1.0E-3, current_vacuum + desorption_burst * dx)

        vibration_kick = random.gauss(0, 0.0004)
        new_angle = beam_angle + vibration_kick

        return new_solenoid, new_vacuum, new_angle

    #Metoda obliczająca nowe position_y i kąt wiązki po przebyciu dx metrów
    def lebt_calculate_trajectory_step(self, x, y, angle, current, focusing_force, steerer_voltage, dx):
        space_charge_kick = (self.LEBT_SPACE_CHARGE_SCALE * current * dx) / (abs(y) + 0.005)
       
        steerer_kick = steerer_voltage * 1.85E-5

        if focusing_force > 0:
            solenoid_angle_correction = -(focusing_force * y * dx)
        else:
            solenoid_angle_correction = 0.0

        if y >= 0:
            new_angle = angle + solenoid_angle_correction + steerer_kick + space_charge_kick
        else:
            new_angle = angle + solenoid_angle_correction + steerer_kick - space_charge_kick

        new_y = y + (new_angle * dx)
        new_x = x + dx

        return new_x, new_y, new_angle

    #Metoda unicjująca wszystko - wywołuje wszystkie powyższe metody w odpowiedniej kolejności.
    def lebt_process_automatic_step(self, beam, current_solenoid, current_vacuum, steerer_voltage, dx):

        if not beam.is_alive:
            return current_solenoid, current_vacuum, {}

        prev_current = beam.current
        prev_y = beam.position_y
        prev_angle = beam.angle

        updated_solenoid, updated_vacuum, new_angle_after_vibration = self.lebt_apply_environmental_drift(current_solenoid, current_vacuum, beam.angle, dx)

        beam.angle = new_angle_after_vibration

        beam.position_x += dx

        beam.current = self.lebt_calculate_transmission(updated_vacuum, beam.current)

        beam.current = self.lebt_calculate_scraping_and_nominal_losses(beam.position_y, beam.current, dx)

        force = self.lebt_calculate_solenoid_focus(updated_solenoid, beam.energy)

        _, new_y, new_angle = self.lebt_calculate_trajectory_step(
            beam.position_x, beam.position_y, beam.angle, beam.current, force, steerer_voltage, dx
        )
        beam.position_y = new_y
        beam.angle = new_angle

        if abs(beam.position_y) >= self.LEBT_RADIUS:
            beam.is_alive = False

        return updated_solenoid, updated_vacuum
    """
    -+/=====================================================/+-
        Radio-Frequency Quadrupole (RFQ) - wszsytkie metody 
    -+/=====================================================/+-
    """
    
    """
    -+/=========================================================/+-
        MEBT (Medium  Energy Beam Transport) - wszsytkie metody 
    -+/=========================================================/+-
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