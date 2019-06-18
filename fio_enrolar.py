from math import *

L=5
R=2
v=0.1
dt=0.001

l = L
theta1=pi
x=-R
y=L
vx=v
vy=0
t=0
theta2=atan(y/x)+pi

a=0
while(l>0 and a<999999999):
    a = (theta2-theta1)/dt *l**2

    x = x + vx*dt
    y = y + vy *dt

    theta1=theta2
    theta2=atan(y/x)
    if(x<0):
        theta2=theta2+pi

    ax = a*(-sin(theta1))
    ay = a*(cos(theta1))

    vx = vx + ax*dt
    vy= vy + ay*dt

    l = l - abs(theta2-theta1)*R
    theta=((L-l)/R) + pi
    t = t+dt


print(t)
print(sqrt(vx**2 + vy**2))
print(l)




