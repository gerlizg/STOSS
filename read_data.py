#-------------------------------------------------
#             LIBRERIES & FUNCTIONS
#-------------------------------------------------
import pandas as pd

#-------------------------------------------------
def read_data (flag):

        '''
        Taking the index of the studied system, this part of the code 
        returns all its constants and description
        '''
            
        data = pd.read_csv('full_data_file.csv', sep=';')   #   Reading the file 

        #--------------------------------------------------------------------  
        # Saving constants's compounds:
        #--------------------------------------------------------------------    
        g_Dy = data.iloc[:, -1]
        g_Dy = g_Dy.astype('float32')
        constants = data.iloc[:, 2:7]
        constants = constants.astype('float32')
        compound_constants = constants.values.tolist()
        compound_names_all = data[[ "compound"]].values
        number = data[["sample_ID"]].values
        
        #--------------------------------------------------------------------  
        #   Cleaning the names:
        #--------------------------------------------------------------------
        name = str(compound_names_all[flag])
        number = str(number [flag])
        name = name.replace('[', '').replace(']', '')
        number = number.replace('[', '').replace(']', '')
        
        #--------------------------------------------------------------------
        return compound_constants[flag], g_Dy[flag], name, number

