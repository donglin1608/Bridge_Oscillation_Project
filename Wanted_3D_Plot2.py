import numpy as np
import matplotlib.pyplot as plt

# Define system parameters (mass-spring-damper per mass)
m = 1e5      # kg, each mass
k0 = 2e7     # N/m, spring to ground at each mass
kc = 1e7     # N/m, coupling spring between adjacent masses
c0 = 2*np.sqrt(k0*m)*0.01  # Ns/m, damping (zeta ~ 0.01)
cc = c0      # Ns/m, coupling damper (for simplicity)

# Define derivatives for the 4-mass system
def derivatives(state, t, F0, omega):
    # state: [x1, v1, x2, v2, x3, v3, x4, v4]
    x1,v1,x2,v2,x3,v3,x4,v4 = state
    # External forcing on each mass (sinusoidal wind load)
    F_ext = F0 * np.sin(omega*t)
    F1 = F_ext; F2 = F_ext; F3 = F_ext; F4 = F_ext
    # Relative displacements for coupling springs/dampers
    dx12 = x1 - x2; dv12 = v1 - v2
    dx13 = x1 - x3; dv13 = v1 - v3
    dx24 = x2 - x4; dv24 = v2 - v4
    dx34 = x3 - x4; dv34 = v3 - v4
    # Compute accelerations from forces (spring + damper)
    a1 = (F1
          - k0*x1 - c0*v1
          - kc*dx12 - cc*dv12
          - kc*dx13 - cc*dv13) / m
    a2 = (F2
          - k0*x2 - c0*v2
          - kc*(-dx12) - cc*(-dv12)
          - kc*dx24 - cc*dv24) / m
    a3 = (F3
          - k0*x3 - c0*v3
          - kc*(-dx13) - cc*(-dv13)
          - kc*dx34 - cc*dv34) / m
    a4 = (F4
          - k0*x4 - c0*v4
          - kc*(-dx24) - cc*(-dv24)
          - kc*(-dx34) - cc*(-dv34)) / m
    return np.array([v1, a1, v2, a2, v3, a3, v4, a4])

# Fourth-order Runge-Kutta integrator step
def rk4_step(f, state, t, dt, *args):
    k1 = f(state,       t,          *args)
    k2 = f(state+dt/2*k1, t+dt/2,   *args)
    k3 = f(state+dt/2*k2, t+dt/2,   *args)
    k4 = f(state+dt*k3,   t+dt,     *args)
    return state + dt/6*(k1 + 2*k2 + 2*k3 + k4)

# Simulate the system for a given forcing frequency
F0 = 1e6                # N, forcing amplitude
freq = 2.25             # Hz, near expected natural frequency
omega = 2*np.pi*freq    # rad/s
dt = 0.005              # time step (s)
t_end = 50              # total simulation time (s)
n_steps = int(t_end/dt)
state = np.zeros(8)     # initial [x,v] = 0
time = np.linspace(0, t_end, n_steps+1)
sol = np.zeros((n_steps+1, 8))
sol[0] = state

for i in range(n_steps):
    state = rk4_step(derivatives, state, i*dt, dt, F0, omega)
    sol[i+1] = state

# Extract displacement of mass 1 (they move nearly identically in this symmetric case)
x1 = sol[:,0]
plt.figure(figsize=(6,4))
plt.plot(time, x1, color='tab:blue')
plt.xlabel('Time (s)')
plt.ylabel('Displacement of Mass 1 (m)')
plt.title('Bridge Mass Displacement Over Time')
plt.grid(True)
plt.tight_layout()
plt.savefig('amplitude_time.png')