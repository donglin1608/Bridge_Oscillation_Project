import numpy as np
import matplotlib.pyplot as plt

# === PARAMETERS ===
omega_n = 1.0               # normalized natural frequency (rad/s)
t_vals = np.linspace(0, 60, 2000)  # If you want, you can change the time range to check it out different response

# Damping ratios
zeta_under  = 0.5   # underdamped (0 < ζ < 1)
zeta_crit   = 1.0   # critically damped (ζ = 1)
zeta_over   = 2.0   # overdamped (ζ > 1)

# === UNDERDAMPED RESPONSE ===
omega_d = omega_n * np.sqrt(1 - zeta_under**2)
# x(0)=1, x'(0)=0 ⇒ A=1, B=ζ/√(1−ζ²)
A_u = 1.0
B_u = zeta_under / np.sqrt(1 - zeta_under**2)
x_vals_underdamped = np.exp(-zeta_under*omega_n*t_vals) * (
        A_u * np.cos(omega_d*t_vals) +
        B_u * np.sin(omega_d*t_vals)
)

# === CRITICAL DAMPING ===
# x_h(t) = (C1 + C2 t) e^{-ω_n t}, with x(0)=1, x'(0)=0 ⇒ C1=1, C2=ω_n
x_vals_critical = (1 + omega_n*t_vals) * np.exp(-omega_n*t_vals)

# === OVERDAMPED RESPONSE ===
# Roots λ1,2 = -ζω_n ± ω_n√(ζ²−1)
sqrt_term = np.sqrt(zeta_over**2 - 1)
lambda1 = -omega_n*(zeta_over - sqrt_term)
lambda2 = -omega_n*(zeta_over + sqrt_term)
# Coeffs from x(0)=1, x'(0)=0 ⇒
#   A + B = 1
#   A*λ1 + B*λ2 = 0  ⇒  A = λ2/(λ2−λ1), B = -λ1/(λ2−λ1)
A_o =  lambda2 / (lambda2 - lambda1)
B_o = -lambda1 / (lambda2 - lambda1)
x_vals_overdamped = A_o*np.exp(lambda1*t_vals) + B_o*np.exp(lambda2*t_vals)

# === PLOT ===
plt.figure(figsize=(10, 6))
plt.plot(t_vals, x_vals_overdamped,  label="Overdamped (ζ=2.0)",   color="red",    lw=2)
plt.plot(t_vals, x_vals_underdamped, label="Underdamped (ζ=0.5)",  color="blue",   lw=2)
plt.plot(t_vals, x_vals_critical,   label="Critically Damped (ζ=1)", color="green", lw=2)

plt.xlabel("Time (s)", fontsize=14)
plt.ylabel("Displacement $x(t)$ (m)", fontsize=14)
plt.title("Effect of Damping on Free Vibration Response", fontsize=16)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()
# Save the figure
plt.savefig("Effect_of_Damping_on_Displacement.png", dpi=300)
