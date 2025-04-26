import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Bridge parameters
rows, cols = 5, 5  # grid size
spacing = 1.0      # spacing between masses
F_w = 5.0          # wind force (N)
k = 10.0           # spring constant (N/m)

# Generate grid of masses
x = np.linspace(0, (cols - 1) * spacing, cols)
y = np.linspace(0, (rows - 1) * spacing, rows)
X, Y = np.meshgrid(x, y)

# Calculate displacement due to wind force
# Assuming each mass displaces by F_w / k in the x-direction
Z = np.zeros_like(X)  # No vertical displacement
U = (F_w / k) * np.ones_like(X)  # Displacement in x-direction
V = np.zeros_like(Y)  # No displacement in y-direction

# Plotting
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X, Y, Z, U, V, Z, length=0.1, normalize=True, color='blue')
ax.set_title('3D Visualization of Bridge Deck Deformation')
ax.set_xlabel('X Position (m)')
ax.set_ylabel('Y Position (m)')
ax.set_zlabel('Z Position (m)')
plt.show()