import numpy as np
import plotly.graph_objects as go

# === 1) Physical / simulation parameters ===
m = 1000.0             # mass (kg)
k = 4e4                # stiffness (N/m)
omega_n = np.sqrt(k/m) # natural frequency (rad/s)
F0 = 1000.0            # forcing amplitude (N)
zeta = 0.05            # damping ratio – change as desired

# === 2) RK4 time‑history for displacement A(t) ===
def deriv(y, t, z):
    x, v = y
    c = 2*z*np.sqrt(k*m)
    F = F0*np.sin(omega_n*t)        # harmonic force at ω_n
    return np.array([v, (F - c*v - k*x)/m])

# time array
t = np.linspace(0, 20, 400)
h = t[1] - t[0]
y = np.array([0.0, 0.0])             # initial conditions [x(0), v(0)]
A = np.zeros_like(t)                 # to store x(t)

for i, ti in enumerate(t):
    A[i] = y[0]
    k1 = deriv(y, ti,     zeta)
    k2 = deriv(y+0.5*h*k1, ti+0.5*h, zeta)
    k3 = deriv(y+0.5*h*k2, ti+0.5*h, zeta)
    k4 = deriv(y+  h*k3, ti+   h,   zeta)
    y += (h/6)*(k1 + 2*k2 + 2*k3 + k4)

# === 3) First‑mode shape of a simply supported span ===
L = 10.0                             # span length (m)
x = np.linspace(0, L, 100)          # spatial discretization
phi = np.sin(np.pi * x / L)         # mode shape

# === 4) Build animation frames ===
frames = []
for ti, Ai in zip(t, A):
    w = Ai * phi                    # displacement at each x
    trace = go.Scatter3d(
        x=x, y=np.zeros_like(x), z=w,
        mode='lines',
        line=dict(color='royalblue', width=4),
    )
    frames.append(go.Frame(data=[trace], name=f'{ti:.2f}s'))

# === 5) Initial trace & figure setup ===
fig = go.Figure(
    data=frames[0].data,
    frames=frames,
    layout=go.Layout(
        title="Bridge Deck Oscillation (1st Mode)",
        scene=dict(
            xaxis_title='Span (m)',
            yaxis_title='',
            zaxis_title='Deflection (m)',
            aspectratio=dict(x=2, y=0.2, z=0.5)
        ),
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            y=1.05,
            x=0.1,
            xanchor='right',
            yanchor='top',
            buttons=[dict(
                label='▶ Play',
                method='animate',
                args=[None, {
                    'frame': {'duration': 50, 'redraw': True},
                    'fromcurrent': True
                }]
            )]
        )]
    )
)

# Show!
fig.show()
