import math
from visual import *

def calc_alpha_2 (alpha_0, beta_0, alpha_1, beta_1, l1, l2, m1, m2, g):
    return ((-m2*math.cos(alpha_0-beta_0)*l1*(alpha_1**2)*math.sin(alpha_0-beta_0) + m2*math.cos(alpha_0-beta_0)*g*math.sin(beta_0) - m2*l2*(beta_1**2)*math.sin(alpha_0-beta_0) - (m1+m2)*g*math.sin(alpha_0)) / (l1*(m1+m2 - m2*(math.cos(alpha_0-beta_0)**2))))

def calc_beta_2 (alpha_0, beta_0, alpha_1, beta_1, l1, l2, m1, m2, g):
    return (((m1+m2)*(l1*(alpha_1**2)*math.sin(alpha_0-beta_0) + (((beta_1**2)*math.sin(alpha_0-beta_0)*math.cos(alpha_0-beta_0)*m2*l2)/(m1+m2)) + math.cos(alpha_0-beta_0)*g*math.sin(alpha_0) - g*math.sin(beta_0)))/(l2*(m1 + m2*(math.sin(alpha_0-beta_0)**2))))

alpha_0 = math.pi
beta_0 = math.pi-0.1
alpha_1 = 0
beta_1 = 0
alpha_2 = 0
beta_2 = 0
l1 = 1
l2 = 1
m1 = 1
m2 = 2
g = 9.81

dt = 0.001
t_max = 60
t=0


scene.autoscale = 0		# stop it from zooming in and out
scene.title = 'Double pendulum'
scene.range = (2.5, 2.5, 1)

#Center
ball0 = sphere(pos=vector(0, 0, 0), radius=0.05, color=color.cyan)

#Balls
ball1 = sphere(pos=vector(l1*math.sin(alpha_0), -l1*math.cos(alpha_0),0), radius=0.12, color=color.blue, make_trail=True)
ball2 = sphere(pos=vector(l1*math.sin(alpha_0) + l2*math.sin(beta_0), -l1*math.cos(alpha_0) - l2*math.cos(beta_0), 0), radius=0.12, color=color.red, make_trail=True)

#Strings
arm1 = cylinder(pos=(0,0,0), axis=(l1*math.sin(alpha_0), -l1*math.cos(alpha_0),0), radius=.03, color=color.white)
arm2 = cylinder(pos=(l1*math.sin(alpha_0), -l1*math.cos(alpha_0),0), axis=(l2*math.sin(beta_0), -l2*math.cos(beta_0), 0), radius=.03, color=color.white)

#while t<t_max :
while 1:
    rate(1/dt)
    
    if(round(t, int(-math.log10(dt)))%1 == 0):
        print "%ds" %t
        
    alpha_2 = calc_alpha_2(alpha_0, beta_0, alpha_1, beta_1, l1, l2, m1, m2, g)
    beta_2 = calc_beta_2(alpha_0, beta_0, alpha_1, beta_1, l1, l2, m1, m2, g)
    alpha_1 = alpha_1 + alpha_2*dt
    beta_1 = beta_1 + beta_2*dt
    alpha_0 = alpha_0 + alpha_1*dt
    alpha_0 = alpha_0%(2*math.pi)
    beta_0 = beta_0 + beta_1*dt
    beta_0 = beta_0%(2*math.pi)

    t=t+dt

    ball1.pos.x = l1*math.sin(alpha_0)
    ball1.pos.y = -l1*math.cos(alpha_0)
    arm1.axis = (ball1.pos.x, ball1.pos.y, 0)
    
    ball2.pos.x = ball1.pos.x + l2*math.sin(beta_0)
    ball2.pos.y = ball1.pos.y - l2*math.cos(beta_0)
    arm2.pos = (ball1.pos.x, ball1.pos.y, 0)
    arm2.axis = (ball2.pos.x - ball1.pos.x, ball2.pos.y - ball1.pos.y, 0)


