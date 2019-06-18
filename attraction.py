def main():
    dt=0.001
    t=0
    m1=40
    m2=65
    x1=0
    x2=1
    v1=0
    v2=0
    a1=0
    a2=0

    while abs(x2-x1)>0.10:
        a1=g_acceleration(m2, x1-x2)
        a2 = g_acceleration(m1, x2-x1)

        v1+=a1*dt
        v2+=a2*dt

        x1+=v1*dt
        x2+=v2*dt

        t+=dt

    print(t, 's')
    print(t/60, 'min')
    print(t/3600, 'h')

def g_acceleration(m, r):
    if r<0:
        return ((6.6740831e-11)*m/(r**2))
    else:
        return -((6.6740831e-11)*m/(r**2))


main()