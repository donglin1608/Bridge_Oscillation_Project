import numpy as np
import plotly.graph_objects as go

# 1) Physical parameters
m = 1000.0      # mass (kg)
k = 4e4         # stiffness (N/m)
omega_n = np.sqrt(k / m)  # natural frequency
F0 = 1000.0     # forcing amplitude (N)

# 2) Grid definition (refine resolution as needed)
t = np.linspace(0, 20, 60)    # time axis (s)
zetas = np.linspace(0, 2, 30) # damping ratio axis
T, Z = np.meshgrid(t, zetas)

# 3) Slider over excitation frequency ratios (Ω = ratio * ω_n)
ratios = [0.8, 0.9, 1.0, 1.1, 1.2]
Omegas = omega_n * np.array(ratios)

frames = []
for r, Omega in zip(ratios, Omegas):
    # steady-state amplitude and phase
    denom = np.sqrt((omega_n**2 - Omega**2)**2 + (2*Z*omega_n*Omega)**2)
    X = (F0/m) / denom
    phi = np.arctan2(2*Z*omega_n*Omega, omega_n**2 - Omega**2)

    # displacement surface
    disp = X * np.sin(Omega*T - phi)
    # normalized wind acceleration surface
    accel = (F0*np.sin(Omega*T)) / m

    frames.append(go.Frame(
        name=f"{r:.1f}·ωₙ",
        data=[
            go.Surface(x=T, y=Z, z=disp, showscale=False, opacity=0.9,
                       hovertemplate="t=%{x:.1f}s, ζ=%{y:.1f}, x=%{z:.3f}m"),
            go.Surface(x=T, y=Z, z=accel, showscale=False, opacity=0.5,
                       colorscale="Viridis",
                       hovertemplate="t=%{x:.1f}s, ζ=%{y:.1f}, a=%{z:.2f}m/s²")
        ]
    ))

# 4) Initial data (mid-frequency)
initial_data = frames[2].data
fig = go.Figure(data=initial_data, frames=frames)

# 5) Slider setup
steps = [
    dict(
        method="animate",
        args=[[fr.name], {"mode": "immediate", "frame": {"duration": 0}}],
        label=fr.name
    ) for fr in frames
]

fig.update_layout(
    title="3D Bridge Response & Wind Force vs. Frequency",
    scene=dict(
        xaxis_title="Time (s)",
        yaxis_title="Damping ζ",
        zaxis_title="Magnitude"
    ),
    sliders=[dict(
        active=2,
        currentvalue={"prefix": "Ω = "},
        pad={"t": 60},
        steps=steps
    )]
)

# 6) Export as a standalone HTML for GitHub Pages
fig.write_html(
    "bridge_response_3d.html",
    include_plotlyjs="cdn",  # loads plotly.js from CDN
    full_html=True
)

print("Exported interactive plot to bridge_response_3d.html")
