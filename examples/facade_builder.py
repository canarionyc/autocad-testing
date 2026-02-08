# facade_builder.py
import argparse
import math


import argparse
import math
import cad_tools  # Your custom library

# --- Constants ---
WIDTH = 20.0
HEIGHT_EAVES = 15.0
X_INSET = 4 * math.sqrt(2)  # approx 5.657


def get_col_centers():
    """Returns the X-coordinates for the 3 columns."""
    return [
        0.5 * X_INSET,  # Left Gable
        0.5 * WIDTH,  # Center
        WIDTH - (0.5 * X_INSET)  # Right Gable
    ]


def get_window_rects():
    """Generates 3 columns of 4 windows (Sills: 2.5, 5.5, 8.5, 11.5)."""
    w_side = 1.0
    centers = get_col_centers()
    sill_heights = [2.5, 5.5, 8.5, 11.5]

    windows = []
    for x_c in centers:
        for y_s in sill_heights:
            rect = [
                (x_c - 0.5, y_s),
                (x_c + 0.5, y_s),
                (x_c + 0.5, y_s + 1.0),
                (x_c - 0.5, y_s + 1.0),
                (x_c - 0.5, y_s)
            ]
            windows.append(rect)
    return windows


def get_door_rects():
    """Generates 3 doors at the base of the columns (0 to 2.0m)."""
    w_side = 1.0
    h_door = 2.0
    centers = get_col_centers()

    doors = []
    for x_c in centers:
        # Door goes from Y=0 to Y=2
        rect = [
            (x_c - 0.5, 0.0),  # Bottom Left
            (x_c + 0.5, 0.0),  # Bottom Right
            (x_c + 0.5, h_door),  # Top Right
            (x_c - 0.5, h_door),  # Top Left
            (x_c - 0.5, 0.0)  # Close Loop
        ]
        doors.append(rect)
    return doors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Facade Generator")
    # We now use standard optional arguments instead of a mutually exclusive group
    # so you can do multiple things at once (e.g. clear AND send)
    parser.add_argument("--draw", action="store_true", help="Preview geometry in window")
    parser.add_argument("--send", action="store_true", help="Send geometry to AutoCAD")
    parser.add_argument("--clear", type=str, help="Clear a specific layer name")

    args = parser.parse_args()

    # 1. Calculate All Geometry
    windows = get_window_rects()
    doors = get_door_rects()

    # 2. Handle "Clear" Command
    if args.clear:
        cad_tools.clear_layer(args.clear)

    # 3. Handle "Draw" (Preview)
    if args.draw:
        # Combine lists just for the plot
        all_shapes = windows + doors
        cad_tools.plot_on_screen(all_shapes, title="Facade Layout: Windows + Doors")

    # 4. Handle "Send" (AutoCAD)
    if args.send:
        # Send Windows to A-GLAZ
        print("--- Processing Windows ---")
        # cad_tools.send_to_autocad(windows, layer_name="A-GLAZ")

        # Send Doors to A-DOOR
        print("--- Processing Doors ---")
        cad_tools.send_to_autocad(doors, layer_name="A-DOOR")