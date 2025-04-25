import numpy as np
import plotly.graph_objects as go

# 1) System parameters
m, k, F0 = 1000.0, 4e4, 1000.0
omega_n = np.sqrt(k/m)
zeta = 0.05

# 2) Grid in time (T) and forcing frequency ratio (Ω)
t = np.linspace(0, 20, 200)           # 0–20 s
ratio = np.linspace(0.5, 1.5, 80)     # 0.5–1.5·ω_n
Ω = ratio * omega_n
T, R = np.meshgrid(t, ratio)

# 3) Steady‐state amplitude X and phase φ
denom = np.sqrt((omega_n**2 - (R*omega_n)**2)**2 + (2*zeta*omega_n*(R*omega_n))**2)
X = (F0/m) / denom
phi = np.arctan2(2*zeta*omega_n*(R*omega_n), omega_n**2 - (R*omega_n)**2)

# 4) Displacement surface: x = X·sin(Ω·T − φ)
Disp = X * np.sin(R*omega_n*T - phi)

# 5) Plotly 3D surface
fig = go.Figure(data=go.Surface(
    x=T, y=R*omega_n, z=Disp,
    colorscale='Viridis', cmin=-X.max(), cmax= X.max(),
    colorbar=dict(title='x (m)')
))
fig.update_layout(
    title="Bridge Steady-State Response vs Time & Forcing Frequency",
    scene=dict(
        xaxis_title="Time (s)",
        yaxis_title="Ω (rad/s)",
        zaxis_title="Displacement x (m)"
    ),
    autosize=False,
    width=800, height=600
)
fig.show()
# To export: fig.write_html("time_frequency_surface.html", include_plotlyjs='cdn')
# )
fig.write_html("time_frequency_surface.html", include_plotlyjs="cdn", full_html=True)
