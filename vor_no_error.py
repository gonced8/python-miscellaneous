import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parameters
step = 30       # [º] angular distance between radials
nmodes = 4      # [] number of simulated modes 
niter = 1       # [] number of simulated iterations
max_dt = 1     # [s] max time step in simulation
n_t_lap = 2     # [] number of laps to simulate (assuming cirle)

# Simulations constants
cte = {
    'd0': 5,    # [NM] radius
    'v0': 100,  # [kt] velocity
}

def model(t, y, cte, rad, ref):
    px, py = y[0:2]

    # Convert from kts to m/s
    v = cte['v0'] * 0.514

    # Compute current radial
    radial = get_radial(px, py)
    # Compute reference for VOR
    thetaref = get_thetaref(radial, rad, ref)

    # Calculate velocity
    vx = v*np.cos(thetaref)
    vy = v*np.sin(thetaref)

    return [vx, vy]

def get_radial(x, y):
    angle = np.arctan2(y, x)

    while angle<0:
        angle += 2*np.pi

    return angle

def get_thetaref(radial, rad, ref):
    angle = np.rad2deg(radial)

    idx = np.argmax(rad > angle)-1

    return np.deg2rad(ref[idx])

def generate_radial_ref(mode):
    if mode==0:
        rad = np.arange(0, 360, step)
        ref = np.arange(0+90, 360+90, step)
    elif mode==1:
        rad = np.arange(0, 360, step)
        ref = np.arange(0+step+90, 360+step+90, step)
    elif mode==2:
        rad = np.arange(0, 360, 2*step)
        ref = np.arange(0+90+step, 360+90+step, 2*step)
    elif mode==3:
        rad = np.arange(0, 360, step)
        ref = np.arange(0+90+step/2, 360+90+step/2, step)
    
    return rad, ref

def cartesian_to_polar(pos):
    radius = np.sqrt(pos[0]**2+pos[1]**2)
    angle = np.arctan2(pos[1], pos[0])
    angle = np.unwrap(angle)
    return radius, angle

def get_first_lap(sol):
    angle = np.arctan2(sol.y[1], sol.y[0])
    idx1 = np.argmax(angle<0)
    idx2 = np.argmax(angle[idx1:]>=0)
    if idx1!=0 and idx2!=0:
        sol.t = sol.t[0:idx1+idx2]
        sol.y = sol.y[:, 0:idx1+idx2]

    return sol

def draw_circle(d, rad, ax):
    circlex = d*np.cos(np.linspace(0, 2*np.pi, 100))
    circley = d*np.sin(np.linspace(0, 2*np.pi, 100))
    ax.plot(circlex, circley, '--')

def draw_radials(rad, radius, angle, ax):
    for r in np.deg2rad(rad):
        if r>angle[-1]:
            break
        idx = np.argmin(np.abs(angle-r))
        di = radius[idx]

        ax.plot([0, di*np.cos(r)], [0, di*np.sin(r)], 'k--', lw=0.5)

if __name__=="__main__":
    # Conversion from NM to m
    NM2m = 1852

    # Initial position
    px0, py0 = [cte['d0']*NM2m, 0]

    # Calculate timespan
    tf = 2*np.pi*cte['d0']*NM2m/(100*0.514)
    tspan = [0, n_t_lap*tf]

    # Generate figure
    fig, axs = plt.subplots(3, nmodes)

    for mode in range(nmodes):
        # Get radial and heading reference
        rad, ref = generate_radial_ref(mode)

        # Draw reference circle
        ax = axs[0, mode]
        draw_circle(cte['d0'], rad, ax)
                
        # Print progress
        print(mode*100/nmodes, '%')

        # Simulate
        y0 = [px0, py0]
        sol = solve_ivp(model, tspan, y0, args=[cte, rad, ref], method='BDF', max_step=max_dt)

        # Get only first lap
        sol = get_first_lap(sol)

        # Convert to min and NM
        sol.t = sol.t/60
        sol.y[:2] /= NM2m

        # Convert to polar coordinates
        radius, angle = cartesian_to_polar(sol.y[:2])

        # Compute heading
        heading = np.array([get_thetaref(a, rad, ref) for a in angle])

        # Convert to degrees and correct orientation
        radial = 90-np.rad2deg(angle)
        heading = 360+90-np.rad2deg(heading)
        
        # Plot trajectory
        ax = axs[0, mode]
        ax.plot(sol.y[0], sol.y[1])

        # Plot distance error
        ax = axs[1, mode]
        ax.plot(sol.t, radius-cte['d0'])

        # Plot radial and heading
        ax = axs[2, mode]
        ax.plot(sol.t, radial)
        ax.plot(sol.t, heading)

        # Draw radials
        ax = axs[0, mode]
        draw_radials(rad, radius, angle, ax)

        # Set plot title
        if mode==0:
            ax.set_title("90º current")
        elif mode==1:
            ax.set_title("90º next")
        elif mode==2:
            ax.set_title("90º next for 2")
        elif mode==3:
            ax.set_title("90º half for 1")

        # Set axes labels
        ax = axs[0, mode]
        ax.legend(['desired', 'actual', 'radials'], loc='upper right')
        ax.set_xlabel('x [NM]')
        ax.set_ylabel('y [NM]')
        ax.axis('equal')
        ax.grid()

        ax = axs[1, mode]
        ax.set_xlabel('t [min]')
        ax.set_ylabel('$\Delta$r [NM]')
        ax.grid()

        ax = axs[2, mode]
        ax.legend(["radial", "heading"])
        ax.set_xlabel('t [min]')
        ax.set_ylabel('angle [º]')
        ax.grid()

    #plt.tight_layout(pad=0.1, h_pad=0.5, w_pad=0.1)
    plt.show()
