# STOSS
Stochastic Spin Simulator

This simulator is part of the supporting information file from the article: Lanthanide molecular nanomagnets as probabilistic bits. 

Modules that are needed:
* Pandas
* Numpy
* Scipy
* Math
* Random
* Time
* Matplotlib

The script is written using Python Programming Language.

The next list shows the parameter that could be changed by the user (main.py):
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
save = 1                                     # 1: for saving results; 0: for not saving results
cycles = 4                                  # Changeable field applied. If only option = 1 
starting_mode = 0                           # Starting mode for all the spins (0.5 = 50% spins in the lower state of energy) 
repicable_exp = 0                           # 1: to plant a seed; 0: for random results
total_time = 3 * 1000                       # Total Time of the experiment, s

