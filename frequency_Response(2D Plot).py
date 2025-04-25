import numpy as np
import matplotlib.pyplot as plt

# === SYSTEM PARAMETERS ===
m = 1000.0         # Mass (kg)
k = 4e4            # Stiffness (N/m)
omega_n = np.sqrt(k / m)  # Natural frequency (rad/s)
zeta = 0.05        # Damping ratio
F0 = 1000.0        # Forcing amplitude (N)

# Damping coefficient (for steady-state calculation)
c = 2 * zeta * np.sqrt(k * m)

# === AMPLITUDE CALCULATION FUNCTION ===
def calculate_amplitude(omega):
    """
    Compute steady-state amplitude X for harmonic forcing at frequency omega.
    X = (F0/m) / sqrt((omega_n^2 - omega^2)^2 + (2*zeta*omega_n*omega)^2)
    """
    denom = np.sqrt((omega_n**2 - omega**2)**2 + (2*zeta*omega_n*omega)**2)
    return (F0 / m) / denom

# === FREQUENCY RESPONSE DATA ===
frequencies = np.linspace(0.5 * omega_n, 2 * omega_n, 100)
amplitudes = np.array([calculate_amplitude(omega) for omega in frequencies])

# === PLOT ===
plt.figure(figsize=(10, 6))
plt.plot(frequencies, amplitudes, lw=2)
plt.xlabel("Frequency (rad/s)")
plt.ylabel("Steady-State Amplitude, X (m)")
plt.title("Frequency Response of the SDOF Bridge Model (ζ=0.05)")
plt.grid(True)
plt.tight_layout()
plt.show()
