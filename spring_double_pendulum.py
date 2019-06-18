import math
from visual import *

def calc_a_2 (alpha_0,alpha_1, beta_0, beta_1, a_0, a_1, b_0, b_1, l1, l2, k1, k2, m1, m2, g):
    return ((k1*l1+g*m1*math.cos(alpha_0)-k2*l2*math.cos(alpha_0-beta_0)+k2*b_0*math.cos(alpha_0-beta_0)+a_0*(-k1+m1*(alpha_1**2)))/m1)
    
def calc_b_2 (alpha_0,alpha_1, beta_0, beta_1, a_0, a_1, b_0, b_1, l1, l2, k1, k2, m1, m2, g):
    return ((k2*l2*m1+k2*l2*m2-k1*l1*m2*math.cos(alpha_0-beta_0)+k1*m2*a_0*math.cos(alpha_0-beta_0)-b_0*(k2*(m1+m2)-m1*m2*(beta_1**2)))/(m1*m2))

def calc_alpha_2 (alpha_0,alpha_1, beta_0, beta_1, a_0, a_1, b_0, b_1, l1, l2, k1, k2, m1, m2, g):
    return (-((g*m1*math.sin(alpha_0)-k2*l2*math.sin(alpha_0-beta_0)+k2*b_0*math.sin(alpha_0-beta_0)+2*m1*a_1*alpha_1)/(m1*a_0)))

def calc_beta_2 (alpha_0,alpha_1, beta_0, beta_1, a_0, a_1, b_0, b_1, l1, l2, k1, k2, m1, m2, g):
    return ((-k1*l1*math.sin(alpha_0-beta_0)+k1*a_0*math.sin(alpha_0-beta_0)-2*m1*b_1*beta_1)/(m1*b_0))

alpha_0 = math.pi/2
beta_0 = 0
alpha_1 = 0
beta_1 = 0
alpha_2 = 0
beta_2 = 0

a_0 = 1
b_0 = 1
a_1 = 0
b_1 = 0
a_2 = 0
b_2 = 0

l1 = 1
l2 = 1
m1 = 1
m2 = 2
k1 = 200
k2 = 300
g = 9.81

dt = 0.001
t_max = 60
t=0


scene.autoscale = 0		# stop it from zooming in and out
scene.title = 'Double pendulum'
scene.range = (3, 3, 1)

#Center
ball0 = sphere(pos=vector(0, 0, 0), radius=0.05, color=color.cyan)

#Balls
ball1 = sphere(pos=vector(a_0*math.sin(alpha_0), -a_0*math.cos(alpha_0),0), radius=0.12, color=color.blue, make_trail=True, retain=int(1.0/dt))
ball2 = sphere(pos=vector(a_0*math.sin(alpha_0) + b_0*math.sin(beta_0), -a_0*math.cos(alpha_0) - b_0*math.cos(beta_0), 0), radius=0.12, color=color.red, make_trail=True, retain=int(1.0/dt))

#Strings
arm1 = cylinder(pos=(0,0,0), axis=(a_0*math.sin(alpha_0), -a_0*math.cos(alpha_0),0), radius=.03, color=color.white)
arm2 = cylinder(pos=(a_0*math.sin(alpha_0), -a_0*math.cos(alpha_0),0), axis=(b_0*math.sin(beta_0), -b_0*math.cos(beta_0), 0), radius=.03, color=color.white)

#while t<t_max :
while 1:
    rate(1/dt)
    
    if(round(t, int(-math.log10(dt)))%1 == 0):
        print "%ds" %t
        
    alpha_2 = calc_alpha_2 (alpha_0,alpha_1, beta_0, beta_1, a_0, a_1, b_0, b_1, l1, l2, k1, k2, m1, m2, g)
    beta_2 = calc_beta_2 (alpha_0,alpha_1, beta_0, beta_1, a_0, a_1, b_0, b_1, l1, l2, k1, k2, m1, m2, g)
    a_2 = calc_a_2 (alpha_0,alpha_1, beta_0, beta_1, a_0, a_1, b_0, b_1, l1, l2, k1, k2, m1, m2, g)
    b_2 = calc_b_2 (alpha_0,alpha_1, beta_0, beta_1, a_0, a_1, b_0, b_1, l1, l2, k1, k2, m1, m2, g)

    alpha_1 = alpha_1 + alpha_2*dt
    beta_1 = beta_1 + beta_2*dt
    a_1 = a_1 + a_2*dt
    b_1 = b_1 + b_2*dt

    alpha_0 = alpha_0 + alpha_1*dt
    beta_0 = beta_0 + beta_1*dt
    a_0 = a_0 + a_1*dt
    b_0 = b_0 + b_1*dt

    alpha_0 = alpha_0%(2*math.pi)
    beta_0 = beta_0%(2*math.pi)
    
    ball1.pos.x = a_0*math.sin(alpha_0)
    ball1.pos.y = -a_0*math.cos(alpha_0)
    arm1.axis = (ball1.pos.x, ball1.pos.y, 0)
    
    ball2.pos.x = ball1.pos.x + b_0*math.sin(beta_0)
    ball2.pos.y = ball1.pos.y - b_0*math.cos(beta_0)
    arm2.pos = (ball1.pos.x, ball1.pos.y, 0)
    arm2.axis = (ball2.pos.x - ball1.pos.x, ball2.pos.y - ball1.pos.y, 0)

#    if (t==0):
#        raw_input()
    
    t=t+dt

