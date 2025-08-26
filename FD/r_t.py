import numpy as np


class operaciones:
    def __init__(self):
        self.phi = 0
        self.theta = 0
        self.psi = 0
        self.alpha = 0
        self.beta = 0
        self.u = 0
        self.v = 0
        self.w = 0
        
    def L_bv(self,phi:float,theta:float,psi:float):
        # Transformation matriz for get body coordinates from vehicle coordintate
        return np.array([
            [np.cos(theta)                                                  ,np.cos(theta)*np.sin(psi)                                          ,-np.sin(theta)],
            [np.sin(phi)*np.sin(theta)*np.cos(psi)-np.cos(phi)*np.sin(psi)  ,np.sin(phi)*np.sin(theta)*np.sin(psi)+np.cos(theta)*np.cos(psi)    ,np.sin(phi)*np.cos(theta)],
            [np.cos(phi)*np.sin(theta)*np.cos(psi)+np.sin(phi)*np.sin(psi)  ,np.cos(phi)*np.sin(theta)*np.sin(psi)-np.sin(phi)*np.cos(psi)      ,np.cos(phi)*np.cos(theta)]
        ])
        
    def L_bw(self,alpha:float,beta:float):
        # Transformation matriz for get body coordinates from wind coordintate
        return np.array([
            [np.cos(alpha)*np.cos(-beta)    ,np.cos(alpha)*np.sin(-beta)    ,-np.sin(alpha)],
            [-np.sin(-beta)                 ,np.cos(beta)                   ,0],
            [np.sin(alpha)*np.cos(-beta)    ,np.sin(alpha)*np.sin(-beta)    ,np.cos(alpha)]
        ])
   

# if __name__ == "__main__":


    


    