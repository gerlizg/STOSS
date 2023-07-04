#-------------------------------------------------
#            MODULES FROM PYTHON
#-------------------------------------------------

import numpy as np
import math
import scipy.optimize as opt

#--------------------------------------------------------------------

def solve (vars, vao):
        x, y = vars
        eq1 = (x+y)-(vao [0])
        eq2 = (x/y)-(vao [1])
        return [eq1, eq2]

#--------------------------------------------------------------------

def Bolztmann_distribution (B_max, Matrix_0, g_Dy, T, time_steps, step, option, B_constant, cycles, probability, total_time):

    '''
    The equation was obtained from the paper: Relaxation Dynamics and Magnetic
    Anisotropy in a Low-Symmetry DyIII Complex.
    Authors: Lucaccini, Briganti, Perfetti, Vendier, Costes, Totti,Sessoli,Sorace.
    Page: 4/11, equation (2).

    Hs = miu_B * S_eff * g * B 

    The energy of an arrangement increases, the probability decreseas.
    At very high energies, the probability never quite reaches zero, but 
    becomes very small. 

    Relative probability of two different states:
    P(i)/P(j) = e^((Ej-Ei)/(kBT))  (*)

    Where i denotes ground state and j excited one
	'''
    
    #--------------------------------------------------------------------
    #   Defining the parameters:
    #--------------------------------------------------------------------
    
    miu_B = 0.67167                                             # Bohr magneton                      
    Mj = 7.5                                                    # Spin Projection       
    t = np.arange(start = 0, stop = total_time, step = step)    # Time vector
    t= t[0:time_steps]
    
    # Vector that will contain the probability for spin flipping
    vao = np.zeros(2)               
    vao [0] = probability
    
    #--------------------------------------------------------------------    
    #   Creating vectors:
    #--------------------------------------------------------------------
    
    B = np.zeros(time_steps)                # Magnetic field
    x = np.zeros(time_steps)                # Probability of changing to state 1
    y = np.zeros(time_steps)                # Probability of changing to state 0
      
    if option != 0:  # Changeable field or two pbits network
    
        #--------------------------------------------------------------------
        #   Iterative Process
        #--------------------------------------------------------------------

        P_ij = np.zeros(time_steps)         # Bolztman distribution 
        E = np.zeros(time_steps)            # Energy
            
        for i in range (0, time_steps):
        
            if option == 1:
                
                # Calculating the field using the cosine function:
                # Where B = Bmax (amplitude) * cos (time[i]*360/time_steps )
                B[i] = B_max * math.cos ((math.pi/2)+ (i * cycles * 2 * math.pi / time_steps))
                
            else:
                
                # Calculating the field using the result for the pbit1:
                B[i] = Matrix_0[i] 
            
            # Calculating the energy through the equation 1:
            E[i] = abs(2 * Mj * g_Dy * miu_B * B[i])
            
            # Calculating the Bolztmann distribution:       
            P_ij[i] = 1 / (np.exp(E[i]/T))
            vao [1] = P_ij[i]
                  
            # Calculating the ratio between the two states for changing:
            x[i], y[i] =  opt.fsolve(solve, (vao [0]/2, vao [0]/2), vao)

            
    else:  # Constant field                             
    
        # Calculating the energy through the equation 1:
        E = 2 * Mj * g_Dy * miu_B * B_constant

        # Calculating the Bolztmann distribution:       
        P_ij = 1/(np.exp(E/T))
        vao [1] = P_ij

        # Calculating the ratio between the two states for changing:
        xx, yy =  opt.fsolve(solve, (vao [0]/2, vao [0]/2), vao)
  
        for i in range (0, time_steps):
            
            x[i], y[i], B[i] = xx, yy, B_constant
        
    #--------------------------------------------------------------------
    return t, B, P_ij, x, y, E      
    #--------------------------------------------------------------------
        
 
    
    
    