#-------------------------------------------------
#            MODULES FROM PYTHON
#-------------------------------------------------

import numpy as np
import pandas as pd
import random                   

#-------------------------------------------------

def changeable_field (N_ex, time_steps, step, t, B, x, y, save, starting_mode, B_pbit2, flag, factor, option_2spin):

	#-------------------------------------------------
    #   Defining the parameters:
    #-------------------------------------------------
    
    swap = {0: 1, 1:0}                  # Function that returns the value 
    conditional = int (N_ex/factor)
    
    #-------------------------------------------------
    #   Creating the lists:
    #-------------------------------------------------

    Matrix = np.zeros((N_ex, time_steps), dtype=np.uint8)           # Contains all the states (0, 1)  
    up = np.zeros ((time_steps))                                    # Spins in the excited state 
    down = np.zeros ((time_steps))                                  # Spins in the ground state 
    difference = np.zeros((time_steps))
    B_2pbit = np.zeros((time_steps)) 
    
    #-------------------------------------------------                
    #   Iteration over the Matrix
    #-------------------------------------------------
    
    # Initializating the spins in a specific state:
    
    for i in range (0, int (N_ex * starting_mode)):
        Matrix [i, 0] = Matrix [i, 0] + 1
       
    # For each spin:
    
    for i in range(0, N_ex):
        
                    
        random_n = [np.random.uniform(0, 1) for i in range(time_steps)]
        
        # For each step:
                     
        for j in range(1, time_steps):
         
            if B[j]>=0:  # Positive Magnetic Field
            
                # Changing the state from 1 to 0:
                
                if random_n [j]<x[j] and Matrix[i,j-1]== 1:    
                    Matrix[i,j] = swap[Matrix[i,j-1]]
                                        
                # Changing the state from 0 to 1:
                
                elif random_n [j]<y[j] and Matrix[i,j-1]== 0:  
                    Matrix[i,j] = swap[Matrix[i,j-1]]
                                        
                else:
                    Matrix[i,j] = Matrix[i,j-1]
                    
            else:       # Negative Magnetic Field
            
                # Changing the state from 1 to 0:
                
                if random_n [j]<y[j] and Matrix[i,j-1]== 1:    
                    Matrix[i,j] = swap[Matrix[i,j-1]]
                                      
                # Changing the state from 0 to 1:
                
                elif random_n [j]<x[j] and Matrix[i,j-1]== 0:  
                    Matrix[i,j] = swap[Matrix[i,j-1]]
                                        
                else:
                    Matrix[i,j] = Matrix[i,j-1]
           
    #-------------------------------------------------    
    #   Relaxation curve:
    #-------------------------------------------------
    
    column = np.sum (Matrix, axis = 0).tolist()
    y_relaxation = [N_ex - i for i in column]
    
    if option_2spin == 1:
        
        for i in range (0, time_steps):
            down [i] = y_relaxation [i] 
            up[i] = N_ex - down [i]
            difference [i] = up [i] - down [i]
            
            if difference [i] >= conditional:                           
                B_2pbit [i] = B_2pbit [i] + B_pbit2
                   
        mean_value = np.mean (B_2pbit)
        B_2pbit = B_2pbit - mean_value
	
    #-------------------------------------------------
    #   Saving the data 
    #-------------------------------------------------
     
    if save == 1:    
        
        if flag == 2:
            extension = '_2.csv'
        else: 
            extension = '_1.csv'
        
        Matrix_copy = pd.DataFrame(Matrix)
        Matrix_copy.to_csv('Matrix_'+ extension, index=False)
      
        y_relaxation_copy = pd.DataFrame(y_relaxation)
        y_relaxation_copy.to_csv('y_relaxation_' + extension, index=False)
                
        time_copy = pd.DataFrame(t)
        time_copy.to_csv('time_' + extension, index=False)
              
        B_copy = pd.DataFrame(B)
        B_copy.to_csv('B_' + extension, index=False)
        
        if option_2spin == 1: 
            B_copy = pd.DataFrame(B_2pbit)
            B_copy.to_csv('B_' + extension, index=False)
 
    #--------------------------------------------------------------------
    return y_relaxation, Matrix, B_2pbit, up, down, difference, conditional
    #--------------------------------------------------------------------   
    
  
  
    