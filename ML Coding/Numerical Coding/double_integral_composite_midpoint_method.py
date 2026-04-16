def midpoint(
    f: "function", 
    a: "lower bound", 
    b: "upper bound", 
    n: "input"
):
    h = float(b-a)/n
    result = 0
    for i in range(n):
        result += f((a + h/2.0) + i*h)
    result *= h
    return result

def midpoint_double2(
    f: "function",
    a: "outer lower bound", b: "outer upper bound",
    c: "inner lower bound", d: "inner upper bound", 
    nx: "x-input", ny: "y-input"
):
    def g(x):
        return midpoint(lambda y: f(x, y), c, d, ny)

    return midpoint(g, a, b, nx)