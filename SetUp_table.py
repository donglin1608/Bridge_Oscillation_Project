import numpy as np
import pandas as pd

# Re-run simulation to get data
m = 1000.0
k = 4e4
omega_n = np.sqrt(k / m)
F0 = 1000.0
Omega = omega_n
h = 0.01
t = np.arange(0, 20 + h, h)
zetas = [0.0, 0.05, 0.5, 2.0]

def deriv(y, time, zeta):
    x, v = y
    c = 2 * zeta * np.sqrt(k * m)
    F = F0 * np.sin(Omega * time)
    dxdt = v
    dvdt = (F - c * v - k * x) / m
    return np.array([dxdt, dvdt])

# Run RK4 simulation
results = {}
for z in zetas:
    y = np.array([0.0, 0.0])
    xs = []
    for ti in t:
        k1 = deriv(y, ti, z)
        k2 = deriv(y + 0.5*h*k1, ti + 0.5*h, z)
        k3 = deriv(y + 0.5*h*k2, ti + 0.5*h, z)
        k4 = deriv(y + h*k3, ti + h, z)
        y = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        xs.append(y[0])
    results[z] = np.array(xs)

# Helper to get values at specific times
def get_values(times, absolute=False):
    indices = [np.searchsorted(t, time) for time in times]
    data = {'Time (s)': times}
    for z in zetas:
        vals = np.abs(results[z][indices]) if absolute else results[z][indices]
        data[f'zeta={z}'] = vals
    return pd.DataFrame(data)

# Table 1: Time-history sample
times1 = [0, 4, 8, 12, 16, 20]
df_timehistory = get_values(times1, absolute=False)

# Table 2: Steady-state sample
times2 = [10, 12, 14, 16, 18, 20]
df_steady_state = get_values(times2, absolute=False)

# Table 3: Envelope (absolute value)
times3 = [1, 5, 10, 15, 20]
df_envelope = get_values(times3, absolute=True)

# Export to CSV
df_timehistory.to_csv("time_history_samples.csv", index=False)
df_steady_state.to_csv("steady_state_samples.csv", index=False)
df_envelope.to_csv("envelope_samples.csv", index=False)

print("Exported CSV files: time_history_samples.csv, steady_state_samples.csv, envelope_samples.csv")
