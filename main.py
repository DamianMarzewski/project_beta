import time
from commands import *
from objects import User
def main():
    gracz = User()
    logowanie = AuthorizationPanel(gracz)
    panel = ControlPanel()
    
    logowanie.do_cls("cls")
    logowanie.cmdloop()
    
    time.sleep(2)
    
    panel.do_cls("cls")
    panel.cmdloop()

if __name__ == "__main__":
    main()