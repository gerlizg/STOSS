#-------------------------------------------------
#             LIBRERIES & FUNCTIONS
#-------------------------------------------------
import numpy as np
import pandas as pd
import scipy.optimize as opt
import random                   

#-------------------------------------------------
def constant_field (N_ex, time_steps, step, t, B, x, y, save, replicable_exp, starting_mode):
	
    #-------------------------------------------------
	#   Defining the parameters:
    #-------------------------------------------------
    swap = {0: 1, 1:0}                        #Function that returns the value 
    seeds = np.arange(start = 0, stop = N_ex) #Repicable experiment     
    
    #-------------------------------------------------
    #   Creating the lists:
    #-------------------------------------------------      
    changes = int (0.08*time_steps)          #Sets the size of some matrixs
    Matrix = np.zeros((N_ex, time_steps))    #Contains all the states (0, 1) 
    
    changes_m = np.zeros(N_ex)           #Save all state changes 
    state_1 = np.zeros(N_ex)             #Save all state changes from 0 to 1 
    state_0 = np.zeros(N_ex)             #Save all state changes from 1 to 0
    Rt_1 = np.zeros((N_ex,changes))      #Residence Times of states 1
    Rt_0 = np.zeros((N_ex,changes))      #Residence Times of states 0
    
    R_time = np.zeros((N_ex,time_steps)) #Residence Time for all the states
    Rt = np.zeros((N_ex,changes))        #Final Residence Times 
    
    Rt_final_0 = np.zeros(N_ex)          #Final Residence Times of states 0
    Rt_final_1 = np.zeros(N_ex)          #Final Residence Times of states 1
                       
    #-------------------------------------------------                
    #   Iteration over the Rt matrix
    #-------------------------------------------------
    for i in range (0, int (N_ex * starting_mode)):
        Matrix [i, 0] = Matrix [i, 0] + 1
       
    for i in range(0,N_ex):
        
        if replicable_exp == 1:
            np.random.seed(seeds[i])        #Takes the seed

        random_n = [np.random.uniform(0, 1) for i in range(time_steps)]
        c = 0   # Counter for 1 state
        b = 0   # Counter for Rt 
        a = 0   # Counter for 0 state

        for j in range(1,time_steps):
         
            if j == 1:      #Only for the second step
                if random_n [j]<0.01:  #Given the condition:
                    Matrix[i,j] = swap[Matrix[i,j-1]]       #Swaps the state 
                    changes_m [i] = changes_m [i] + 1       #Adding up the change
                    R_time [i,j] = 0                        #Restarts the conter
                    Rt [i,b] = R_time [i,j-1]               #Saves the previus Res Time
                    state_1 [i] = state_1 [i] + 1           #Saves the change in Rt_1 list
                    b = b + 1
                    
                else:       #If not, everything stays the same
                    Matrix[i,j] = Matrix[i,j-1]
                    R_time [i,j] = R_time [i,j-1] + 1
            
            else:
                            #Changing the state from 1 to 0:
                if random_n [j]<x and Matrix[i,j-1]== 1:    
                    Matrix[i,j] = swap[Matrix[i,j-1]]
                    changes_m [i] = changes_m [i] + 1
                    state_0 [i] = state_0 [i] + 1                    
                    R_time [i,j] = 0
                    Rt [i,b] = R_time [i,j-1]
                    Rt_1 [i,a] = Rt [i,b] 
                    b = b + 1
                    a = a + 1
                    
                            #Changing the state from 0 to 1:
                elif random_n [j]<y and Matrix[i,j-1]== 0:  
                    Matrix[i,j] = swap[Matrix[i,j-1]]
                    changes_m [i] = changes_m [i] + 1 
                    state_1 [i] = state_1 [i] + 1
                    R_time [i,j] = 0
                    Rt [i,b] = R_time [i,j-1]
                    Rt_0 [i,c] = Rt [i,b]
                    c = c + 1
                    b = b + 1
                    
                else:
                    Matrix[i,j] = Matrix[i,j-1]
                    R_time [i,j] = R_time [i,j-1] + 1
                    if j == time_steps-1:
                        if Matrix[i,j] == 1:
                            Rt_final_1[i] = R_time [i,j]                           
                        else:
                            Rt_final_0[i] = R_time [i,j]
     
    #-------------------------------------------------
    #   Counting spins without changing:
    #-------------------------------------------------
    N_zeros = np.count_nonzero (changes_m == 0.0)
    N_zeros_percent = N_zeros * 100/N_ex    

    #-------------------------------------------------    
    #   Relaxation curve:
    #-------------------------------------------------
    column = np.sum (Matrix,axis=0).tolist()
    y_relaxation = [N_ex - i for i in column]
    
	#-------------------------------------------------
    #   SAVING CREATED DATA 
    #-------------------------------------------------
       
    if save == 1:
        Matrix_copy = pd.DataFrame(Matrix)
        Matrix_copy.to_csv('Matrix.csv', index=False)
        
        R_time_copy = pd.DataFrame(R_time)
        R_time_copy.to_csv('R_time.csv', index=False)

        Rt_copy = pd.DataFrame(Rt)
        Rt_copy.to_csv('Rt.csv', index=False)
        
        Rt_1_copy = pd.DataFrame(Rt_1)
        Rt_1_copy.to_csv('Rt1.csv', index=False)
        
        Rt_0_copy = pd.DataFrame(Rt_0)
        Rt_0_copy.to_csv('Rt0.csv', index=False)
        
        state_0_copy = pd.DataFrame(state_0)
        state_0_copy.to_csv('state_0.csv', index=False)
        
        state_1_copy = pd.DataFrame(state_1)
        state_1_copy.to_csv('state_1.csv', index=False)

        Rt_final_0_copy = pd.DataFrame(Rt_final_0)
        Rt_final_0_copy.to_csv('Rt_final_0.csv', index=False)
        
        Rt_final_1_copy = pd.DataFrame(Rt_final_1)
        Rt_final_1_copy.to_csv('Rt_final_1.csv', index=False)
        
        y_relaxation_copy = pd.DataFrame(y_relaxation)
        y_relaxation_copy.to_csv('y_relaxation.csv', index=False)
        
        time_copy = pd.DataFrame(t)
        time_copy.to_csv('time.csv', index=False)
        
    #--------------------------------------------------------------------
    return Rt, Rt_1, Rt_0, changes_m, N_zeros_percent, y_relaxation, Matrix 
        
    
  
  
    