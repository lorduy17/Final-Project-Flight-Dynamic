import numpy as np




class operations:

    def __init__(self):
        self.phi = 0
        self.theta = 0
        self.psi = 0
        self.alpha = 0
        self.beta = 0
        self.gamma = 0
        self.wind = np.array([0,0,0])
        
    def rot_x(self,phi):
        self.phi = phi
        c = np.cos( (phi))
        s = np.sin( (phi))
        return np.array([[1, 0, 0],
                         [0, c, -s],
                         [0, s, c]])
    
     
    def rot_y(self,theta):
        self.theta = theta
        c = np.cos( (theta))
        s = np.sin( (theta))
        return np.array([[c, 0, s],
                         [0, 1, 0],
                         [-s, 0, c]])
    
     
    def rot_z(self,psi):
        self.psi = psi
        c = np.cos( (psi))
        s = np.sin( (psi))
        return np.array([[c, -s, 0],
                         [s, c, 0],
                         [0, 0, 1]])
    
    def update_state(self,alpha,beta,gamma,wind):

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.wind = wind
 

    
    def state_actual(self,):

        return print(
            "********  STATE ACTUAL  *******",'\n'
            "------------------------------", '\n'
            "Angles,                  deg" '\n'
            "------------------------------" '\n'
            "AoA, alpha:              ",np.rad2deg(self.alpha), '\n'
            "Slideslipe angle, beta:  ",np.rad2deg(self.beta), '\n'
            "Climb angle, gamma:      ",np.rad2deg(self.beta), '\n'
            "------------------------------"  '\n'
            "Attitude: Euler angles,  rads" '\n'
            "------------------------------" '\n'
            "psi:                     ",self.psi, '\n'
            "theta:                   ",self.theta, '\n'
            "phi:                     ",self.phi, '\n'
            "------------------------------"  '\n'
            "Velocities body,         km/h" '\n'
            "------------------------------" '\n'
            "u:                       ",self.wind[0], '\n'
            "v:                       ",self.wind[1],'\n'
            "w:                       ",self.wind[2], '\n'
            "------------------------------"  '\n'
            # "Angular rates,           rad/s" '\n'
            # "------------------------------" '\n'
            # "p:                       ",self.p, '\n'
            # "q:                       ",self.q,'\n'
            # "r:                       ",self.r, '\n'
        )
         
    
    



    
    @staticmethod 
    def mult_matrix(*matrices):
        result = np.eye(3)
        for matrix in matrices:
            result = result @ matrix
        return result
    
    @staticmethod
    def normalized(v):

        return v / np.linalg.norm(v)
    
