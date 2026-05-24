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

#Dostęp do orgazinera stylami
style = Styling()

WIDTH = 0.85
HEIGHT = 0.85
#Funkcja inicjująca dziłanie graficznego okna 
def screen_config(w, h):
    screen = turtle.Screen()
    screen.setup(width=w, height=h)
    screen.title("Schemat Akceleratorów CERN")
    screen.bgcolor(f"{style.map_background_color}")
    screen.tracer(0) 
    screen.setworldcoordinates(-800, -500, 800, 500)
    return screen

#Funkcja rysująca elipse
def display_ellipse(pen, center, radius, color, thickness, text="", move_text=(0,0)):
    pen.penup()
    pen.goto(center[0] + radius[0], center[1])
    pen.pendown()
    pen.color(color)
    pen.pensize(thickness)
    
    for i in range(1441):
        radians = math.radians(i / 4.0)
        x = center[0] + radius[0] * math.cos(radians)
        y = center[1] + radius[1] * math.sin(radians)
        pen.goto(x, y)
        
    if text:
        pen.penup()
        pen.goto(center[0] + move_text[0], center[1] + move_text[1])
        pen.color(color)
        pen.write(text, align="center", font=("Arial", 14, "bold"))

#Funkcja wyszukująca dany punkt po danym procencie długość od prawej strony poruszając się odwrotnie do ruchu zegara
def find_point_on_ellipse(center, radius, percent):
    angle_rad = percent * 2 * math.pi
        
    x = center[0] + radius[0] * math.cos(angle_rad)
    y = center[1] + radius[1] * math.sin(angle_rad)

    return (x, y)

'''
Ważna uwaga!
Krzywa Beziera to funckja wektorowa 
(wykorzystuje mechaniki algebry liniowej, która należy do matematyki wyższej, więc niestety nie zgłebiałem się w jej działanie matematyczne - za mało czasu), 

Oto jej wzór:
B(t) = ((1-t)^3)*p0 + 3((1-t)^2) * t * p1 + 3(1-t) * (t^2) * p2 + t^3 * p3
B(t) = ((1 - t)^2) *p0 + 2(1 - t) * t * p1 + t^2 * p3

gdzie p0, p1, p2, p3 to punkty

Dzięki wzorowi można modelować różne krzywe np. za pomocą narzędzia Geogebra
'''

#Funkcja rysująca krzywe - wykorzystuje mechanizm Krzywej Beziera:
def display_bezier_curve(pen, p0, p1, p3, p2=None, color_b="black", thickness_b=3):
    pen.penup()
    pen.goto(p0)
    pen.pendown()
    pen.color(color_b)
    pen.pensize(thickness_b)
    
    line_accuracy = 500
    
    if p2 is None:
        for i in range(1, line_accuracy + 1):
            time = i / line_accuracy
            x = (1 - time)**2 * p0[0] + 2 * (1 - time) * time * p1[0] + time**2 * p3[0]
            y = (1 - time)**2 * p0[1] + 2 * (1 - time) * time * p1[1] + time**2 * p3[1]
            pen.goto(x, y)
    else:
        for i in range(1, line_accuracy + 1):
            time = i / line_accuracy
            x = (1-time)**3 * p0[0] + 3 * (1-time)**2 * time * p1[0] + 3 * (1-time) * time**2 * p2[0] + time**3 * p3[0]
            y = (1-time)**3 * p0[1] + 3 * (1-time)**2 * time * p1[1] + 3 * (1-time) * time**2 * p2[1] + time**3 * p3[1]
            pen.goto(x, y) 

#Funkcja służąca do automatycznego tworzenia krzywych Beziera
def create_bezier_curve(pen, start_cordinates, end_cordinates, move_ratio, move_ratio_2=None, color="#2e83f3", thickness=4):
    p0 = start_cordinates
    delta_x = end_cordinates[0]-start_cordinates[0]
    delta_y = end_cordinates[1]-start_cordinates[1]
    if move_ratio_2 is None:
        p1_move_by_start_cordinates = (move_ratio[0] * delta_x, move_ratio[1] * delta_y )
        p1 = (start_cordinates[0] + p1_move_by_start_cordinates[0], start_cordinates[1] + p1_move_by_start_cordinates[1])
        p3 = end_cordinates
        display_bezier_curve(pen, p0, p1, p3, p2=None, color_b=color, thickness_b=thickness)
    else: 
        p1_move_by_start_cordinates = (move_ratio[0] * delta_x, move_ratio[1] * delta_y )
        p2_move_by_start_cordinates = (move_ratio_2[0] * delta_x, move_ratio_2[1] * delta_y )
        p1 = (start_cordinates[0] + p1_move_by_start_cordinates[0], start_cordinates[1] + p1_move_by_start_cordinates[1])
        p2 = (start_cordinates[0] + p2_move_by_start_cordinates[0], start_cordinates[1] + p2_move_by_start_cordinates[1])
        p3 = end_cordinates
        display_bezier_curve(pen, p0, p1, p3, p2, color_b=color, thickness_b=thickness)

#Runkcja wyświatlająca kropki na mapie jako dany obiekt
def display_dot_object(pen, x, y, size_object=24, color="black", text="", move_x=0, move_y=16, align_text="center"):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.dot(size_object, color)
    
    pen.penup()
    pen.goto(x + move_x, y + move_y)
    pen.color(color)
    pen.write(text, align=align_text, font=("Arial", 12, "bold"))

