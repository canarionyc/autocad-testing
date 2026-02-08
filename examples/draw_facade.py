# %% setup
import numpy as np
import matplotlib.pyplot as plt

from pyautocad import Autocad, APoint

# Connect to the running AutoCAD instance
acad = Autocad(create_if_not_exists=True)

# Define your points (or read from a file)
# Format: [x, y, z]
points = [
    [0.0, 0.0, 0.0],
    [20.0, 0.0, 0.0],
    [20.0, 15.0, 0.0],
    [14.343146, 15.0, 0.0],  # Your calculated point
    [10.0, 17.83, 0.0],      # Roof Apex
    [5.656854, 15.0, 0.0],   # Other side
    [0.0, 15.0, 0.0],
    [0.0, 0.0, 0.0]          # Close the loop
]

# Draw the lines
for i in range(len(points) - 1):
    p1 = APoint(points[i])
    p2 = APoint(points[i+1])
    acad.model.AddLine(p1, p2)

print(f"Successfully drew {len(points)-1} lines.")