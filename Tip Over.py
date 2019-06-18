from math import *

L=.15
g=9.81
theta=0.1
t=0
dt=0.000001

omega=0

while theta<pi/4.0:
    alpha=3*sin(theta)*g/(2*L)
    omega=omega+alpha*dt
    theta=theta+omega*dt
    t=t+dt

print(t)
print(omega)
'''

print(sqrt((2*g*(1-cos(pi))/(L/2.0))/(1+(1/3.0))))


print(9.284312183599829)


print(((14.007141035914502**2)*L) + 9.81)
'''
