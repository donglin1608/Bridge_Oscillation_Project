#!/usr/bin/env python3
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# --- System Parameters ---
m = 1000
k = 20000
omega_n = np.sqrt(k / m)
zeta = 0.05
c = 2 * zeta * omega_n * m

# --- Wind Forcing ---
F0 = 1000
Omega = omega_n
def F(t): return F0 * np.sin(Omega * t)

# --- Time Setup ---
T, dt = 60, 0.01
t_vals = np.arange(0, T + dt, dt)

# --- Initial Conditions ---
x0, v0 = 0.0, 0.0
y = np.array([x0, v0])
x_vals = []

# --- RK4 Integrator ---
def deriv(t, y):
    x, v = y
    return np.array([v, (F(t) - c*v - k*x)/m])

for t in t_vals:
    x_vals.append(y[0])
    k1 = deriv(t,         y)
    k2 = deriv(t+dt/2,    y+dt/2*k1)
    k3 = deriv(t+dt/2,    y+dt/2*k2)
    k4 = deriv(t+dt,      y+dt*k3)
    y += (dt/6)*(k1+2*k2+2*k3+k4)

x_vals = np.array(x_vals)

# --- Analytical Solution ---
omega_d = omega_n*np.sqrt(1-zeta**2)
X   = (F0/m)/np.sqrt((omega_n**2-Omega**2)**2+(2*zeta*omega_n*Omega)**2)
phi = np.arctan2(2*zeta*omega_n*Omega, omega_n**2-Omega**2)
A   = x0 + X*np.sin(phi)
B   = (zeta*omega_n*A - Omega*X*np.cos(phi))/omega_d

def x_analytical(t):
    return (np.exp(-zeta*omega_n*t)*(A*np.cos(omega_d*t)+B*np.sin(omega_d*t))
            + X*np.sin(Omega*t - phi))

x_exact_vals = x_analytical(t_vals)

# --- Steady‑State Error (t ≥ 40 s) ---
mask      = t_vals >= 40
t_out     = t_vals[mask]
x_pred    = x_vals[mask]
x_theory  = x_exact_vals[mask]
abs_error = np.abs(x_pred - x_theory)
rel_error = abs_error/np.maximum(np.abs(x_theory),1e-10)*100

df_steady_error = pd.DataFrame({
    "Time (s)":           t_out,
    "X_exact (m)":        x_theory,
    "X_predicted (m)":    x_pred,
    "Absolute Error (m)": abs_error,
    "Relative Error (%)": rel_error
})

print(df_steady_error.head(10))

# --- Plot Response ---
fig, ax = plt.subplots(figsize=(14,6))
ax.plot(t_vals, x_vals,       label="RK4 Numerical", linewidth=2)
ax.plot(t_vals, x_exact_vals, '--', label="Analytical",  linewidth=2)
ax.axhline(F0/k, color='gray', linestyle='--', label='$F_0/k$')
ax.set(xlabel="Time (s)", ylabel="Displacement $x(t)$ [m]",
       title="Bridge Response Under Harmonic Wind Load")
ax.legend(); ax.grid(True)
fig.tight_layout()

# --- Output Dir & Save CSV/XLSX ---
out_dir = os.getcwd()
os.makedirs(out_dir, exist_ok=True)
csv_path  = os.path.join(out_dir, "steady_state_error.csv")
xlsx_path = os.path.join(out_dir, "steady_state_error.xlsx")
df_steady_error.to_csv(csv_path, index=False)
df_steady_error.to_excel(xlsx_path, index=False)
print(f"Saved:\n • {csv_path}\n • {xlsx_path}")

# --- Save Main Plot ---
plot_path = os.path.join(out_dir, "bridge_response.png")
fig.savefig(plot_path, dpi=300, bbox_inches='tight')
print(f"Plot → {plot_path}")

# --- Save Table Image with Mixed Formatting ---
table_df = df_steady_error.head(20).copy()

# format columns
table_df["Time (s)"]           = table_df["Time (s)"].map(lambda x: f"{x:.2f}")
table_df["X_exact (m)"]        = table_df["X_exact (m)"].map(lambda x: f"{x:.6f}")
table_df["X_predicted (m)"]    = table_df["X_predicted (m)"].map(lambda x: f"{x:.6f}")
table_df["Absolute Error (m)"] = table_df["Absolute Error (m)"].map(lambda x: f"{x:.8f}")
table_df["Relative Error (%)"] = table_df["Relative Error (%)"].map(lambda x: f"{x:.6f}")

fig2, ax2 = plt.subplots(figsize=(12,6))
ax2.axis("off")
tbl = ax2.table(cellText=table_df.values,
                colLabels=table_df.columns,
                loc="center")
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1,1.5)

# make room and place title below the table
# --- Save Table Image with Perfectly Centered Footer Title ---

table_df = df_steady_error.head(20).copy()
# format columns…
table_df["Time (s)"]           = table_df["Time (s)"].map(lambda x: f"{x:.2f}")
table_df["X_exact (m)"]        = table_df["X_exact (m)"].map(lambda x: f"{x:.6f}")
table_df["X_predicted (m)"]    = table_df["X_predicted (m)"].map(lambda x: f"{x:.6f}")
table_df["Absolute Error (m)"] = table_df["Absolute Error (m)"].map(lambda x: f"{x:.8f}")
table_df["Relative Error (%)"] = table_df["Relative Error (%)"].map(lambda x: f"{x:.6f}")

fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.axis("off")
tbl = ax2.table(
    cellText=table_df.values,
    colLabels=table_df.columns,
    loc="center"
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1, 1.5)

# carve out a bottom margin...
bottom_margin = 0.15
fig2.subplots_adjust(bottom=bottom_margin)

# place the title exactly halfway down that margin
title_y = bottom_margin / 2
fig2.text(
    0.5, title_y,
    "Table: Steady‑State Error (First 20 Rows)",
    ha="center", va="center", fontsize=12
)

table_img_path = os.path.join(out_dir, "steady_state_error_table.png")
fig2.savefig(table_img_path, dpi=300, bbox_inches='tight')
plt.close(fig2)
print(f"Table image → {table_img_path}")



