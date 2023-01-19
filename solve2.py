def solve2(vars, vao):
        x, y = vars
        eq1 = (x+y)-(vao [0]/100)
        eq2 = (x/y)-(vao [1])
        return [eq1, eq2]