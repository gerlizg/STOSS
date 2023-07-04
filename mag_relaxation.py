#-------------------------------------------------
#            MODULES FROM PYTHON
#-------------------------------------------------

import numpy as np
from math import factorial

#-------------------------------------------------------------------------------------------------

def total_probability (tau_exp):

    number = tau_exp
    probability = 0

    for i in range (1, 25):
        temp = 1/((number**i) * factorial (i))
        if i %2 == 0:
            probability = probability - temp
        else:
            probability = probability + temp
    
    #--------------------------------------------------------------------        
    return probability
    #--------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------

def mag_relaxation (compound_constants, T, time_steps, sample_ID):

        '''
        With this function we can see how the three mechanisms of 
        magnetic relaxation process behave. 
        --------------------------------------------------------------------------
        
        C = (s^-1)(K^-n)
        n = Raman parameter
        tau_0 = Normalization Constant, (s)
        Ueff = Effective Demagnetization Barrier (-DeltaE/Kb), (K)
        tau_QTM = Process that not depends on T, (s^-1)
        
        --------------------------------------------------------------------------
        
        Equation: Raman + Orbach + Quantum tunneling of magnetization
        
        --------------------------------------------------------------------------
        Tau-1 = C·T^n + tau_0^-1exp(-Ueff/T) + tau_QTM^-1 (1)
        
        '''
        
        #--------------------------------------------------------------------------
        # Constants's compounds:
        #--------------------------------------------------------------------------
        
        Ueff, tau_0, C, n, tau_QTM = compound_constants 
        
        #--------------------------------------------------------------------------
        # Relaxation time of magnetization, (s):
        #--------------------------------------------------------------------------
        
        if tau_QTM == 0:
            tau_mag = ((((C)*(T**n)))+(((np.exp(-Ueff/T))/tau_0)))**-1
        else:
            tau_mag = ((((C)*(T**n)))+(tau_QTM**-1)+(((np.exp(-Ueff/T))/tau_0)))**-1
        
        total_time = (tau_mag * 20)
        
        
        print ('-------------------------------------------------')
        print ('Sample ID: ', sample_ID)
        print ('Relaxation Time: %.5f sec at %.4f K' % (tau_mag, T))
        print ('-------------------------------------------------')
        print ('*************************************************')
             
        #--------------------------------------------------------------------------
        # Steps calculated from the total time:
        #--------------------------------------------------------------------------
        
        step = total_time/time_steps
        tau_exp = tau_mag/step
        probability  = total_probability (tau_exp)  

        #--------------------------------------------------------------------
        return step, tau_mag, probability, total_time 
        #--------------------------------------------------------------------