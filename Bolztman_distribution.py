#-------------------------------------------------
#             LIBRERIES & FUNCTIONS
#-------------------------------------------------
from solve import *
from solve2 import *
import numpy as np
import scipy.optimize as opt
import math

#--------------------------------------------------------------------
def Bolztman_distribution (B_max, Matrix_0, g_Dy, T, time_steps, step, option, B_constant, cycles, probability):

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
    miu_B = 0.67167                 #Bohr magneton
    total_gap = 2                       
    Mj = 7.5         
    t = np.arange(start = 0, stop = (time_steps*step)+step, step = step)    #Time vector
    t = t [0:time_steps]
    vao = np.zeros(2)               
    vao [0] = probability
    
    if option != 0:                 #Changeable field or two pbits network
    
        #--------------------------------------------------------------------    
        #   Creating the vectors that will contain each step value:
        #--------------------------------------------------------------------
        B = np.zeros(time_steps)    #Magnetic field
        P_ij = np.zeros(time_steps) #Bolztman distribution
        P_i = np.zeros(time_steps)  #Probability for "i" state 
        x = np.zeros(time_steps)    #Probability of changing to state 1
        y = np.zeros(time_steps)    #Probability of changing to state 0
        E = np.zeros(time_steps)    #Energy
        
        #--------------------------------------------------------------------
        #   Iteration Process:
        #--------------------------------------------------------------------
        
        for i in range (0, time_steps):
        
            if option == 1:
                #Calculating the field using the cosine function:
                #B = Bmax (amplitude) * cos (time[i]*360/time_steps )
                B[i] = B_max + (B_max * math.cos (i * cycles * 2 * math.pi / time_steps))
            else:
                #Calculating the field using the result for the pbit1:
                B[i] = B_max * Matrix_0[i] 
            
            #Calculating the energy through the equation 1
            E[i] = (total_gap * Mj * g_Dy * miu_B * B[i])
            
            #Calculating the Bolztman distribution       
            P_ij[i] = 1 / (np.exp(E[i]/T))
            vao [1] = P_ij[i]
                       
            #Taking the single probabilities for one state and the other one
            solution =  opt.fsolve(solve, (0.5, 0.5), P_ij[i])
            P_i[i] = solution [0]
                  
            #Calculating the ratio between the two states for changing
            x[i], y[i] =  opt.fsolve(solve2, (vao [0]/2, vao [0]/2), vao)

            
    else:             #Constant field                             
    
        #Calculating the energy through the equation 1
        E = total_gap * Mj * g_Dy * miu_B * B_constant
        
        #Calculating the Bolztman distribution       
        P_ij = 1/(np.exp(E/T))
        vao [1] = P_ij
               
        #Taking the single probabilities for one state and the other one
        solution =  opt.fsolve(solve, (0.5, 0.5), P_ij)
        P_i = solution [0]
        
        #Calculating the ratio between the two states for changing
        x, y =  opt.fsolve(solve2, (vao [0]/2, vao [0]/2), vao)
  
        B = B_constant
        
  

    #--------------------------------------------------------------------
    return t, B, P_ij, P_i, x, y, E
        

        
 
    
    
    