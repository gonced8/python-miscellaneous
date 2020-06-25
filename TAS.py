''' A program to calculate the TAS from the CAS, QNH, altimeter, and ground temperature 
'''

from sys import argv, exit
from math import sqrt

def get_pressure(QNH, h):
    return QNH*(1-0.0065*h/288.15)**5.25588

def get_temperature(h, T0=15):
    return T0-0.0065*h

def get_dynamic_pressure(CAS):
    gamma = 1.4
    a0 = 340.3
    p0 = 101325
    return (((CAS**2*(gamma-1))/(2*a0**2)+1)**(gamma/(gamma-1))-1)*p0

def get_mach(p, q):
    gamma = 1.4
    return sqrt(2/(gamma-1)*((q/p+1)**((gamma-1)/gamma)-1))

def get_airspeed(T):
    a0 = 340.3
    return a0*sqrt((273.15+T)/(273.15+15))

def get_tas(M, a):
    return M*a

if __name__=="__main__":
    if len(argv)<5:
        print(f"Please specify input arguments. Ex: $ python3 {argv[0]} <CAS> <QNH> <altitude> <ground temp>")
        exit(0)

    CAS, QNH, h, T0 = [float(arg) for arg in argv[1:5]]
    print("CAS", CAS, "\tQNH", QNH, "\taltitude", h, "\tground temp", T0)

    p = get_pressure(QNH, h)
    T = get_temperature(h, T0)
    q = get_dynamic_pressure(CAS)
    M = get_mach(p, q)
    a = get_airspeed(T)
    TAS = get_tas(M, a)

    print("pressure", p, "\ttemperature", T, "\tdynamic pressure", q, "\tMach", M, "\aAirspeed", a, "\tTAS", TAS)
