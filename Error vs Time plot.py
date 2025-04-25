import pandas as pd
import matplotlib.pyplot as plt

# 1) Load your steady-state table (with errors already computed)
df = pd.read_csv("steady_state_error.csv")  # or whichever filename you chose

# 2) Plot Absolute and Relative error vs Time
plt.figure(figsize=(10,5))

# Absolute error (left y-axis)
ax1 = plt.gca()
ax1.plot(df["Time (s)"], df["Absolute Error (m)"],
         color="tab:blue", lw=2, label="Absolute Error (m)")
ax1.set_ylabel("Absolute Error (m)", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")

# Relative error (right y-axis)
ax2 = ax1.twinx()
ax2.plot(df["Time (s)"], df["Relative Error (%)"],
         color="tab:red", lw=2, label="Relative Error (%)")
ax2.set_ylabel("Relative Error (%)", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")

# Finish up
plt.title("Error vs. Time in Steady-State Region (t ≥ 10 s)")
ax1.set_xlabel("Time (s)")
ax1.grid(which="both", ls="--", alpha=0.5)
fig = plt.gcf()
fig.tight_layout()
plt.show()
# Save the figure
plt.savefig("error_vs_time.png", dpi=300)