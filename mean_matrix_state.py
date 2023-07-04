#-------------------------------------------------
#            MODULES FROM PYTHON
#-------------------------------------------------

import numpy as np
import pandas as pd

#-------------------------------------------------

def mean_matrix_state (difference, N_ex, time_steps, factor, flag, save):
    
    #-------------------------------------------------    
    # Obtaining the collective behaviour through the threshold
    #-------------------------------------------------
    
    state = np.zeros((time_steps))  
    
    for i in range (0, time_steps):
       if difference [i] >= int(N_ex/factor):
            state [i] = 1
            
    if flag == 1:
        extension = '_1.csv'
    else:
        extension = '_2.csv'
    
    if save == 1:
        
        state_copy = pd.DataFrame(state)
        state_copy.to_csv('state'+ extension, index=False)
    
    #-------------------------------------------------        
    return state
    #-------------------------------------------------