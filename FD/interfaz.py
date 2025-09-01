

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
from r_t import operations
from objeto import maya



class Interfaz():
    def __init__(self,master):
        self.master = master
        self.objeto = maya()
        self.opn = operations()

        self.entries = {}
        
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        # canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create entries
        self.create_entries()

        # Buttons
        self.create_buttons()

        # Init values
        self.wind_norm = np.array([0,0,0])
    
    # Wigets
    def create_entries(self):
        frame = tk.Frame(self.master)
        frame.pack(pady=5)

        # Euler angles
        euler_frame = tk.LabelFrame(frame, text="Euler Angles")
        euler_frame.pack(side="left", padx=10)
        for key in ["phi(°)", "theta(°)", "psi(°)"]:
            self.add_entry(euler_frame, key)

        # Aerodynamic Angles
        aero_frame = tk.LabelFrame(frame, text="Aerodynamic Angles")
        aero_frame.pack(side="left", padx=10)
        
        for key in ["alpha(°)", "beta(°)", "gamma(°)"]:
            self.add_entry(aero_frame, key)

        # Body
        wind_frame = tk.LabelFrame(frame, text="Body")
        wind_frame.pack(side="left", padx=10)
        for key in ["u m/s", "v m/s", "w m/s"]:
            self.add_entry(wind_frame, key)    

        # Across Wind
        aw_frame = tk.LabelFrame(frame, text="Wind Across")     
        aw_frame.pack(side="left",padx=10)
        for key in ["wind_x m/s","wind_y m/s","wind_z m/s"]:
            self.add_entry(aw_frame, key)
        
        # Gamma input
        self.gamma_input_var = tk.BooleanVar()
        self.gamma_input_var.set(False)

        tk.Checkbutton(aero_frame, text="Gamma es entrada",
                       variable=self.gamma_input_var).pack()

    def add_entry(self,parent,label_text):
        frame = tk.Frame(parent)
        frame.pack(pady=2)
        tk.Label(frame, text=label_text).pack()
        entry = tk.Entry(frame, width=10)
        entry.insert(0, "0")
        entry.pack()
        self.entries[label_text] = entry

    def create_buttons(self):
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Load STL", command=self.load_stl).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Update Rotation", command=self.update_plot).pack(side=tk.LEFT, padx=5)
   

    def load_stl(self):
        filename = filedialog.askopenfilename(title="Select STL file",
            filetypes=[("STL files", "*.stl")])
        if filename:
            self.objeto.file_load(filename)
            self.update_plot()


    
    def set_axes_equal(self):
        '''Set 3D plot axes to equal scale.'''
        x_limits = self.ax.get_xlim3d()
        y_limits = self.ax.get_ylim3d()
        z_limits = self.ax.get_zlim3d()

        x_range = abs(x_limits[1] - x_limits[0])
        x_middle = np.mean(x_limits)
        y_range = abs(y_limits[1] - y_limits[0])
        y_middle = np.mean(y_limits)
        z_range = abs(z_limits[1] - z_limits[0])
        z_middle = np.mean(z_limits)

        plot_radius = 0.5 * max([x_range, y_range, z_range])

        self.ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
        self.ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
        self.ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])


    def update_plot(self):
        if self.objeto.get_normalized_vertices() is None:
            return
        
        vectors = self.objeto.get_normalized_vertices().reshape(-1,3,3)
        try:

            self.phi = np.deg2rad(float(self.entries["phi(°)"].get()))
            self.theta = -np.deg2rad(float(self.entries["theta(°)"].get()))
            self.psi = np.deg2rad(float(self.entries["psi(°)"].get()))
            self.alpha = np.deg2rad(float(self.entries["alpha(°)"].get()))
            self.beta = np.deg2rad(float(self.entries["beta(°)"].get()))
            self.gamma = np.deg2rad(float(self.entries["gamma(°)"].get()))
            u = float(self.entries["u m/s"].get())
            v = float(self.entries["v m/s"].get())
            w = float(self.entries["w m/s"].get())
            wind_x = float(self.entries["wind_x m/s"].get())
            wind_y = float(self.entries["wind_y m/s"].get())
            wind_z = float(self.entries["wind_z m/s"].get())

            # R_euler calc
            if np.linalg.norm([self.phi,self.theta,self.psi]) != 0:
                R_euler = self.opn.mult_matrix(
                    self.opn.rot_x(self.phi),
                    self.opn.rot_y(self.theta),
                    self.opn.rot_z(self.psi)
                    )
            else:
                R_euler = np.eye(3)
            

            # R_aero calc
            awind = np.array([wind_x,wind_y,wind_z])
            wind = np.array([u, v, w]) - awind
         
            if np.linalg.norm(wind) == 0: ## For case 1
                alpha = 0
                beta = 0
                gamma = self.theta
                R_aero = np.eye(3)

            else: 
                self.wind_norm = operations.normalized(wind)
                if wind[2] == 0:
                    alpha = 0
                    beta = np.arcsin(self.wind_norm[1])
                    
                    gamma = self.theta - alpha
                else:
                    alpha = np.arctan2(self.wind_norm[2],self.wind_norm[0])
                    beta = np.arcsin(self.wind_norm[1])
                    
                    if self.gamma_input_var.get():
                        gamma = self.theta - alpha
                        self.theta = self.gamma + self.alpha
                    else:
                        gamma = 0

            self.alpha = alpha 
            self.beta = beta
            self.gamma = gamma
            

            R = R_euler

            self.opn.update_state(
                self.alpha,
                self.beta,
                self.gamma,
                wind
            )

            print(self.opn.state_actual())
                    
        except ValueError:
            print("Invalid input")
            return
        
        vectors_rot = vectors.reshape(-1,3) @ R.T
        vectors_rot = vectors_rot.reshape(vectors.shape)

        

        # Draw
        self.ax.clear()
        self.ax.grid(True)
        self.ax.set_axis_off()
        
        poly = Poly3DCollection(vectors_rot, alpha=0.7,
                                facecolor="lightblue",
                                edgecolor="k")
        

        self.ax.add_collection3d(poly)
        self.ax.set_box_aspect([1,1,1])  
        self.set_axes_equal()

        # NED fixed
        NED = np.array([[1, 0, 0],
                        [0, -1, 0],
                        [0, 0, -1]])
        NED = R @ NED

        self.ax.quiver(0, 0, 0, NED[0,0], NED[1,0], NED[2,0], color='g', length=1.4, normalize=True)
        self.ax.quiver(0, 0, 0, NED[0,1], NED[1,1], NED[2,1], color='g', length=1.4, normalize=True)
        self.ax.quiver(0, 0, 0, NED[0,2], NED[1,2], NED[2,2], color='g', length=1.4, normalize=True)
        self.ax.text(NED[0,0], NED[1,0], NED[2,0], 'X', color='g')
        self.ax.text(NED[0,1], NED[1,1], NED[2,1], 'Y', color='g')
        self.ax.text(NED[0,2], NED[1,2], NED[2,2], 'Z', color='g')

        ## X fixed

        self.ax.quiver(0,0,0, 1,0,0, color='magenta', length=1.4, normalize=True)
        self.ax.text(1,0,0, 'Xs', color='magenta')

    


        # Show wind vector
        if np.linalg.norm(self.wind_norm) != 0:
            v_r = self.wind_norm
            self.ax.quiver(0,0,0, 
                           v_r[0],v_r[1],v_r[2],
            color="lightblue",linewidth = 2, length=1.3, normalize=True)
            self.ax.text(v_r[0],v_r[1],v_r[2],
                 'Wind', color='lightblue')

        
         # Initial view
        self.ax.view_init(elev=20., azim=-30)
        self.canvas.draw()


# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("3D STL Viewer")
#     app = Interfaz(root)
#     root.mainloop()

        
