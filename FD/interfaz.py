import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
from r_t import operaciones
from objeto import maya



class Interfaz():
    def __init__(self,master,objeto):
        self.master = master
        self.objeto = objeto
        self.opn = operaciones()

        self.sld_original = None

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111,projection='3d')

        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH,expand=True)


        # Frames
        frm_inputs = tk.Frame(master)
        frm_inputs.pack(fill="x", pady=5)


        ## Euler angles Frames
        self.entry_phi = self.crear_entry(frm_inputs, "phi (°):")
        self.entry_theta = self.crear_entry(frm_inputs, "theta (°):")
        self.entry_psi = self.crear_entry(frm_inputs, "psi (°):")
        ## Aerodynamic angles Frames
        self.entry_alpha = self.crear_entry(frm_inputs, "alpha (°):")
        self.entry_beta = self.crear_entry(frm_inputs, "beta (°):")
        ## wind vector Frames
        self.entry_u = self.crear_entry(frm_inputs, "u m/s:")
        self.entry_v = self.crear_entry(frm_inputs, "v m/s:")
        self.entry_w = self.crear_entry(frm_inputs, "w m/s:")

        for entry in [self.entry_phi, self.entry_theta, self.entry_psi,
                      self.entry_alpha, self.entry_beta,
                      self.entry_u, self.entry_v, self.entry_w]:
            entry.bind("<Return>", self.update_plot)
            
        # Actualizar
        btn_update = tk.Button(master, text="Actualizar rotación", command=self.update_plot)
        btn_update.pack(pady=5)

        self.update_plot()

    # Entradas
    def crear_entry(self, parent, label_text):
    
        frame = tk.Frame(parent)
        frame.pack(side="left", padx=5)
        lbl = tk.Label(frame, text=label_text)
        lbl.pack()
        entry = tk.Entry(frame, width=6)
        entry.insert(0, "0")  # valor inicial
        entry.pack()
        
        return entry
    
   
    # Actualiza plot
    def update_plot(self,_=None):
        if not self.objeto.ruta_stl:
            return
        try:
            # Obtener valores
            phi = np.radians(float(self.entry_phi.get()))
            theta = np.radians(float(self.entry_theta.get()))
            psi = np.radians(float(self.entry_psi.get()))
            alpha = np.radians(float(self.entry_alpha.get()))
            beta = np.radians(float(self.entry_beta.get()))
            u = float(self.entry_u.get())
            v = float(self.entry_v.get())
            w = float(self.entry_w.get())

            wind = [u,v,w]
        except ValueError:
            print("Valores incorrectos")
            return

        if wind is not None and len(wind) == 3:
            norm_wind = np.linalg.norm(wind)

            if wind[0] != 0 and norm_wind != 0:
                alpha = np.arctan(wind[2]/wind[0])
                beta = np.arcsin(wind[1]/norm_wind)
            else:
                alpha = 0
                beta = 0
        else:
            alpha = 0
            beta = 0

        # Rotación del cuerpo
        matriz_rot = self.opn.L_bv(phi,theta,psi)@self.opn.L_bw(alpha,beta)
        sld_original = self.objeto.solido() 
        n_tri = sld_original.shape[0]
        sld_flat = sld_original.reshape(-1,3).T
        sld_r = matriz_rot@sld_flat
        sld_r = sld_r.T.reshape(n_tri,3,3)

        # Redibujar
        self.ax.clear()
        self.ax.grid(False)
        self.ax.set_axis_off()
        coleccion = Poly3DCollection(sld_r, alpha=0.7, facecolor="lightblue", edgecolor="k")
        self.ax.add_collection3d(coleccion)

        x_min, y_min,z_min = np.min(sld_r.reshape(-1,3),axis=0)
        x_max, y_max,z_max = np.max(sld_r.reshape(-1,3),axis=0)
        self.ax.set_xlim(x_min,x_max)
        self.ax.set_ylim(y_min,y_max)
        self.ax.set_zlim(z_min,z_max)
        self.ax.set_box_aspect([x_max-x_min,y_max-y_min,z_max-z_min])

        # Origen fijo
        origen_fijo = np.array([0, 0, 0])  # esquina inferior del modelo
        longitud = 0.5 * max(x_max - x_min, y_max - y_min, z_max - z_min)
        self.ax.quiver(*origen_fijo, longitud, 0, 0, color='r')
        self.ax.quiver(*origen_fijo, 0, longitud, 0, color='g')
        self.ax.quiver(*origen_fijo, 0, 0, longitud, color='b')
        self.ax.text(*origen_fijo + [longitud, 0, 0], "X", color="r", weight="bold")
        self.ax.text(*origen_fijo + [0, longitud, 0], "Y", color="g", weight="bold")
        self.ax.text(*origen_fijo + [0, 0, longitud], "Z", color="b", weight="bold")

        self.ax.view_init(elev=20, azim=30)

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rotación STL con entradas")

    obj = maya()  # Esto abrirá el diálogo para cargar el STL
    app = Interfaz(root, obj)

    btn_cargar = tk.Button(root, text="Cargar STL", command=lambda: [obj.carga_archivo(), app.update_plot()])
    btn_cargar.pack()

    root.mainloop()

