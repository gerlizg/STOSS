#	Main Code

#-------------------------------------------------
#                   FUNCTIONS
#-------------------------------------------------

from read_data import *
from mag_relaxation import *
from Bolztman_distribution import *
from Bolztman_distribution_bit2 import *
from changeable_field import *
from changeable_field_bit2 import *
from constant_field import *
from frequency import *
from curve_fitting import *
from td import *
import time


#--------------------------------------------------------------------
#                   CONFIGURATIONS
#--------------------------------------------------------------------

option = 0                                  # 1: changeable field; 0: constant field 
option_2spin = 1                            # 1: yes; 0: no
N_ex = 1000                                 # Number of Spins
flag = 23                                   # System index in the data set
T = 20                                      # Temperature, Kelvin
B = 0.01                                    # Applied magnetic field, Tesla. If only option = 0
B_max = 0.00025	                            # Maximum applied magnetic field, Tesla. If only option = 1
B_pbit2 = 0.2                               # Applied magnetic field, Tesla. If only option = 2
save =1                                     # 1: for saving results; 0: for not saving results
cycles = 4                                  # Changeable field applied. If only option = 1 
starting_mode = 0                           # Starting mode for all the spins (0.5 = 50% spins in the lower state of energy) 
repicable_exp = 0                           # 1: to plant a seed; 0: for random results
tau_exp = 50                                # Tau value of the exponential curve
total_time = 3 * 1000                       # Total Time of the experiment
probability = 1.9998                        # Probability of state changing (each time step), % 

 
'''
Do not change any part of the program below
'''
#-----------------------------------------------------------
# Studying the interaction of spin-spin:
#-----------------------------------------------------------
if option_2spin == 1 :
    N_ex = 1  
    starting_mode = 0
    number2 = 600
    
#------------------
#   Timer:
#------------------
t0 = time.time() 

#-----------------------------------------------------------
#   Reading the data set:
#-----------------------------------------------------------
compound_constants, g_Dy, name, number = read_data (flag)

#--------------------------------------------------------------------
#   Mean Magnetic relaxation time through Raman, Orbach, & QTM:
#--------------------------------------------------------------------
step, tau_mag, time_steps = mag_relaxation (compound_constants, T, option, tau_exp, total_time)

#--------------------------------------------------------------------
#   Obtaining the spin distribution in each state:
#--------------------------------------------------------------------
t, B, P_ij, P_i, x, y, E = Bolztman_distribution (B_max, [], g_Dy, T, time_steps, step, option, B, cycles, probability)

#--------------------------------------------------------------------
#   To changeable or constant field, we have:
#--------------------------------------------------------------------
if option == 1:
    Rt, Rt_1, Rt_0, cambios, N_zeros_percent, y_relaxation,  Matrix  = changeable_field (N_ex, time_steps, step,  t, B, x, y, save, repicable_exp, starting_mode, option)

else:
    Rt, Rt_1, Rt_0, cambios, N_zeros_percent, y_relaxation, Matrix = constant_field (N_ex, time_steps, step, t, B, x, y, save, repicable_exp, starting_mode)

#--------------------------------------------------------------------
#   Graphics:
#--------------------------------------------------------------------

#   For relaxation curve:
a_rel, tau_rel, c_rel = curve_fitting ('Relaxation_curve', T, x, y, name, number, t, y_relaxation, P_i, 2,option, N_ex, time_steps, B, time_steps, E, P_ij )

#--------------------------------------------------------------------
#   If we want to see the effect of one spin on another:
#--------------------------------------------------------------------

if option_2spin == 1:
    
    Matrix = [item for sublist in Matrix for item in sublist]
    option = 2 
    
    #--------------------------------------------------------------------
    t, B2, P_ij2, P_i2, x2, y2, E2  = Bolztman_distribution (B_pbit2, Matrix, g_Dy, T, time_steps, step, option, B, cycles, probability)
    Rt2, Rt_12, Rt_02, cambios2, N_zeros_percent2, y_relaxation2, Matrix_1 = changeable_field (N_ex, time_steps, step,  t, B2, x2, y2, save, repicable_exp, starting_mode, option)
    #--------------------------------------------------------------------
    Matrix_1 = [item for sublist in Matrix_1 for item in sublist]
    
    #--------------------------------------------------------------------
    itera = np.arange(start = 0, stop = number2)
    value = np.zeros(number2)
    v00 = np.zeros(number2)
    v01 = np.zeros(number2)
    v10 = np.zeros(number2)
    v11 = np.zeros(number2)
    
    for i in range (0, number2,1):
        value[i], v00[i], v01[i], v10[i], v11[i] = td(i, Matrix,Matrix_1)
       
    results = pd.DataFrame(list(zip(itera, value, v00, v01, v10, v11 ))) 
    
    # adding column name to the respective columns:
    results.columns =['Time Delay', 'Correlation', '0-0', '0-1', '1-0', '1-1']
    
    if save == 1 :
        results.to_csv('Correlation_results.csv', index=False, sep =';')
    
    r2 = np.arange(start = 0, stop = number2)
    plt.rcParams["figure.figsize"] = [18, 14]
    plt.rcParams["figure.autolayout"] = True
    plt.plot(r2, value, linewidth = 1.5, color = "red")
    plt.xlabel("Delay time")
    plt.ylabel("r2")
    plt.legend(loc='upper right')
    plt.grid()
    plt.savefig('correlacion')
    plt.show()

    r2_copy = pd.DataFrame(r2)
    r2_copy.to_csv('units.csv', index=False)

    value_copy = pd.DataFrame(value)
    value_copy.to_csv('correlation.csv', index=False)
    #--------------------------------------------------------------------

#------------------
#   Timer:
#------------------
t1 = time.time()        #   Timer Finishing
time = (t1-t0)/60       #   Total Time

#-------------------------------------------------
#   DataFrames:
#-------------------------------------------------
# list of strings:

if option == 0: 
    lst_names = ['Compound name', 'Spins', 'Temperature', 'Relaxation Time', 'Time step',
           'Steps', 'Spins without changes', 'Magnetic Field', 'Boltzman Distribution',
           'Lower state probability', 'Tau (relaxation curve)',
           'Processing time']
    units = ['-', '-', 'Kelvin', 'seconds', 'seconds',
           '-', '%', 'Tesla', '-',
           '-','seconds', 'seconds',
           'seconds', 'seconds',
           'minutes']

    lst_values = [name, N_ex, T, tau_mag, step, time_steps, N_zeros_percent, B, P_ij,
           P_i, tau_rel, time]

else:

    lst_names = ['Compound name', 'Spins', 'Temperature', 'Relaxation Time', 'Time step',
           'Steps', 'Spins without changes', 'Magnetic Field', 'Processing time']
    units = ['-', '-', 'Kelvin', 'seconds', 'seconds',
           '-', '%', 'Tesla', 'minutes']

    lst_values = [name, N_ex, T, tau_mag, step, time_steps, N_zeros_percent,'variable', 
           time]

#-------------------------------------------------
# Calling DataFrame constructor after zipping
# both lists, with columns specified
#-------------------------------------------------
df = pd.DataFrame(list(zip(lst_names, units, lst_values)),
               columns =['Name', 'Units', 'Value'])

df.to_csv('Results.csv', index=False)

print(df)








