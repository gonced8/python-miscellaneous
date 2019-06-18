import matplotlib
matplotlib.use('TKAgg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

animate = True
n_curves = 5
dt = 0.01
t = 10
n_iterations = int(t/dt)
x0 = 0

t = np.arange(0, t, dt)
x = np.empty((n_iterations, n_curves))

x[0] = x0 * n_curves

for i in range(1, n_iterations):
    x[i] = x[i-1] + dt * np.random.normal(size=(n_curves))

x = np.transpose(x)     # more efficient for plotting
lines = []
fig, ax = plt.subplots()

lines = [ax.plot(t, x[i], lw=1)[0] for i in range(n_curves)]    # plots lines and adds each plot to a list

def update(num, t, x, lines):
    for i in range(len(lines)):
        lines[i].set_data(t[:num], x[i, :num])
    return lines

if animate:
    ani = animation.FuncAnimation(fig, update, n_iterations, fargs=[t, x, lines],
                              interval=dt*1000, blit=True, repeat=False)

plt.title('Random Walk')
plt.xlabel('t')
plt.ylabel('x')
plt.grid(which='both')
plt.minorticks_on()
plt.show()

