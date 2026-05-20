class Colors:
    #Metoda przekonwertująca kolor HEX na formatowanie ANSII
    def convert_hex_to_ansii(hex_color):
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"\033[38;2;{r};{g};{b}m"
    
    #Restart formatu ANSII
    clear = "\033[0m"

    #Formatowanie tekstu ANSII
    bold = "\033[1m"
    cursive = "\033[3m"
    underline = "\033[4m"
    pulse = "\033[5m"
    strike = "\033[9m"
    
    #Kolory zdefiniowane w postaci formatowania ANSII
    prefix_cmd = convert_hex_to_ansii("#1648C6")
    errors = convert_hex_to_ansii("#B11616")
    help = convert_hex_to_ansii("#087C1F")
    help2 = convert_hex_to_ansii("#0CDA32")
