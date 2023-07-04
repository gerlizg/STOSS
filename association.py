#-------------------------------------------------
#            MODULES FROM PYTHON
#-------------------------------------------------

from collections import Counter
import numpy as np
import pandas as pd

#-------------------------------------------------

def td (number, spin1, spin2):

    spin2 = spin2 [number:-1]
    spin1 = spin1 [0:len(spin2)]

    sp1_sp2 = list (map(lambda x,y: (x,y), spin1,spin2))
     
    rr = Counter(sp1_sp2)
    
    checking = {(0.0, 1.0), (1.0, 0.0), (1.0, 1.0), (0.0, 0.0)}
    
    # Preventing error message:
    for i in checking:
        if i not in rr:
            rr.update({i:0.02})
    
    # Sorting the dictionary:
    # r2 = {(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)}        
    r2 = [rr[x] for x in sorted(rr.keys())]
    
    # Calculating each term from the asociation factor equation
    N1 = r2[2] + r2[3]
    N2 = r2[0] + r2[1]
    N3 = r2[0] + r2[2]
    N4 = r2[1] + r2[3]
    
    asociation = ((r2[0] * r2[3]) - (r2[1] * r2[2]))/((N1 * N2 * N3 * N4)**(0.5))
    
    #-------------------------------------------------
    return asociation, r2[0], r2[1], r2[2], r2[3]    
    #-------------------------------------------------

#-------------------------------------------------

def association (number, Matrix_1, Matrix_2, save, step):

    itera = np.arange(start = 0, stop = number, step = step)
    value = np.zeros(number)
    v00 = np.zeros(number)
    v01 = np.zeros(number)
    v10 = np.zeros(number)
    v11 = np.zeros(number)
     
    for i in range (0, number, step):
        print (i)
        value[i], v00[i], v01[i], v10[i], v11[i] = td (i, Matrix_1 ,Matrix_2)
      
    results = pd.DataFrame(list(zip(itera, value, v00, v01, v10, v11 ))) 

    # adding column name to the respective columns:
    results.columns =['Time Delay', 'Correlation', '0-0', '0-1', '1-0', '1-1']
    
    if save == 1 :
        results.to_csv('Correlation_results.csv', index=False, sep =';')   
    
    #-------------------------------------------------
    return results, itera, value
    #-------------------------------------------------
