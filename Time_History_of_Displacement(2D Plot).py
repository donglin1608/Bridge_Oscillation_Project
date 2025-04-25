import numpy as np
import matplotlib.pyplot as plt

# === 1) SYSTEM PARAMETERS ===
m = 1000.0                # mass (kg)
k = 4e4                   # stiffness (N/m)
omega_n = np.sqrt(k/m)    # natural frequency (rad/s)
zeta = 0.05               # damping ratio
c = 2*zeta*omega_n*m      # damping coefficient (Ns/m)
F0 = 1000.0               # forcing amplitude (N)
Omega = omega_n           # drive at resonance
h = 0.005                 # time step (s)

# === 2) TIME ARRAY ===
t_vals = np.arange(0, 20+h, h)

# === 3) RUNGE–KUTTA 4 SOLVER ===
def deriv(y, t):
    x, v = y
    F = F0*np.sin(Omega*t)
    return np.array([v, (F - c*v - k*x)/m])

y = np.array([0.0, 0.0])      # x(0)=0, v(0)=0
x_vals = np.zeros_like(t_vals)
for i, t in enumerate(t_vals):
    x_vals[i] = y[0]
    k1 = deriv(y, t)
    k2 = deriv(y+0.5*h*k1, t+0.5*h)
    k3 = deriv(y+0.5*h*k2, t+0.5*h)
    k4 = deriv(y+   h*k3, t+   h)
    y += (h/6)*(k1 + 2*k2 + 2*k3 + k4)

# === 4) ANALYTICAL (HOMOGENEOUS + PARTICULAR) SOLUTION ===
# 4a) particular
denom = np.sqrt((omega_n**2 - Omega**2)**2 + (2*zeta*omega_n*Omega)**2)
X = (F0/m)/denom
phi = np.arctan2(2*zeta*omega_n*Omega, omega_n**2 - Omega**2)
x_part = X * np.sin(Omega*t_vals - phi)

# 4b) homogeneous
omega_d = omega_n*np.sqrt(1 - zeta**2)
# initial homogeneous conditions:
x_h0 = 0 - x_part[0]
v_h0 = 0 - (X*Omega*np.cos(-phi))
C1 = x_h0
C2 = (v_h0 + zeta*omega_n*C1)/omega_d
x_hom = np.exp(-zeta*omega_n*t_vals)*(C1*np.cos(omega_d*t_vals) + C2*np.sin(omega_d*t_vals))

x_exact = x_part + x_hom

# === 5) PLOT EVERYTHING ===
plt.figure(figsize=(10,6))
plt.plot(t_vals, x_vals,      label="Numerical Solution (RK4)",      lw=2)
plt.plot(t_vals, x_exact, '--',label="Analytical Solution",            lw=2)
plt.axhline(F0/k, color='gray', ls='--', label='Static Deflection F₀/k')

plt.xlabel("Time (s)")
plt.ylabel("Displacement x(t) [m]")
plt.title("Bridge Displacement Over Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
# Save the figure
plt.savefig("Bridge_Displacement_Over_Time.png", dpi=300)