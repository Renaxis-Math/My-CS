def midpoint_triple1(
    g: "function of three variables (x,y,z)",
    a: "x lower bound", 
    b: "x upper bound",
    c: "y lower bound", 
    d: "y upper bound",
    e: "z lower bound", 
    f: "z upper bound",
    nx: "number of x subdivisions",
    ny: "number of y subdivisions",
    nz: "number of z subdivisions"
):
    hx = (b - a)/float(nx)
    hy = (d - c)/float(ny)
    hz = (f - e)/float(nz)
    I = 0
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                xi = a + hx/2 + i*hx
                yj = c + hy/2 + j*hy
                zk = e + hz/2 + k*hz
                I += hx*hy*hz*g(xi, yj, zk)
    return I

def midpoint(
    f: "function of one variable",
    a: "lower bound",
    b: "upper bound",
    n: "number of subdivisions"
):
    h = float(b-a)/n
    result = 0
    for i in range(n):
        result += f((a + h/2.0) + i*h)
    result *= h
    return result

def midpoint_triple2(
    g: "function of three variables (x,y,z)",
    a: "x lower bound", 
    b: "x upper bound",
    c: "y lower bound", 
    d: "y upper bound",
    e: "z lower bound", 
    f: "z upper bound",
    nx: "number of x subdivisions",
    ny: "number of y subdivisions",
    nz: "number of z subdivisions"
):
    def p(x: "x coordinate", y: "y coordinate"):
        return midpoint(lambda z: g(x, y, z), e, f, nz)

    def q(x: "x coordinate"):
        return midpoint(lambda y: p(x, y), c, d, ny)

    return midpoint(q, a, b, nx)

### TESTING-ONLY ###
def test_midpoint_triple():
    """Test that a linear function is integrated exactly."""
    def g(x, y, z):
        return 2*x + y - 4*z

    a = 0;  b = 2;  c = 2;  d = 3;  e = -1;  f = 2
    import sympy
    x, y, z = sympy.symbols('x y z')
    I_expected = sympy.integrate(
        g(x, y, z), (x, a, b), (y, c, d), (z, e, f))
    for nx, ny, nz in (3, 5, 2), (4, 4, 4), (5, 3, 6):
        I_computed1 = midpoint_triple1(
            g, a, b, c, d, e, f, nx, ny, nz)
        I_computed2 = midpoint_triple2(
            g, a, b, c, d, e, f, nx, ny, nz)
        tol = 1E-14
        print(I_expected, I_computed1, I_computed2)
        assert abs(I_computed1 - I_expected) < tol
        assert abs(I_computed2 - I_expected) < tol