def trapezoidal_double(f, a, b, c, d, nx, ny):
    hx = (b - a)/float(nx)
    hy = (d - c)/float(ny)
    I = 0.25*(f(a, c) + f(a, d) + f(b, c) + f(b, d))
    Ix = 0
    for i in range(1, nx):
        xi = a + i*hx
        Ix += f(xi, c) + f(xi, d)
    I += 0.5*Ix
    Iy = 0
    for j in range(1, ny):
        yj = c + j*hy
        Iy += f(a, yj) + f(b, yj)
    I += 0.5*Iy
    Ixy = 0
    for i in range(1, nx):
        for j in range(1, ny):
            xi = a + i*hx
            yj = c + j*hy
            Ixy += f(xi, yj)
    I += Ixy
    I *= hx*hy
    return I

def test_trapezoidal_double():
    """Test that a linear function is integrated exactly."""
    def f(x, y):
        return 2*x + y

    a = 0;  b = 2;  c = 2;  d = 3
    import sympy
    x, y = sympy.symbols('x  y')
    I_expected = sympy.integrate(f(x, y), (x, a, b), (y, c, d))
    # Test three cases: nx < ny, nx = ny, nx > ny
    for nx, ny in (3, 5), (4, 4), (5, 3):
        I_computed = trapezoidal_double(f, a, b, c, d, nx, ny)
        tol = 1E-14
        #print I_expected, I_computed
        assert abs(I_computed - I_expected) < tol

if __name__ == '__main__':
    test_trapezoidal_double()