import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# --- 1) PARAMETERS ---
m   = 1000.0           # mass of each corner (kg)
k0  = 4e4              # vertical stiffness (N/m)
c0  = 2 * 0.05 * np.sqrt(k0*m)  # vertical damping (Ns/m)
kc  = 1e4              # coupling stiffness between corners (N/m)
cc  = 500.0            # coupling damping (Ns/m)
F0  = 1e3              # forcing amplitude (N)
omega = 2 * np.pi * 2.25  # forcing frequency (rad/s)

dt = 0.001   # time step (s)
T  = 10.0    # total simulation time (s)
n_steps = int(T / dt)

# --- 2) RK4 HELPER ---
def rk4_step(f, y, t, h, *args):
    k1 = f(y,            t,       *args)
    k2 = f(y + 0.5*h*k1, t + 0.5*h,*args)
    k3 = f(y + 0.5*h*k2, t + 0.5*h,*args)
    k4 = f(y +     h*k3, t +     h,*args)
    return y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)

# --- 3) DERIVATIVES WITH FORCE ON LEFT COLUMN ONLY ---
def derivatives_leftonly(state, t, F0, omega):
    x1,v1,x2,v2,x3,v3,x4,v4 = state

    # External forces
    F1 = F0 * np.sin(omega*t)
    F3 = F0 * np.sin(omega*t)
    F2 = 0.0
    F4 = 0.0

    # Relative displacements & velocities
    dx12, dv12 = x1-x2, v1-v2
    dx13, dv13 = x1-x3, v1-v3
    dx24, dv24 = x2-x4, v2-v4
    dx34, dv34 = x3-x4, v3-v4

    # Corner accelerations
    a1 = (F1 - k0*x1 - c0*v1
          - kc*dx12 - cc*dv12
          - kc*dx13 - cc*dv13) / m

    a2 = (F2 - k0*x2 - c0*v2
          + kc*dx12 + cc*dv12  # note the sign flip
          - kc*dx24 - cc*dv24) / m

    a3 = (F3 - k0*x3 - c0*v3
          + kc*dx13 + cc*dv13
          - kc*dx34 - cc*dv34) / m

    a4 = (F4 - k0*x4 - c0*v4
          + kc*dx24 + cc*dv24
          + kc*dx34 + cc*dv34) / m

    return np.array([v1, a1, v2, a2, v3, a3, v4, a4])

# --- 4) RUN THE SIMULATION ---
state = np.zeros(8)     # [x1,v1, x2,v2, x3,v3, x4,v4]
for step in range(n_steps):
    t = step * dt
    state = rk4_step(derivatives_leftonly, state, t, dt, F0, omega)

# Extract final displacements (corners 1–4)
disp = state[[0, 2, 4, 6]]

# --- 5) MAKE A 3D SURFACE OF THE DEFORMED PLATE ---
L, W = 100.0, 20.0  # bridge length & width
X = np.array([[0, L], [0, L]])
Y = np.array([[0, 0], [W, W]])
Z = np.array([[disp[0], disp[1]],
              [disp[2], disp[3]]])

fig = plt.figure(figsize=(6,4))
ax  = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, color='orange', alpha=0.8)
ax.set_xlabel('Bridge Length (m)')
ax.set_ylabel('Bridge Width (m)')
ax.set_zlabel('Lateral Deflection (m)')
ax.set_title('Bridge Deck Deformation under Wind Load')
plt.tight_layout()
plt.savefig('deformation_3d.png', dpi=200)
plt.show()
