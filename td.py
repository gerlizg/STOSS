from collections import Counter

def td(number, spin1, spin2):

    spin2 = spin2 [number:-1]
    spin1 = spin1 [0:len(spin2)]
    
    
    
    sp1_sp2 = list (map(lambda x,y: (x,y), spin1,spin2))
    
    rr = Counter(sp1_sp2)
    
    '''
    if number < 2:
        print ('spin 1')
        print (spin1)
        #print (len(spin1))
        print ('spin 2')
        print (spin2)
        #print (len(spin2))
        print ('Combination')
        print (sp1_sp2)
        #print (len(sp1_sp2))
        
    #print ('Tiempo de retardo:')
    #print (number)
    #print (rr)
    '''
    
   
    
    checking = {(0.0, 1.0), (1.0, 0.0), (1.0, 1.0), (0.0, 0.0)}
    
    for i in checking:
        if i not in rr:
            rr.update({i:0.02})
    
           
    listt = [rr[x] for x in sorted(rr.keys())]
    '''
    if number == 0:
        print (rr)
        print (listt)
    '''
    correlacion = (listt[0]+listt[3])/(listt[1]+listt[2])
    #print (correlacion)
    
    #return correlacion, listt[3], listt[0], listt[2], listt[1]
    return correlacion, listt[0], listt[1], listt[2], listt[3]