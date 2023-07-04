#-------------------------------------------------
#            MODULES FROM PYTHON
#-------------------------------------------------

import matplotlib.pyplot as plt
import pandas as pd
import time

#-------------------------------------------------
#            SUPPORTING FILES
#-------------------------------------------------

from read_data import *
from mag_relaxation import *
from Bolztmann_distribution import *
from changeable_field import *
from plotting import *
from mean_matrix_state import *
from association import *

#------------------------------------------------------------------------------------------------
#                           SETTING PARAMETERS BY THE USER
#-----------------------------------------------------------------------------------------------

# GENERAL CONFIGURATIONS:
#-------------------------------------
N_ex = 1000000                                      # Number of Spins of each p-bit
T = 4                                               # Temperature, K
save = 1                                            # 1: for saving results; 0: no
flag = 25                                           # System to be studied from SIMDAVIS database
starting_mode = 0.5                                 # Starting mode for all the spins (0.5 = 50% spins in the lower state of energy)
time_steps = 10000                                  # Total time steps
option = 0                                          # 1: changeable field; 0: constant field 
option_2spin = 1                                    # 1: yes; 0: no for the study of a p-bit network

# CONSTANT MAGNETIC FIELD:
#-------------------------------------
B_constant = 0                                      # Applied magnetic field, Tesla. If only "option" = 0

# CHANGEABLE MAGNETIC FIELD:
#-------------------------------------
B_max = 0.00025                                     # Maximum value for Magnetic Field, Tesla. If only "option" = 1
cycles = 4                                          # Changeable field applied. If only "option" = 1 

# TWO P-BIT NETWORK:
#-------------------------------------
B_pbit2 = 0.02                              # Applied magnetic field, Tesla. If only "option_2spin" = 1
factor = 1000                               # Threshold for the definition of the collective state of each p-bit. If only "option_2spin" = 1
association_factor = time_steps             # How many delays the program will take into account
step_association_factor = 1                 # How many steps of delay the program will take into account to reach the value of the previous variable

#-----------------------------------------------------------

#------------------
#   Timer:
#------------------

t0 = time.time() 

#-----------------------------------------------------------
#   Reading the data set:
#-----------------------------------------------------------

compound_constants, g_Dy, sample_ID = read_data (flag)


#--------------------------------------------------------------------
#   Mean Magnetic relaxation time through Raman, Orbach, & QTM:
#--------------------------------------------------------------------

step, tau_mag, probability, total_time = mag_relaxation (compound_constants, T, time_steps, sample_ID)

#--------------------------------------------------------------------
#   Obtaining the spin distribution in each state:
#--------------------------------------------------------------------

t, B_1, P_ij_1, x_1, y_1, E_1 = Bolztmann_distribution (B_max, [], g_Dy, T, time_steps, step, option, B_constant, cycles, probability, total_time)

#--------------------------------------------------------------------
#   To changeable or constant field, we have:
#--------------------------------------------------------------------

y_relaxation_1, Matrix_1, B_2pbit_1, up_1, down_1, difference_1, conditional = changeable_field (N_ex, time_steps, step, t, B_1, x_1, y_1, save, starting_mode, B_pbit2, option, factor, option_2spin)

print ('-------------------------------------------------')
print ('First p-bit has finished')
print ('-------------------------------------------------')
print ('*************************************************')

#--------------------------------------------------------------------
#   For p-bit network:
#--------------------------------------------------------------------

if option_2spin == 1:
       
    flag = 2

    t, B_2, P_ij_2, x_2, y_2, E_2 = Bolztmann_distribution (B_max, B_2pbit_1, g_Dy, T, time_steps, step, flag, B_1, cycles, probability, total_time)
      
    y_relaxation_2, Matrix_2, B_2pbit_2, up_2, down_2, difference_2, conditional = changeable_field (N_ex, time_steps, step, t, B_2, x_2, y_2, save, starting_mode, B_pbit2, flag, factor, option_2spin)
    
    print ('-------------------------------------------------')
    print ('Second p-bit has finished')
    print ('-------------------------------------------------')
    print ('*************************************************')
    
    state_1 = mean_matrix_state (difference_1, N_ex, time_steps, factor, 1, save)
    state_2 = mean_matrix_state (difference_2, N_ex, time_steps, factor, 2, save)

    print ('-------------------------------------------------')
    print ('Starting association analysis between both p-bits:')
    print ('-------------------------------------------------')
    print ('*************************************************')
    
    results, x_vector, association_results = association (association_factor, state_1, state_2, save, step_association_factor)
    
    print ('-------------------------------------------------')
    print ('Association analysis:')
    print ('-------------------------------------------------')
    print ('*************************************************')
    print (results)
    print ('*************************************************')

else:
    
    x_vector, association_results, B_2, y_relaxation_2, state_1, state_2 = 0, 0, 0, 0, 0, 0

#--------------------------------------------------------------------
#   Plotting the results
#-------------------------------------------------------------------- 

plotting (T, option, N_ex, B_1, B_2,  y_relaxation_1, y_relaxation_2, option_2spin, t, conditional, B_pbit2, state_1, state_2, x_vector, association_results, association_factor, save)    

#------------------
#   Timer:
#------------------
t1 = time.time()        #   Timer Finishing
time = (t1-t0)/60       #   Total Time

print ('Time processing: ', time, ' minutes')
       
#-------------------------------------------------
#   DataFrames:
#-------------------------------------------------

lst_names = ['Compound ID', 'Spins', 'Temperature', 'Relaxation Time', 'Time step',
       'Steps', 'Processing time']
units = ['-', '-', 'Kelvin', 'seconds', 'seconds',
       '-', 'minutes']

lst_values = [sample_ID, N_ex, T, tau_mag, step, time_steps, time]

#-------------------------------------------------
# Calling DataFrame constructor after zipping
# both lists, with columns specified
#-------------------------------------------------
df = pd.DataFrame(list(zip(lst_names, units, lst_values)),
               columns =['Name', 'Units', 'Value'])

if save == 1:
    df.to_csv('Results.csv', index=False)

print ('*************************************************')
print ('-------------------------------------------------')
print ('Information about the simulation:')
print ('-------------------------------------------------')
print ('')
print(df)


    