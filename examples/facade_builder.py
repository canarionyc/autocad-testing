import argparse
import math
import matplotlib.pyplot as plt
from pyautocad import Autocad, APoint

# --- Constants ---
WIDTH = 20.0
HEIGHT_EAVES = 15.0
X_INSET = 4 * math.sqrt(2)  # approx 5.657


def get_window_rects():
    """
    Generates a list of Closed Polylines (rectangles) for the windows.
    Returns: List of [ (x1,y1), (x2,y2), (x3,y3), (x4,y4), (x1,y1) ]
    """
    # 1. Window Dimensions
    w_width = 1.0
    w_height = 1.0

    # 2. Define Center X coordinates for the 3 columns
    # Col 1: Center of left gable
    x_col1 = 0.5 * X_INSET
    # Col 2: Center of the whole building
    x_col2 = 0.5 * WIDTH
    # Col 3: Center of right gable (Symmetric to Col 1 from the right)
    x_col3 = WIDTH - (0.5 * X_INSET)

    col_centers = [x_col1, x_col2, x_col3]

    # 3. Define Sill Heights (Y coordinates of the bottom edge)
    sill_heights = [2.5, 5.0, 8.0, 11.0]

    windows = []

    # 4. Generate Geometry
    for x_center in col_centers:
        for y_sill in sill_heights:
            # Calculate corners based on center X and sill Y
            x_left = x_center - (w_width / 2)
            x_right = x_center + (w_width / 2)
            y_bottom = y_sill
            y_top = y_sill + w_height

            # Define the 4 corners + closing point
            rect = [
                (x_left, y_bottom),  # Bottom Left
                (x_right, y_bottom),  # Bottom Right
                (x_right, y_top),  # Top Right
                (x_left, y_top),  # Top Left
                (x_left, y_bottom)  # Close Loop
            ]
            windows.append(rect)

    return windows


def plot_on_screen(polygons):
    """Visualizes the windows using Matplotlib."""
    print(f"Plotting {len(polygons)} windows...")

    plt.figure(figsize=(10, 6))

    # Draw Building Outline (Reference)
    plt.plot([0, WIDTH, WIDTH, 0, 0], [0, 0, HEIGHT_EAVES, HEIGHT_EAVES, 0], 'k--', alpha=0.3)

    for poly in polygons:
        x_vals, y_vals = zip(*poly)
        plt.fill(x_vals, y_vals, color='cyan', alpha=0.5, edgecolor='blue')

    plt.title("Facade Window Layout")
    plt.xlabel("Width (m)")
    plt.ylabel("Height (m)")
    plt.axis('equal')
    plt.grid(True)
    plt.show()


def send_to_autocad(polygons):
    """Draws the window rectangles in AutoCAD."""
    try:
        acad = Autocad(create_if_not_exists=True)
        print(f"Connected to: {acad.doc.Name}")
    except:
        print("Error: AutoCAD not found.")
        return

    print("Drawing windows...")

    for poly in polygons:
        # Convert list of tuples to flat list of doubles [x1, y1, 0, x2, y2, 0...]
        # AutoCAD LightweightPolyline requires this specific format
        flat_coords = []
        for x, y in poly[:-1]:  # Skip the last point (AutoCAD closes it automatically)
            flat_coords.extend([x, y])

        # Create Lightweight Polyline
        # Note: pyautocad handles the array conversion automatically usually,
        # but sometimes requires distinct points. Let's try AddLightWeightPolyline.

        # Alternative: Draw 4 lines if Polyline fails in simple API
        for i in range(len(poly) - 1):
            p1 = APoint(poly[i][0], poly[i][1])
            p2 = APoint(poly[i + 1][0], poly[i + 1][1])
            acad.model.AddLine(p1, p2)

    print(f"Done. {len(polygons)} windows added.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--draw", action="store_true")
    group.add_argument("--send", action="store_true")

    args = parser.parse_args()
    geometry = get_window_rects()

    if args.draw:
        plot_on_screen(geometry)
    elif args.send:
        send_to_autocad(geometry)