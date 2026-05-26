"""
+=======================================+
ZAIMPORTOWANIE: 
a) bibliotek:
        math - możliwość korzystania z bardziej zaawansowanej matematyki
        turtle - możliwość tworzenia grafiki w oknie
b) plików/funkcjonalności z innych plików
        utils - łatwe zarządzanie stylami
+=======================================+
"""

import math
import turtle
from utils import Styling

#Klasa obsługująca tworzenie całej mapy w turtle
class CernMapApp():
    def __init__(self):
        #dostęp do orgazinera stylami
        self.style = Styling()
        
        self.width_screen_window  = 0.85
        self.height_screen_window = 0.85
        
        self.screen = self.screen_config(-800, -450, 800, 450)
        self.root = self.screen._root
        self.pen = turtle.Turtle()
        
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.line_accuracy = 1440
        self.ratio_scale = 1

        self.timer_update = None
        self.timer_resize = None
        
        #reakcja na dane eventy
        self.root.bind("<Configure>", self.check_width_window)
        self.root.protocol("WM_DELETE_WINDOW", self.hide_screen_window)

        #zdefiniowanie rozmiaru układu kartezjańskiego, współrzędnych akceleratorów, ich promieni oraz grubość linii w szablonie
        self.LAYOUTS = {
            "large": {
                "world": (-800, -450, 800, 450),
                "scale": 1.0,
                "lhc": ((0, 175), (630, 220)),
                "sps": ((60, 10), (330, 110)),
                "ps": ((220, -325), (130, 45)),
                "bst": ((105, -225), (65, 22)),
                "linac4": 1.1,
                "map_legend": (-365, -430, 98, -430),
                "thickness": [6, 5, 5, 7, 8, 4, 40, 30, 12] # grubości linii w paczce

            },
            "medium": {
                "world": (-480, -270, 480, 270),
                "scale": 0.6,
                "lhc": ((0, 105), (378, 132)),
                "sps": ((36, 6), (198, 66)),
                "ps": ((132, -195), (78, 27)),
                "bst": ((63, -135), (39, 13)),
                "linac4": 0.6,
                "map_legend": (-365, -250, 98, -250),
                "thickness": [5, 4, 4, 6, 7, 3, 35, 25, 11]
            },
            "small": {
                "world": (-320, -180, 320, 180),
                "scale": 0.4,
                "lhc": ((0, 70), (252, 88)),
                "sps": ((24, 4), (132, 44)),
                "ps": ((88, -130), (52, 18)),
                "bst": ((42, -90), (26, 8)),
                "linac4": 0.4,
                "map_legend": (-154, -154, -154, -165),
                "thickness": [2, 2, 2, 3, 4, 1, 30, 20, 8]
            }
        }

        self.track_points = [] 
        self.beam_pen = turtle.Turtle()
        self.beam_pen.shape("circle")
        self.beam_pen.penup()
        self.beam_pen.hideturtle()
        
    #Metoda inicjująca dziłanie graficznego okna 
    def screen_config(self, left_x, left_y, right_x, right_y):
        self.screen = turtle.Screen()
        self.screen.setup(self.width_screen_window , self.height_screen_window)
        self.screen.title("Schemat Akceleratorów CERN")
        self.screen.bgcolor(f"{self.style.map_background_color}")
        self.screen.tracer(0) 
        self.screen.setworldcoordinates(left_x, left_y, right_x, right_y)
        return self.screen
    
    #Metoda ustaiwająca odpowiedni rozmiar wszystkiego
    def set_size(self):
            if not self.root.winfo_exists():
                return
            self.root.bind("<Configure>", "")
            current_window_width = self.root.winfo_width() 
            
            #sparwdzanie jaki szbl0on trzeba wykorzystać
            if current_window_width >= 1025:   
                self.config_layouts = self.LAYOUTS["large"]
            elif current_window_width >= 641: 
                self.config_layouts = self.LAYOUTS["medium"]
            else:                      
                self.config_layouts = self.LAYOUTS["small"]
            
            #ustawienie układu kartezjańskiego
            self.screen.setworldcoordinates(*self.config_layouts["world"])

            #ustawienie współrzędnych obiektów
            self.ratio_scale = self.config_layouts["scale"]
            self.lhc_coords, self.lhc_radius = self.config_layouts["lhc"]
            self.sps_coords, self.sps_radius = self.config_layouts["sps"]
            self.ps_coords, self.ps_radius = self.config_layouts["ps"]
            self.bst_coords, self.bst_radius = self.config_layouts["bst"]
            
            #ustawienie grubości linii
            thickness = self.config_layouts["thickness"]
            self.style.map_linac4_thickness = thickness[0]
            self.style.map_bst_thickness = thickness[1]
            self.style.map_ps_thickness = thickness[2]
            self.style.map_sps_thickness = thickness[3]
            self.style.map_lhc_thickness = thickness[4]
            self.style.map_trn_line_thickness = thickness[5]
            self.style.background_detectors_thickness = thickness[6]
            self.style.detectors_thickness = thickness[7]
            self.style.text_thickness = thickness[8]

            self.l4_start = (int(-60 * self.config_layouts["linac4"]), int(-340 * self.config_layouts["linac4"]))
            self.l4_end = self.find_point_on_ellipse(self.bst_coords, self.bst_radius, 0.75)

            self.pen.clear()
            self.create_map()
            self.screen.update()
            
            self.timer_resize = None

            self.root.bind("<Configure>", self.check_width_window)
    
    #Metoda zabezpieczająca przed ciągłym wyrosywywaniem okna podczas zmieny jego rozmiaru
    def check_width_window(self, event=None):
        if self.timer_resize:
            self.root.after_cancel(self.timer_resize)
        self.timer_resize = self.root.after(50, self.set_size)

    #Metoda rysująca elipse
    def display_ellipse(self, center, radius, color, thickness, text="", text_thickness=14, move_text=(0,0)):
        self.pen.penup()
        self.pen.goto(center[0] + radius[0], center[1])
        self.pen.pendown()
        self.pen.color(color)
        self.pen.pensize(thickness)
        
        for i in range(self.line_accuracy + 1):
            radians = math.radians(i / 4.0)
            x = center[0] + radius[0] * math.cos(radians)
            y = center[1] + radius[1] * math.sin(radians)
            self.pen.goto(x, y)
        
        if text:
            self.pen.penup()
            self.pen.goto(center[0] + move_text[0], center[1] + move_text[1])
            self.pen.color(color)
            self.pen.write(text, align="center", font=("Arial", int(text_thickness), "bold"))

    #Metoda wyszukująca dany punkt an elipsie po danym procencie długość od prawej strony poruszając się odwrotnie do ruchu zegara
    def find_point_on_ellipse(self, center, radius, percent):
        angle_rad = percent * 2 * math.pi
            
        x = center[0] + radius[0] * math.cos(angle_rad)
        y = center[1] + radius[1] * math.sin(angle_rad)

        return (x, y)


    #Metoda rysująca krzywe - wykorzystuje mechanizm Krzywej Beziera:
    def display_bezier_curve(self, start_point, control_point_1, end_point, p2=None, color_b="black", thickness=3):
        self.pen.penup()
        self.pen.goto(start_point)
        self.pen.pendown()
        self.pen.color(color_b)
        self.pen.pensize(thickness)
        
        if p2 is None:
            for i in range(1, self.line_accuracy + 1):
                time = i / self.line_accuracy
                x = (1 - time)**2 * start_point[0] + 2 * (1 - time) * time * control_point_1[0] + time**2 * end_point[0]
                y = (1 - time)**2 * start_point[1] + 2 * (1 - time) * time * control_point_1[1] + time**2 * end_point[1]
                self.pen.goto(x, y)
        else:
            for i in range(1, self.line_accuracy + 1):
                time = i / self.line_accuracy
                x = (1-time)**3 * start_point[0] + 3 * (1-time)**2 * time * control_point_1[0] + 3 * (1-time) * time**2 * p2[0] + time**3 * end_point[0]
                y = (1-time)**3 * start_point[1] + 3 * (1-time)**2 * time * control_point_1[1] + 3 * (1-time) * time**2 * p2[1] + time**3 * end_point[1]
                self.pen.goto(x, y) 

    #Metoda służąca do automatycznego tworzenia krzywych Beziera na podstawie danych: punkt startowy i punkt końcowy 
    #oraz wspołczyniki na podstawie wykresu geogebry które są proporcjonalnością wzięta z tamtego układu
    def create_bezier_curve(self, start_cordinates, end_cordinates, move_ratio, move_ratio_2=None, color="#2e83f3", thickness=4):
        p0 = start_cordinates
        delta_x = end_cordinates[0]-start_cordinates[0]
        delta_y = end_cordinates[1]-start_cordinates[1]
        if move_ratio_2 is None:
            control_point_1_move_by_start_cordinates = (move_ratio[0] * delta_x, move_ratio[1] * delta_y )
            control_point_1 = (start_cordinates[0] + control_point_1_move_by_start_cordinates[0], start_cordinates[1] + control_point_1_move_by_start_cordinates[1])
            end_point = end_cordinates
            self.display_bezier_curve(p0, control_point_1, end_point, p2=None, color_b=color, thickness=thickness)
        else: 
            control_point_1_move_by_start_cordinates = (move_ratio[0] * delta_x, move_ratio[1] * delta_y )
            control_point_2_move_by_start_cordinates = (move_ratio_2[0] * delta_x, move_ratio_2[1] * delta_y )
            control_point_1 = (start_cordinates[0] + control_point_1_move_by_start_cordinates[0], start_cordinates[1] + control_point_1_move_by_start_cordinates[1])
            control_point_2 = (start_cordinates[0] + control_point_2_move_by_start_cordinates[0], start_cordinates[1] + control_point_2_move_by_start_cordinates[1])
            end_point = end_cordinates
            self.display_bezier_curve(p0, control_point_1, end_point, control_point_2, color_b=color, thickness=thickness)

    #Metoda wyświatlająca kropki na mapie jako dany obiekt
    def display_dot_object(self, x, y, size_object=24, color="black", text="", move=(0, 0), align_text="center", text_thickness=12):
        self.pen.penup()
        self.pen.goto(x, y)
        self.pen.pendown()
        self.pen.dot(size_object, color)
        
        self.pen.penup()
        self.pen.goto(x + move[0], y + move[1])
        self.pen.color(color)
        self.pen.write(text, align=align_text, font=("Arial", int(text_thickness), "bold"))

    #Metoda tworząca mapę
    def create_map(self):
        self.pen.hideturtle()
        
        #stworzenie obiektów korzystających z wzoru krzywej Beziera:
        
        #Linie transferowe:

        #SPS -> LHC (od ALICE)
        self.create_bezier_curve(self.find_point_on_ellipse(self.sps_coords, self.sps_radius, 0.75), self.find_point_on_ellipse(self.lhc_coords, self.lhc_radius, 0.5), (1.2714, -0.3636), move_ratio_2=None, color=self.style.map_trn_line_color, thickness=self.style.map_trn_line_thickness)
        
        #SPS -> LHC (od LHCb)
        self.create_bezier_curve(self.find_point_on_ellipse(self.sps_coords, self.sps_radius, 0.13), self.find_point_on_ellipse(self.lhc_coords, self.lhc_radius, 0.925), (0.55, -2), move_ratio_2=(0.3, 3.2), color=self.style.map_trn_line_color, thickness=self.style.map_trn_line_thickness)
        
        #PS -> SPS 
        self.create_bezier_curve(self.find_point_on_ellipse(self.ps_coords, self.ps_radius, 0.5), self.find_point_on_ellipse(self.sps_coords, self.sps_radius, 0.5), (0.41, 0.31), move_ratio_2=(1.22, -0.4175), color=self.style.map_trn_line_color, thickness=self.style.map_trn_line_thickness)
        
        #BOOSTER -> PS
        self.create_bezier_curve(self.find_point_on_ellipse(self.bst_coords, self.bst_radius, 0.82), self.find_point_on_ellipse(self.ps_coords, self.ps_radius, 0.22), (0.2933, 1.08), move_ratio_2=(0.7167, 0.11), color=self.style.map_trn_line_color, thickness=self.style.map_trn_line_thickness)
        

        #LINAC 4
        self.create_bezier_curve(self.l4_start, self.l4_end, (0.5, 0.93), move_ratio_2=None, color=self.style.map_linac4_color, thickness=self.style.map_linac4_thickness, )
        self.pen.penup()
        self.pen.goto(-70*self.config_layouts["linac4"], -360*self.config_layouts["linac4"])
        self.pen.color(self.style.map_linac4_color)
        self.pen.write("LINAC 4", align="center", font=("Arial", self.style.text_thickness+1, "bold"))
        

        #stworzenie akceleratorów z wzoru na elipse
        self.display_ellipse(self.lhc_coords, self.lhc_radius, self.style.map_lhc_color, self.style.map_lhc_thickness, text="LHC", text_thickness=self.style.text_thickness+2, move_text=(int(0*self.ratio_scale), int(0*self.ratio_scale)))
        self.display_ellipse(self.sps_coords, self.sps_radius, self.style.map_sps_color, self.style.map_sps_thickness, text="SPS", text_thickness=self.style.text_thickness+2, move_text=(int(0*self.ratio_scale), int(-35*self.ratio_scale)))
        self.display_ellipse(self.ps_coords, self.ps_radius, self.style.map_ps_color, self.style.map_ps_thickness, text="PS", text_thickness=self.style.text_thickness+2, move_text=(int(0*self.ratio_scale), int(-15*self.ratio_scale)))
        self.display_ellipse(self.bst_coords, self.bst_radius, self.style.map_bst_color, self.style.map_bst_thickness, text="BOOSTER", text_thickness=self.style.text_thickness+1, move_text=(int(0*self.ratio_scale), int(35*self.ratio_scale)))
    

        #stworzenie oznaczeń detektorów w LHC
        self.display_dot_object(self.lhc_coords[0], self.lhc_coords[1] + self.lhc_radius[1], self.style.background_detectors_thickness, self.style.map_background_color)
        self.display_dot_object(self.lhc_coords[0], self.lhc_coords[1] - self.lhc_radius[1], self.style.background_detectors_thickness, self.style.map_background_color) 
        self.display_dot_object(self.lhc_coords[0] - self.lhc_radius[0], self.lhc_coords[1], self.style.background_detectors_thickness, self.style.map_background_color)
        self.display_dot_object(self.lhc_coords[0] + self.lhc_radius[0], self.lhc_coords[1], self.style.background_detectors_thickness, self.style.map_background_color)
        self.display_dot_object(self.lhc_coords[0], self.lhc_coords[1] + self.lhc_radius[1], self.style.detectors_thickness, self.style.map_detectors_color, "CMS", move=(int(0*self.ratio_scale), int(27*self.ratio_scale)), text_thickness=self.style.text_thickness)
        self.display_dot_object(self.lhc_coords[0], self.lhc_coords[1] - self.lhc_radius[1], self.style.detectors_thickness, self.style.map_detectors_color, "ATLAS", move=(int(0*self.ratio_scale), int(-42*self.ratio_scale)), text_thickness=self.style.text_thickness)
        self.display_dot_object(self.lhc_coords[0] - self.lhc_radius[0], self.lhc_coords[1], self.style.detectors_thickness, self.style.map_detectors_color, "ALICE", move=(int(-62*self.ratio_scale-15), int(-8*self.ratio_scale)), text_thickness=self.style.text_thickness)
        self.display_dot_object(self.lhc_coords[0] + self.lhc_radius[0], self.lhc_coords[1], self.style.detectors_thickness, self.style.map_detectors_color, "LHCb", move=(int(52*self.ratio_scale+15), int(-8*self.ratio_scale)), text_thickness=self.style.text_thickness)
        
        #stworzenie legendy mapy
        legend_label_1 = "Wiązka sterowana przez użytkownika"
        legend_label_2 = "Wiązka sterowana automatycznie"
        
        self.display_dot_object(self.config_layouts["map_legend"][0], self.config_layouts["map_legend"][1], self.style.map_controllable_beam_thickness, self.style.map_controllable_beam_color, legend_label_1, move=(18, -10), align_text="left", text_thickness=self.style.text_thickness)
        self.display_dot_object(self.config_layouts["map_legend"][2], self.config_layouts["map_legend"][3], self.style.map_automated_beam_thickness, self.style.map_automated_beam_color, legend_label_2, move=(18,-10), align_text="left", text_thickness=self.style.text_thickness)


    def show_screen_window(self):
        self.timer_update = None
        try:
            self.root.deiconify()
            self.set_size()  
        except turtle.Terminator:
            pass

    def hide_screen_window(self):
        if self.timer_resize:
            self.root.after_cancel(self.timer_resize)
        if self.timer_update:
            self.root.after_cancel(self.timer_update)

        self.timer_resize = None
        self.timer_update = None

        if self.root.winfo_exists():
            self.root.withdraw()

#Funkcja inicjująca działanie wszystkiego związanego z mapą
def map_main():
    try:
        app = CernMapApp()
        app.show_screen_window()
    except Exception as e:
            print(f"Wykonując komendę system napotkał błąd: {type(e).__name__} \n{str(e)}")
if __name__ == "__main__":
    map_main()