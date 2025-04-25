import numpy as np
import matplotlib.pyplot as plt

# === 1) TIME ARRAY ===
omega_n = 1.0                    # normalized natural frequency
t_vals = np.linspace(0, 10, 500) # simulate 0–10 s

# === 2) UNDERDAMPED RESPONSE (ζ < 1) ===
zeta_u = 0.5
omega_d = omega_n * np.sqrt(1 - zeta_u**2)
A_u = 1.0
B_u = zeta_u / np.sqrt(1 - zeta_u**2)
x_vals_underdamped = np.exp(-zeta_u*omega_n*t_vals) * (
        A_u * np.cos(omega_d*t_vals) + B_u * np.sin(omega_d*t_vals)
)

# === 3) CRITICAL DAMPING (ζ = 1) ===
zeta_c = 1.0
x_vals_critical = (1 + omega_n*t_vals) * np.exp(-omega_n*t_vals)

# === 4) OVERDAMPED RESPONSE (ζ > 1) ===
zeta_o = 2.0
sqrt_term = np.sqrt(zeta_o**2 - 1)
lam1 = -omega_n*(zeta_o - sqrt_term)
lam2 = -omega_n*(zeta_o + sqrt_term)
A_o = lam2 / (lam2 - lam1)
B_o = -lam1 / (lam2 - lam1)
x_vals_overdamped = A_o*np.exp(lam1*t_vals) + B_o*np.exp(lam2*t_vals)

# === 5) PLOT COMPARISON ===
plt.figure(figsize=(10, 6))
plt.plot(t_vals, x_vals_underdamped, label="Underdamped (ζ=0.5)",  color="blue",  lw=2)
plt.plot(t_vals, x_vals_critical,   label="Critical (ζ=1.0)",   color="green", lw=2)
plt.plot(t_vals, x_vals_overdamped, label="Overdamped (ζ=2.0)", color="red",   lw=2)

plt.xlabel("Time (s)")
plt.ylabel("Displacement x(t) (m)")
plt.title("Damping Comparison: Under, Critical, Over")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
# Save the figure
plt.savefig("Damping_Comparison.png", dpi=300)