#Funkcja tworząca mapę
def create_map():
    pen = turtle.Turtle()
    pen.hideturtle()
    
    #współrzędne akceleratorów i ich promienie
    lhc_coords, lhc_radius = (0, 175), (630, 220)
    sps_coords, sps_radius = (60, 10), (330, 110) 
    ps_coords, ps_radius = (220, -325), (130, 45)     
    bst_coords, bst_radius = (105, -225), (65, 22)  
    l4_start, l4_end = (-60, -340), find_point_on_ellipse(bst_coords, bst_radius, 0.75)
    
    #stworzenie obiektów korzystających z wzoru krzywej Beziera
    
    #Linie transferowe:

    #SPS -> LHC (od ALICE)
    create_bezier_curve(pen, find_point_on_ellipse(sps_coords, sps_radius, 0.75), find_point_on_ellipse(lhc_coords, lhc_radius, 0.5), (1.2714, -0.3636), move_ratio_2=None, color=style.map_trn_line_color, thickness=style.map_trn_line_thickness)
    
    #SPS -> LHC (od LHCb)
    create_bezier_curve(pen, find_point_on_ellipse(sps_coords, sps_radius, 0.13), find_point_on_ellipse(lhc_coords, lhc_radius, 0.925), (0.55, -2), move_ratio_2=(0.3, 3.2), color=style.map_trn_line_color, thickness=style.map_trn_line_thickness)
    
    #PS -> SPS 
    create_bezier_curve(pen, find_point_on_ellipse(ps_coords, ps_radius, 0.5), find_point_on_ellipse(sps_coords, sps_radius, 0.5), (0.41, 0.31), move_ratio_2=(1.22, -0.4175), color=style.map_trn_line_color, thickness=style.map_trn_line_thickness)
    
    #BOOSTER -> PS
    create_bezier_curve(pen, find_point_on_ellipse(bst_coords, bst_radius, 0.82), find_point_on_ellipse(ps_coords, ps_radius, 0.22), (0.2933, 1.08), move_ratio_2=(0.7167, 0.11), color=style.map_trn_line_color, thickness=style.map_trn_line_thickness)
    

    #LINAC 4
    create_bezier_curve(pen, l4_start, l4_end, (0.5, 0.93), move_ratio_2=None, color=style.map_linac4_color, thickness=style.map_linac4_thickness)
    pen.penup()
    pen.goto(-70, -360)
    pen.color(style.map_linac4_color)
    pen.write("LINAC 4", align="center", font=("Arial", 12, "bold"))
    

    #stworzenie akceleratorów z wzoru na elipse
    display_ellipse(pen, lhc_coords, lhc_radius, style.map_lhc_color, style.map_lhc_thickness, "LHC", (0, 0))
    display_ellipse(pen, sps_coords, sps_radius, style.map_sps_color, style.map_sps_thickness, "SPS", (0, -35))
    display_ellipse(pen, ps_coords, ps_radius, style.map_ps_color, style.map_ps_thickness, "PS", (0, -15))
    display_ellipse(pen, bst_coords, bst_radius, style.map_bst_color, style.map_bst_thickness, "BOOSTER", (0, 35))
   

    #stworzenie oznaczeń detektorów w LHC
    display_dot_object(pen, lhc_coords[0], lhc_coords[1] + lhc_radius[1], 40, style.map_background_color)
    display_dot_object(pen, lhc_coords[0], lhc_coords[1] - lhc_radius[1], 40, style.map_background_color) 
    display_dot_object(pen, lhc_coords[0] - lhc_radius[0], lhc_coords[1], 40, style.map_background_color)
    display_dot_object(pen, lhc_coords[0] + lhc_radius[0], lhc_coords[1], 40, style.map_background_color)
    display_dot_object(pen, lhc_coords[0], lhc_coords[1] + lhc_radius[1], 30, style.map_detectors_color, "CMS", move_x=0, move_y=20)
    display_dot_object(pen, lhc_coords[0], lhc_coords[1] - lhc_radius[1], 30, style.map_detectors_color, "ATLAS", move_x=0, move_y=-35)
    display_dot_object(pen, lhc_coords[0] - lhc_radius[0], lhc_coords[1], 30, style.map_detectors_color, "ALICE", move_x=-55, move_y=-8)
    display_dot_object(pen, lhc_coords[0] + lhc_radius[0], lhc_coords[1], 30, style.map_detectors_color, "LHCb", move_x=45, move_y=-8)
    
    #stworzenie legendy mapy
    legend_label_1 = "Wiązka sterowana przez użytkownika"
    legend_label_2 = "Wiązka sterowana automatycznie"
    
    display_dot_object(pen, -330, -420, style.map_controllable_beam_thickness, style.map_controllable_beam_color, legend_label_1, move_x=18, move_y=-10, align_text="left")
    display_dot_object(pen, 30, -420, style.map_automated_beam_thickness, style.map_automated_beam_color, legend_label_2, move_x=18, move_y=-10, align_text="left")
    
#Funkcja inicjująca działanie wsyztskiego związanego z mapą
def map_main():
    screen = screen_config(w=WIDTH, h=HEIGHT)
    create_map()
    screen.update() 
    screen.exitonclick()

if __name__ == "__main__":
    map_main()
