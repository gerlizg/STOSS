def objective (x, tau, P_i):
        a = N_ex
        b = N_ex * P_i
        return ((a-b)* np.exp (-x/tau)) + b