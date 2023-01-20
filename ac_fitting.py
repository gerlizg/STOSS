# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 17:57:30 2023

@author: Silvia Gimenez Santamarina
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import pandas as pd
import numpy as np
import os
import math
from scipy import fftpack
from scipy import optimize
from scipy.signal import find_peaks_cwt

def objective10(x, a, b, c, d, e):
    return a * np.sin( x* 2*np.pi/b ) + c* np.cos( x * 2*np.pi/b ) + d*x - e*d

## reading data
path = "C:\\Users\\Silvia\\WORK\\pbits\\Sfitting"
nums = pd.read_csv(path + "\\data01\\numbers.txt", delimiter=",", skipinitialspace=True,nrows=1)
nums = nums.columns.tolist()
out_f = open(path + "\\fitting_params_d01.txt", "w")
out_f.write("#sin-amplitude\tperiod\tcos-amplitude2\td\te\n")

columns = 1
rows = len(nums)

fig, ax = plt.subplots(rows, columns,squeeze=False, figsize=(5,50),
                       tight_layout=True)
c = 0
for num in nums[:]:
    print(num)
    
    d0_time = np.loadtxt(path + "\\data01\\time_"+num+".csv")
    #d0_B = np.loadtxt(path + "/data01/B_"+num+".csv")
    d0_y = np.loadtxt(path + "\\data01\\y_relaxation_"+num+".csv")

    i = len(d0_time)
    j = 5
    
    x = d0_time[1:i:j] 
    xn= d0_time[1:i:j] 
    y = d0_y[1:i:j] - np.mean(d0_y[1:i])
    #y = d0_B[1:i:j] - np.mean(d0_B[1:i])
    N = len(x)
    mv=30000
    
    if c==0:
        # initial guess
        yhat = fftpack.rfft(y)
        idx = (yhat**2).argmax()
        freqs = fftpack.rfftfreq(N, d = (x[1]-x[0])/(2*np.pi))
        frequency0 = freqs[idx]
        amplitude0 = 50
        period0 = 8931
        d0 = 0.004
        e0 = 16000
        guess_o10 = [-0.3*amplitude0, period0, -0.6*amplitude0, d0 , e0]
                
        # fitting
        (amplitude1_o10, frequency1_o10, amplitude2_o10, d, e), pcov = optimize.curve_fit(
            objective10, x, y, guess_o10,maxfev = mv)
        print("Fitted params obj10:", amplitude1_o10, frequency1_o10, amplitude2_o10, d, e)
    
    else:
        frequency0 = frequency1_o10
        amplitude01 = amplitude1_o10
        amplitude02 = amplitude2_o10
        period0 = frequency1_o10
        d0 = d
        e0 = e
        guess_o10 = [amplitude0, period0, amplitude0, d0 , e0]
        
        # fitting
        (amplitude1_o10, frequency1_o10, amplitude2_o10, d, e), pcov = optimize.curve_fit(
            objective10, x, y, guess_o10,maxfev = mv)
        print("Fitted params obj10:", amplitude1_o10, frequency1_o10, amplitude2_o10, d, e)
        
    
    # Calculate new y points
    yn6 = objective10(xn, amplitude1_o10, frequency1_o10, amplitude2_o10, d, e)
    
    # error
    ss_res = sum((yn6 - y)**2)
    ss_tot = sum((y - np.mean(y))**2)
    r_square = 1 - (ss_res/ss_tot)      
    print("R: ", r_square)         
    
    out_f.write("{}\t{:>.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\n".format(c,amplitude1_o10, frequency1_o10, amplitude2_o10, d, e))
    
    # plotting           
    ax[c,0].scatter(x,y, alpha=.3, label="calc")
    ax[c,0].plot(xn,yn6, linewidth=2, 
                 color="red", label="fit")
    ax[c,0].set_title("N. " + str(c) + "; T= " + str(num),
                      weight='bold', )
    ax[c,0].set_ylabel("# spins")
    ax[c,0].set_xlabel("Time, $t$(s)")
    ax[c,0].set_xticks([])
    ax[c,0].grid(True)
    
    c+=1

fig.align_ylabels()
plt.savefig(path+"\\fig_fittings.png", dpi=330)
out_f.close()