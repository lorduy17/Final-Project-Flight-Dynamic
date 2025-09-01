import tkinter as tk
from objeto import maya
from interfaz import Interfaz
import os

if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear')
    root = tk.Tk()
    root.title("3D STL Viewer")
    app = Interfaz(root)

    root.mainloop()


    
