import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import TransferFunction, bode

# 1) System parameters
m = 1000.0                 # mass (kg)
k = 4e4                    # stiffness (N/m)
zeta = 0.05                # damping ratio
c = 2 * zeta * np.sqrt(k * m)  # damping coefficient

# 2) Build transfer function H(s) = 1 / (m s^2 + c s + k)
num = [1.0]
den = [m, c, k]
sys = TransferFunction(num, den)

# 3) Compute Bode data
w = np.logspace(-1, 2, 500)    # rad/s from 0.1 to 100
w, mag, phase = bode(sys, w=w)

# 4) Plot magnitude (dB) and phase (deg)
fig, (ax1, ax2) = plt.subplots(2,1, figsize=(8,6), sharex=True)

ax1.semilogx(w, mag, 'b', lw=2)
ax1.set_ylabel('Magnitude (dB)')
ax1.set_title('Bode Plot of Bridge SDOF Transfer Function')
ax1.grid(True, which='both', ls='--', alpha=0.5)

ax2.semilogx(w, phase, 'r', lw=2)
ax2.set_xlabel('Frequency (rad/s)')
ax2.set_ylabel('Phase (deg)')
ax2.grid(True, which='both', ls='--', alpha=0.5)

plt.tight_layout()
plt.show()
# Save the figure
plt.savefig("Bode_Plot_Bridge_SDOF.png", dpi=300)