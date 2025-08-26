import numpy as np

class matriz_rotacion:
    def __init__(self):
        self.phi = 0
        self.theta = 0
        self.psi = 0
    def L(self,phi,theta,psi):
        self.L = np.array([
            [np.cos(theta)                                                  ,np.cos(theta)*np.sin(psi)                                          ,-np.sin(theta)],
            [np.sin(phi)*np.sin(theta)*np.cos(psi)-np.cos(phi)*np.sin(psi)  ,np.sin(phi)*np.sin(theta)*np.sin(psi)+np.cos(theta)*np.cos(psi)    ,np.sin(phi)*np.cos(theta)],
            [np.cos(phi)*np.sin(theta)*np.cos(psi)+np.sin(phi)*np.sin(psi)  ,np.cos(phi)*np.sin(theta)*np.sin(psi)-np.sin(phi)*np.cos(psi)      ,np.cos(phi)*np.cos(theta)]
        ])

