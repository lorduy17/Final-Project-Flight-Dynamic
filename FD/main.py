import tkinter as tk
from objeto import maya
from interfaz import Interfaz

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rotación STL con sliders")

    obj = maya()
    app = Interfaz(root, obj)

    root.mainloop()

    