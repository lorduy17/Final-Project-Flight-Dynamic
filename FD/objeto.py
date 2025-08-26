import numpy as np
from stl import mesh
import tkinter as tk
from tkinter import filedialog

class maya():

    def __init__(self):
        self.ruta_stl = None

    def carga_archivo(self):
        self.ruta_stl = filedialog.askopenfilename(title="Selecciona archivo STK",filetypes=[("Archivos STL","*stl")])
        if not self.ruta_stl:
            raise ValueError("No se seleccionó archivo STL")
       
    def solido(self):
        if not self.ruta_stl:
            raise ValueError("No hay archivo STL cargado")
        
        modelo = mesh.Mesh.from_file(self.ruta_stl)
        return modelo.vectors
    

