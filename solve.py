def solve(vars, P_ij):
        Pa, Pb = vars
        eq1 = (Pa/Pb)-P_ij
        eq2 = (Pa+Pb)-1
        return [eq1, eq2]