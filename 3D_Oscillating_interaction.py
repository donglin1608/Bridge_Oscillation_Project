import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1) Prepare the surface data (steady‑state)
m, k, F0 = 1000, 4e4, 1000
ωn = np.sqrt(k/m)
t = np.linspace(0,20,60)
ζ = np.linspace(0,2,30)
T, Z = np.meshgrid(t, ζ)
Ω = ωn
den = np.sqrt((ωn**2 - Ω**2)**2 + (2*Z*ωn*Ω)**2)
X = (F0/m) / den
ϕ = np.arctan2(2*Z*ωn*Ω, ωn**2 - Ω**2)
disp = X * np.sin(Ω*T - ϕ)
accel = (F0 * np.sin(Ω*T)) / m

# 2) Prepare the mode‑shape line data (animation)
L = 10.0
x = np.linspace(0, L, 100)
mode = np.sin(np.pi * x / L)
t2 = np.linspace(0, 5, 50)
A2 = np.sin(ωn * t2) * 0.1

# 3) Build a 1×2 subplot: left is static surfaces, right is animated line
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"type":"surface"}, {"type":"scene"}]],
    subplot_titles=["Steady‑State Response", "Mode‑Shape Animation"]
)

# Add the two static surface traces
fig.add_trace(go.Surface(x=T, y=Z, z=disp, showscale=False, opacity=0.9), row=1, col=1)
fig.add_trace(go.Surface(x=T, y=Z, z=accel, showscale=False, opacity=0.5, colorscale="Viridis"), row=1, col=1)

# Add the initial line trace for the beam
init_line = go.Scatter3d(
    x=x,
    y=np.zeros_like(x),
    z=A2[0] * mode,
    mode="lines",
    line=dict(color="crimson", width=4),
)
fig.add_trace(init_line, row=1, col=2)

# 4) Build animation frames
frames = []
for Ai in A2:
    line_trace = go.Scatter3d(
        x=x,
        y=np.zeros_like(x),
        z=Ai * mode,
        mode="lines",
        line=dict(color="crimson", width=4),
    )
    # frame.data must be a list of three traces:
    #   [surface1, surface2, updated_line]
    frames.append(go.Frame(data=[fig.data[0], fig.data[1], line_trace]))

fig.frames = frames

# 5) Add Play button and layout fixes
fig.update_layout(
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        buttons=[dict(
            label="▶ Play",
            method="animate",
            args=[None, {
                "frame": {"duration": 100, "redraw": True},
                "fromcurrent": True
            }]
        )]
    )],
    height=600,           # use '=' not '=='
    width=1000,
    title="3D Bridge Response & Mode‑Shape Animation"
)

# 6) Export a single HTML file for GitHub Pages
fig.write_html(
    "multi_viz.html",
    include_plotlyjs="cdn",
    full_html=True
)

print("✔️  Exported interactive page to multi_viz.html")
