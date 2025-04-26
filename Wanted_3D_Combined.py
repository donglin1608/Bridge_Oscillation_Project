import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# --- 1) PARAMETERS ---
m   = 1000.0
k0  = 4e4
c0  = 2 * 0.05 * np.sqrt(k0*m)
kc  = 1e4
cc  = 500.0
F0  = 1e3
omega = 2 * np.pi * 2.25

dt = 0.005
T  = 10.0
n_steps = int(T/dt)
times = np.linspace(0, T, n_steps+1)

# RK4 step
def rk4_step(f, y, t, h, *args):
    k1 = f(y, t, *args)
    k2 = f(y+0.5*h*k1, t+0.5*h, *args)
    k3 = f(y+0.5*h*k2, t+0.5*h, *args)
    k4 = f(y+h*k3,     t+h,     *args)
    return y + (h/6)*(k1+2*k2+2*k3+k4)

# 4-mass ODE
def deriv(state, t, F0, omega):
    x1,v1,x2,v2,x3,v3,x4,v4 = state
    F1 = F3 = F0*np.sin(omega*t)
    F2 = F4 = 0.0
    dx12,dv12 = x1-x2, v1-v2
    dx13,dv13 = x1-x3, v1-v3
    dx24,dv24 = x2-x4, v2-v4
    dx34,dv34 = x3-x4, v3-v4
    a1 = (F1 - k0*x1 - c0*v1 - kc*dx12 - cc*dv12 - kc*dx13 - cc*dv13)/m
    a2 = (F2 - k0*x2 - c0*v2 + kc*dx12 + cc*dv12 - kc*dx24 - cc*dv24)/m
    a3 = (F3 - k0*x3 - c0*v3 + kc*dx13 + cc*dv13 - kc*dx34 - cc*dv34)/m
    a4 = (F4 - k0*x4 - c0*v4 + kc*dx24 + cc*dv24 + kc*dx34 + cc*dv34)/m
    return np.array([v1,a1, v2,a2, v3,a3, v4,a4])

# integrate
sol = np.zeros((n_steps+1, 8))
for i in range(n_steps):
    sol[i+1] = rk4_step(deriv, sol[i], times[i], dt, F0, omega)

# corner displacements over time
X1, X2, X3, X4 = sol[:,0], sol[:,2], sol[:,4], sol[:,6]

# grid for the deck
L, W = 100, 20
corners = np.array([[0,0],[L,0],[L,W],[0,W]])

# build figure with 3 3D subplots
fig = make_subplots(
    rows=1, cols=3,
    specs=[[{"type":"surface"}, {"type":"cone"}, {"type":"scene"}]],
    subplot_titles=["Deck Deformation","Wind Vectors","Time History"]
)

# --- Deck surface at final time ---
Z_final = np.array([[X1[-1], X2[-1]], [X4[-1], X3[-1]]])
Xg = np.array([[0, L], [0, L]])
Yg = np.array([[0, 0], [W, W]])
fig.add_trace(go.Surface(x=Xg, y=Yg, z=Z_final,
                         colorscale="Oranges", opacity=0.8,
                         showscale=False),
              row=1, col=1)

# --- Cone (quiver) showing wind force direction at t=0 ---
# cones anchored at corners, pointing in +x direction scaled by F0/k0
u = np.array([F0/k0]*4)
v = np.zeros(4)
w = np.zeros(4)
fig.add_trace(go.Cone(x=corners[:,0], y=corners[:,1], z=[0]*4,
                      u=u, v=v, w=w, sizemode="absolute", sizeref=2,
                      anchor="tip", colorscale="Blues"),
              row=1, col=2)

# --- 3D time-history of corner 1 as a line (z=time) ---
fig.add_trace(go.Scatter3d(x=times, y=X1, z=X1*0+5, mode="lines",
                           line=dict(color="firebrick", width=4)),
              row=1, col=3)

# layout tweaks
fig.update_layout(
    height=500, width=1500,
    title_text="Unified 3D Visualizations: Deck, Wind & Time History"
)

# axes labels
fig.update_scenes(dict(xaxis_title="X (m)", yaxis_title="Y (m)", zaxis_title="Z (m)"),
                  row=1, col=1)
fig.update_scenes(dict(xaxis_title="X (m)", yaxis_title="Y (m)", zaxis_title="Z (m)"),
                  row=1, col=3)

fig.show()

# at the end of your plotting script, after fig.show():
fig.write_html(
    "index.html",             # this must be named `index.html` for Pages
    include_plotlyjs="cdn",   # pulls Plotly from the CDN
    full_html=True
)
