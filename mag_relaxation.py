#-------------------------------------------------
#             LIBRERIES & FUNCTIONS
#-------------------------------------------------
import numpy as np

#-------------------------------------------------
def mag_relaxation (compound_constants, T, option, tau_exp, total_time):

        '''
        With this function we can see how the three pathways of 
        magnetic relaxation process behave. 

        C = (s^-1)(K^-n)
        n = Raman parameter
        tau_0 = Normalization Constant, (s)
        Ueff = Effective Demagnetization Barrier (-DeltaE/Kb), (K)
        tau_QTM = Process that not depends on T, (s^-1)

        Equation: Raman + Orbach + Quantum tunneling of magnetization

        Tau-1 = C·T^n + tau_0^-1exp(-Ueff/T) + tau_QTM^-1 (1)
        '''
        
        #--------------------------------------------------------------------------
        # Constants's compounds:
        #--------------------------------------------------------------------------
        Ueff, tau_0, C, n, tau_QTM = compound_constants 
        
        #--------------------------------------------------------------------------
        # Relaxation time of magnetization, (s):
        #--------------------------------------------------------------------------
        tau_mag = ((((C)*(T**n)))+(tau_QTM**-1)+(((np.exp(-Ueff/T))/tau_0)))**-1
        
        #--------------------------------------------------------------------------
        # Constants:
        #--------------------------------------------------------------------------
        step = (tau_mag/tau_exp)
        
        #--------------------------------------------------------------------------
        # Time steps calculated from the total time:
        #--------------------------------------------------------------------------
        time_steps = int(total_time/step)+1 
        
        #--------------------------------------------------------------------
        return step, tau_mag, time_steps