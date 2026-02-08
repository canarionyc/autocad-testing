import argparse
import math
import matplotlib.pyplot as plt
from pyautocad import Autocad, APoint


# def get_facade_points():
#     """
#     Calculates coordinates for a symmetric facade with two gabled ends.
#     Geometry:
#       - Two side gables with 45-degree slopes (Rise = Run).
#       - A flat connecting section in the middle.
#     """
#     # 1. Define Base Dimensions
#     width = 20.0
#     height_eaves = 15.0
#
#     # 2. Calculate Inset and Gable Geometry
#     # x_inset is the horizontal width of the sloped roof section
#     x_inset = 4 * math.sqrt(2)  # approx 5.6568
#
#     # User Formula: extra height is half the inset width (implies 45-degree slope)
#     height_gable = x_inset / 2  # approx 2.8284
#
#     total_peak_height = height_eaves + height_gable  # approx 17.83
#
#     # 3. Calculate Key X Coordinates (Symmetric)
#     x0 = 0.0
#     x1 = x_inset / 2  # Left Peak X
#     x2 = x_inset  # Left Valley X (Start of flat middle)
#
#     x3 = width - x_inset  # Right Valley X (End of flat middle)
#     x4 = width - (x_inset / 2)  # Right Peak X
#     x5 = width
#
#     # 4. Define the Path (Counter-Clockwise starting from 0,0)
#     points = [
#         (x0, 0),  # 1. Bottom Left
#         (x5, 0),  # 2. Bottom Right
#         (x5, height_eaves),  # 3. Eave Right
#         (x4, total_peak_height),  # 4. Right Peak
#         (x3, height_eaves),  # 5. Right Valley
#         (x2, height_eaves),  # 6. Left Valley
#         (x1, total_peak_height),  # 7. Left Peak
#         (x0, height_eaves),  # 8. Eave Left
#         (x0, 0)  # 9. Close Loop
#     ]
#
#     return points
#
#
# def plot_on_screen(points):
#     """Visualizes the geometry using Matplotlib."""
#     print(f"Plotting {len(points)} points...")
#     x_vals, y_vals = zip(*points)
#
#     plt.figure(figsize=(12, 6))
#     plt.plot(x_vals, y_vals, '-o', color='blue', linewidth=2, label='Facade Outline')
#
#     # Annotate points
#     for i, (x, y) in enumerate(points):
#         # Offset text slightly for readability
#         plt.text(x, y + 0.5, f"P{i}\n({x:.2f}, {y:.2f})",
#                  fontsize=8, ha='center', color='darkred')
#
#     plt.title(f"Symmetric Facade Geometry\nWidth: 20.0m | Eave: 15.0m | Peak: {max(y_vals):.2f}m")
#     plt.xlabel("Distance (m)")
#     plt.ylabel("Height (m)")
#     plt.axhline(0, color='black', linewidth=1)
#     plt.grid(True, linestyle='--', alpha=0.6)
#     plt.axis('equal')
#     plt.show()

def plot_on_screen(lines):
    """
    Visualizes specific LINE SEGMENTS using Matplotlib.
    Expects input format: [ ((x1, y1), (x2, y2)), ... ]
    """
    print(f"Plotting {len(lines)} independent lines...")

    plt.figure(figsize=(10, 8))

    # Iterate through each line segment and plot it individually
    for i, (start_pt, end_pt) in enumerate(lines):
        # Extract X and Y for this single line
        x_vals = [start_pt[0], end_pt[0]]
        y_vals = [start_pt[1], end_pt[1]]

        # Plot the line
        plt.plot(x_vals, y_vals, marker='o', linestyle='-', color='blue', linewidth=2)

        # Label the start point of each line for reference
        plt.text(start_pt[0], start_pt[1], f" L{i + 1}\nStart", fontsize=8, ha='right', color='red')

    plt.title("Facade Internal Lines Preview")
    plt.xlabel("Width (m)")
    plt.ylabel("Height (m)")

    # Set fixed limits so it looks like the building
    plt.xlim(-1, 21)
    plt.ylim(-1, 19)
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def get_facade_points():
    """
    Returns ONLY the internal vertical lines for the facade.
    Structure: [ [start_point, end_point], [start_point, end_point] ... ]
    """
    width = 20.0
    height_eaves = 15.0

    # Calculate Inset
    x_inset = 4 * math.sqrt(2)  # approx 5.657

    x2 = x_inset  # Left Valley (Start of flat middle)
    x3 = width - x_inset  # Right Valley (End of flat middle)

    # Define the TWO vertical lines you are missing
    # Format: Tuple of (Start, End)
    lines_to_draw = [
        ((x2, 0), (x2, height_eaves)),  # Left Internal Wall
        ((x3, 0), (x3, height_eaves))  # Right Internal Wall
    ]

    return lines_to_draw


def send_to_autocad(lines_list):
    """Draws specific lines in AutoCAD."""
    try:
        acad = Autocad(create_if_not_exists=True)
        print(f"Connected to: {acad.doc.Name}")
    except:
        print("Error: AutoCAD not found.")
        return

    print("Drawing internal lines...")

    # Loop through the LIST of lines (not a continuous path)
    for start_pt, end_pt in lines_list:
        p1 = APoint(start_pt[0], start_pt[1])
        p2 = APoint(end_pt[0], end_pt[1])
        acad.model.AddLine(p1, p2)

    print(f"Done. {len(lines_list)} lines added.")



# def send_to_autocad(points):
#     """Sends the calculated points to the active AutoCAD drawing."""
#     try:
#         acad = Autocad(create_if_not_exists=True)
#         print(f"Connected to Active Drawing: {acad.doc.Name}")
#     except Exception as e:
#         print("Error: Could not connect to AutoCAD. Ensure it is running.")
#         return
#
#     print("Drawing vectors...")
#
#     # Draw simple lines connecting the points
#     for i in range(len(points) - 1):
#         p1 = APoint(points[i][0], points[i][1])
#         p2 = APoint(points[i + 1][0], points[i + 1][1])
#         acad.model.AddLine(p1, p2)
#
#     print(f"Done. {len(points) - 1} lines created.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AutoCAD Facade Generator")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--draw", action="store_true", help="Preview geometry in a window")
    group.add_argument("--send", action="store_true", help="Send geometry to AutoCAD")

    args = parser.parse_args()
    geometry = get_facade_points()

    if args.draw:
        plot_on_screen(geometry)
    elif args.send:
        send_to_autocad(geometry)