import numpy as np
import matplotlib.pyplot as plt

# Parameters
m = 1000.0                  # mass (kg)
k = 4e4                     # stiffness (N/m)
omega_n = np.sqrt(k / m)    # natural frequency (rad/s)
F0 = 1000.0                 # forcing amplitude (N)
Omega = omega_n             # excitation frequency at resonance
h = 0.01                    # time step (s)
t = np.arange(0, 20 + h, h) # time array from 0 to 20 s

# Damping ratios
zetas = [0.0, 0.05, 0.5, 2.0]

# Function defining the derivatives for the SDOF system
def deriv(y, time, zeta):
    x, v = y
    c = 2 * zeta * np.sqrt(k * m)
    F = F0 * np.sin(Omega * time)
    dxdt = v
    dvdt = (F - c * v - k * x) / m
    return np.array([dxdt, dvdt])

# Runge-Kutta 4th order integrator
results = {}
for z in zetas:
    y = np.array([0.0, 0.0])  # initial conditions: x(0)=0, v(0)=0
    xs = []
    for ti in t:
        k1 = deriv(y, ti, z)
        k2 = deriv(y + 0.5*h*k1, ti + 0.5*h, z)
        k3 = deriv(y + 0.5*h*k2, ti + 0.5*h, z)
        k4 = deriv(y + h*k3, ti + h, z)
        y = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        xs.append(y[0])
    results[z] = np.array(xs)

# 1. Time-History Plot for Different Damping Ratios
plt.figure()
for z in zetas:
    plt.plot(t, results[z], label=f'zeta={z}')
plt.xlabel('Time (s)')
plt.ylabel('Displacement x (m)')
plt.legend()
plt.title('Time-History for Different Damping Ratios')

# 2. Zoomed Steady-State Plot (t >= 10 s)
mask = t >= 10.0
plt.figure()
for z in zetas:
    plt.plot(t[mask], results[z][mask], label=f'zeta={z}')
plt.xlabel('Time (s)')
plt.ylabel('Displacement x (m)')
plt.legend()
plt.title('Steady-State (t ≥ 10 s) for Different Damping Ratios')

# 3. Semilog Plot of Absolute Displacement for Envelope Comparison
plt.figure()
for z in zetas:
    plt.semilogy(t, np.abs(results[z]), label=f'zeta={z}')
plt.xlabel('Time (s)')
plt.ylabel('Absolute Displacement |x| (m)')
plt.legend()
plt.title('Logarithmic Decay of Displacement Envelope')

plt.show()
