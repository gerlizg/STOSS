# **********************************************************************
#                       	STOSS
# ********************************************************************** 

#----------------------
Necessary files:
#----------------------

1) Main.py (Part of the code where the user specifies the parameters)
2) read_data.py (Description of the system)
3) mag_relaxation.py (Relaxation Mechanisms, Total probability for spin flipping)
4) Bolztmann_distribution.py (Zeeman effect, Boltzmann distribution, single probabilities to pass from 0 to 1, and vice versa)
5) mean_matrix_state.py (For a two p-bit network, where the collective state is studied in this function)
6) asociation.py (For a two p-bit network, the association factor is calculated)
7) plotting.py (Graphical Representation of the results)
8) full_data_file.csv (File which contains all the information for few systems, from the work: Data-driven design of molecular nanomagnets [1]

#----------------------
Modules from python:
#----------------------

1) numpy
2) matplotlib.pyplot
3) pandas 
4) scipy.optimize
5) Collections (Counter)
6) random
7) math
8) time

#----------------------
Options for the user:
#----------------------

In this version of STOSS we are capable to simulate three main scenarios:

1) Magnetization decays at different temperatures at constant magnetic field.
2) Magnetization decays at different temperatures at changeable magnetic field.
3) Magnetization decays at different temperatures of two p-bit networks.

Considering this idea, the user can select the type of simulation just writing the values in each variable. 

# GENERAL CONFIGURATIONS:
#-------------------------------------
N_ex = 1000                             # Number of Spins of each p-bit
T = 20/1000                             # Temperature, K
save = 0                                # 1: for saving results; 0: no
flag = 28                               # System to be studied from SIMDAVIS database
starting_mode = 0.5                     # Starting mode for all the spins (0.5 = 50% spins in the lower state of energy)
time_steps = 2000                       # Total time steps
option = 1                              # 1: changeable field; 0: constant field 
option_2spin = 0                        # 1: yes; 0: no for the study of a p-bit network

# CONSTANT MAGNETIC FIELD:
#-------------------------------------
B_constant = 0                          # Applied magnetic field, Tesla. If only "option" = 0

# CHANGEABLE MAGNETIC FIELD:
#-------------------------------------
B_max = 0.00025                         # Maximum value for Magnetic Field, Tesla. If only "option" = 1
cycles = 4                              # Changeable field applied. If only "option" = 1 

# TWO P-BIT NETWORK:
#-------------------------------------
B_pbit2 = 0.02                          # Applied magnetic field, Tesla. If only "option_2spin" = 1
B_constant = 0                          # Applied magnetic field, Tesla. If only "option" = 0
factor = 100                            # Threshold for the definition of the collective state of each p-bit. If only "option_2spin" = 1
asociation_factor = time_steps          # How many delays the program will take into account
step_asociation_factor = 1              # How many steps of delay the program will take into account to reach the value of the previous variable

#------------------------------------
Relaxation Mechanisms STOSS uses: 
#------------------------------------

1) Raman: C*(T^n)
2) Quantum Tunnelling of Magnetization
3) Orbach

#------------------------------------
To cite this work:
#------------------------------------
Lanthanide molecular nanomagnets as probabilistic bits [arXiv:2301.08182].
STOSS is a Markov Chain Monte Carlo model employed to simulate, with the same parameters, 
magnetization decay at all temperatures and hysteresis at all temperatures, 
given the physical parameters of the system.

#------------------------------------
References:
#------------------------------------

[1] Data-driven design of molecular nanomagnets. 
Yan Duan, Lorena E. Rosaleny, Joana T. Coutinho, Silvia Giménez-Santamarina, Allen Scheie, José J. Baldoví, Salvador Cardona-Serra & Alejandro Gaita-Ariño. 
Nature Communications volume 13, Article number: 7626 (2022). 
https://chemistrycommunity.nature.com/posts/data-driven-design-of-molecular-nanomagnets 

#----------------------------------------------------------------------------
Any kind of question from this code, please contact: gerliz.gutierrez@uv.es
#----------------------------------------------------------------------------