class User:
    def __init__(self):
        self.nickname=""
        self.password="gigathon2026"
        self.auth = False

class AcceleratorData:
    def __init__(self):
        self.total_hydrogen_mass = 0
        self.n = 0
        self.p = 0
        self.ionization_efficiency = 0
        self.I_S_rf_start_power = 0
        self.I_S_rf_power = 0
        self.rf_work = 0
        self.ne = 0
        self.T_cez = 0
        self.current_solenoid = 0
        self.current_vacuum = 1013.25
        self.steerer_voltage = 0
        self.focusing_force = 0
        self.dx = 0
        self.pomp_vacuum_status = False
    
    #Metoda służąca do kopiowania danych z jednego obiektu danych do drugiego
    def copy_from(self, source):
        self.total_hydrogen_mass = source.total_hydrogen_mass
        self.n = source.n
        self.p = source.p
        self.ionization_efficiency = source.ionization_efficiency
        self.I_S_rf_start_power = source.I_S_rf_start_power
        self.I_S_rf_power = source.I_S_rf_power
        self.rf_work = source.rf_work
        self.ne = source.ne
        self.T_cez = source.T_cez
        self.current_solenoid = source.current_solenoid
        self.current_vacuum = source.current_vacuum
        self.steerer_voltage = source.steerer_voltage
        self.focusing_force = source.focusing_force
        self.dx = source.dx
        self.pomp_vacuum_status = source.pomp_vacuum_status

class AcceleratorEnvironment:
    def __init__(self):
        #niezależne obiekty danych dla każdego akceleratora
        self.negative_ion_source = AcceleratorData()
        self.linac4 = AcceleratorData()
        
        #wskaźnik akceleratora
        self.active = None 

    #Metoda ustawiająca dany akcelerator
    def set_accelerator(self, name):
        if name == "Negative Ion Source":
            self.active = self.negative_ion_source
        elif name == "Linac4":
            self.active = self.linac4

    #Ukryta metoda do wyszukiwania obiektów danych po nazwie
    def _get_accelerator_by_name(self, name):
        if name == "Negative Ion Source":
            return self.negative_ion_source
        elif name == "Linac4":
            return self.linac4
        return None    
    
    #Metdoda kopiująca dane z jednego akceleratora od drugiego
    def copy_data(self, data_from, data_for):
        source = self._get_accelerator_by_name(data_from)
        target = self._get_accelerator_by_name(data_for)
        
        if source and target:
            # Target (np. LHC) kopiuje do siebie wartości ze Source (np. Negative Ion Source)
            target.copy_from(source)
        else:
            print(f"Błąd: Nie znaleziono akceleratora o nazwie {data_from} lub {data_for}")

#Klasa wiązki - głównego obiektu, który będzie sterowany przez użytkownika
class Beam():
    def __init__(self):
        self.position_x = 0.0 #współrzędna określająca położenie wiązki wzdłuż osi akceleratora  
        self.position_y = 0.0 #Współrzędna określająca poprzeczne odchylenie wiązki od idealnego środka rury   
        self.angle = 0.0 #kąt lotu wiązki wyrażony w stopniach, gdzie 0 oznacza lot idealnie na wprost i równolegle do ścian akceleratora  
        
        self.energy = 4.5E-2 #[MeV] #aktualna energia kinetyczna wiązki
        self.energy_spread = 0.5 #[%] #procentowa różnica w pędzie między cząstkami w tej samej wiązce
        self.current = None #[mA] #prąd wiązki
        self.percent_light_speed = 1 #[%]
        self.luminosity_potential = 100 #[%]
       
        self.N_Intensity = None #liczba cząstek w "paczce" wiązki
        self.epsilon = None #emitancja (miara chaosu i rozbieżności wiązki)
        self.profile = (None, None) #profil wiązki - promień szerokości
        self.RF_phase = None
        self.bunch_structure = None

        self.is_alive = True #flaga logiczna sprawdzająca, czy wiązka nie uległa zniszczeniu 