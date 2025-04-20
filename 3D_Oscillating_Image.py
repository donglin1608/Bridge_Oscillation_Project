import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter

# === 1) Physical / simulation parameters ===
m = 1000.0             # mass (kg)
k = 4e4                # stiffness (N/m)
omega_n = np.sqrt(k/m) # natural frequency (rad/s)
F0 = 1000.0            # forcing amplitude (N)
zeta = 0.05            # damping ratio

# === 2) RK4 time‑history for displacement A(t) ===
def deriv(y, t):
    x, v = y
    c = 2 * zeta * np.sqrt(k*m)
    F = F0 * np.sin(omega_n * t)
    return np.array([v, (F - c*v - k*x) / m])

# time array
t = np.linspace(0, 20, 400)
h = t[1] - t[0]
y = np.array([0.0, 0.0])
A = np.zeros_like(t)

for i, ti in enumerate(t):
    A[i] = y[0]
    k1 = deriv(y, ti)
    k2 = deriv(y + 0.5*h*k1, ti + 0.5*h)
    k3 = deriv(y + 0.5*h*k2, ti + 0.5*h)
    k4 = deriv(y +   h*k3, ti +   h)
    y += (h/6) * (k1 + 2*k2 + 2*k3 + k4)

# === 3) First mode shape ===
L = 10.0
x = np.linspace(0, L, 100)
phi = np.sin(np.pi * x / L)

# === 4) Prepare animation frames ===
# sample 100 frames evenly from the time series
frames_idx = np.linspace(0, len(t)-1, 100, dtype=int)

# === 5) Set up figure & initial line ===
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
line, = ax.plot(x, np.zeros_like(x), A[frames_idx[0]] * phi, linewidth=2)

ax.set_xlabel('Span (m)')
ax.set_ylabel('Width')
ax.set_zlabel('Deflection (m)')
ax.set_title(f'Bridge Oscillation (ζ={zeta})')

# fix camera angle
ax.view_init(elev=20, azim=-60)

# === 6) Update function ===
def update(frame):
    w = A[frame] * phi
    line.set_data(x, np.zeros_like(x))
    line.set_3d_properties(w)
    return line,

# === 7) Animate & save as GIF ===
ani = FuncAnimation(
    fig,
    update,
    frames=frames_idx,
    interval=100,   # milliseconds between frames (slower)
    blit=True
)

writer = PillowWriter(fps=10)  # frames per second for GIF
ani.save("bridge_oscillation_slow.gif", writer=writer)

plt.close(fig)

print("Saved animation as bridge_oscillation_slow.gif")
