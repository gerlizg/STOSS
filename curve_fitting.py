#-------------------------------------------------
#             LIBRERIES & FUNCTIONS
#-------------------------------------------------
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt         #   Graphic Representation
import scipy.stats as ss
import pandas as pd

#-------------------------------------------------
def curve_fitting (name_plot, T, ratio1, ratio2, name, number, x, y, P_i, graph_type, option, N_ex, step, B, time_steps, E, P_ij):
    
    font = {'family' : "Times New Roman",
        'weight' : 'normal',
        'size'   : 30  }

    plt.rc('font', **font)
    plt.rc('legend',fontsize=15) # using a size in points
    plt.rcParams['lines.linewidth'] = 4
    plt.rcParams['lines.linestyle'] = '-'
    
    if graph_type == 1:        #For residence times
        
        
        #Cleaning the residence times list:
        res_time_vector = []
    
        for j in range(0,N_ex):
            
            vector = y[j,:]
            y_temp = [i for i in vector if i != 0]
            res_time_vector.append(y_temp)
        
        res_time_vector = [i for i in res_time_vector if i != []]
        res_time_vector = [item for sublist in res_time_vector for item in sublist]
              
        #Calculating the frequency of each value in the Residence Times list:
        bin_range = int((max(res_time_vector)) - min(res_time_vector))+1
        
        freq = np.histogram(res_time_vector, bins = bin_range)
        tops = freq[0] 
        bin_edges = freq[1] 
      
        bin_centres = list()
        for i in range (len(tops)):
            bin_centre = (bin_edges [i] + bin_edges [i+1])/2
            bin_centres.append(bin_centre)
        
        
        #Mapping bin_centres and tops:
        output = list (map(lambda x,y: (x,y), bin_centres,tops))
        
        #Deleting those who have 0:
        for i in range(len(output)-1,-1,-1):
            pair=output[i]
            for coord in pair:
                if coord == 0:
                    del output[i]
                    
        x = [item[0] for item in output]
        y = [item[1] for item in output]
       
        #Plotting the results:
        name1 = 'Distribution'+str(N_ex)+'exp_'+ name_plot+ '.png'
        plt.rcParams["figure.figsize"] = [18, 14]
        plt.rcParams["figure.autolayout"] = True
        plt.hist(res_time_vector, bins = bin_range, edgecolor="black",  color = "blue", label= "Histogram")
        plt.xlabel('Residence Time')
        plt.ylabel('Frequency')
        plt.title('Residence Times plot for %d experiments at %d K. Compound: %s (Sample ID: %s)' % (N_ex, T, name, number), fontsize = 25 )
        plt.legend(loc='upper right')
        plt.grid()
        plt.savefig(name1)
        plt.show()  

        a = 0
        tau = 0
        c = 0
        
        return a, tau, c                
        
    else:                 #For relaxation curve
        
                
        if option == 1:
                        
            name1 = 'Relaxation_'+str(N_ex)+'exp.png'          
            fig, ax1 = plt.subplots()

            color = 'tab:red'
            ax1.set_xlabel('Time, $t$(s)') 
            ax1.set_ylabel('# of spins aligned with the field', color=color)
            ax1.plot(x, y, color=color)
            ax1.tick_params(axis='y', labelcolor=color)
            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
            
            color = 'tab:blue'
            ax2.set_ylabel('Magnetic Field, B (mT)', color=color)  # we already handled the x-label with ax1
            ax2.plot(x, abs(-1000*B), color=color)
            ax2.tick_params(axis='y', labelcolor=color)
            ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
            
            
            fig.tight_layout()  # otherwise the right y-label is slightly clipped
            plt.title('Relaxation plot for %d experiments at %dmK. Compound: %s (Sample ID: %s)' % (N_ex, T*1000, name, number), fontsize = 25)
            plt.grid()
            plt.savefig(name1)
            plt.show()
            
            a = 0
            tau = 0
            c = 0
            
            return a, tau, c
            
        elif option == 0:
         
            a = N_ex
            c = N_ex * P_i
            tau, pcov = curve_fit(lambda t,  tau: (a-c) * np.exp(-t/tau) + c, x, y)
            y_fitted = (a-c) * np.exp(-x/tau) + c
            values = [2, 40, 80]
            factor = [1, 0.3, 0.0035]
            print (T)
            

                
            # Plot
            name1 = 'Relaxation_'+str(N_ex)+'exp.png'
            plt.rcParams["figure.figsize"] = [18, 14]
            plt.rcParams["figure.autolayout"] = True
            if T in values:
                name2 = str(T) + 'K_exp.csv'
                data = pd.read_csv(name2, sep=';')
                data = data.astype('float32')
                data = data.values
                ii = len(x)
                x_real = data[0:ii, 0]
                y_real = data[0:ii, 1]
                index = values.index(T)
                y = [((2 * x) - N_ex) for x in y]
                y = [x * factor[index] / (N_ex) for x in y]
                plt.plot(x_real, y_real, color = "blue", label = 'Experimental')
                plt.ylabel(u" Magnetic moment, \u03bc (emu)")

            else:
                plt.plot(x, y_fitted, color = "blue", label=r'Fitted function: $y= (%.2f)e^{(-x/%.4f)}+%.2f$' %(a, tau, c))
                plt.ylabel("Spins")
            plt.plot(x, y, color = "red", label= "Simulator")
            plt.xlabel('Time, $t$(s)') 
            plt.title('Relaxation plot for %d experiments at %d K. Compound: %s (Sample ID: %s)' % (N_ex, T, name, number))
            plt.legend(loc='upper right', prop={'size': 30})
            plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
            plt.grid()
            
            
            
            
            plt.savefig(name1)    
            plt.show()
            
            print("Tau parameter for relaxation curve:",tau)
            
            y_fitted_copy = pd.DataFrame(y_fitted)
            y_fitted_copy.to_csv('y_fitted.csv', index=False)
        
        #--------------------------------------------------------------------    
        return a, tau, c
        
        
