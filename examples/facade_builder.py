# facade_builder.py
import argparse
import math
# Import your new module
import source.utils.cad_tools as cad_tools

# --- Constants ---
WIDTH = 20.0
HEIGHT_EAVES = 15.0
X_INSET = 4 * math.sqrt(2)  # approx 5.657


def get_window_rects():
    """
    Generates window coordinates based on updated sill heights:
    Sills: 2.5, 5.5, 8.5, 11.5
    Window Size: 1.0 x 1.0
    """
    w_side = 1.0

    # 1. Define Centers (Horizontal)
    # Left Gable Center, Main Center, Right Gable Center
    col_centers = [
        0.5 * X_INSET,
        0.5 * WIDTH,
        WIDTH - (0.5 * X_INSET)
    ]

    # 2. Define Sill Heights (Vertical)
    # Updated values as per your request
    sill_heights = [2.5, 5.5, 8.5, 11.5]

    windows = []

    # 3. Generate Rectangles
    for x_c in col_centers:
        for y_sill in sill_heights:
            # Calculate geometric bounds
            x_left = x_c - (w_side / 2)
            x_right = x_c + (w_side / 2)
            y_btm = y_sill
            y_top = y_sill + w_side

            # Create closed loop (5 points)
            rect = [
                (x_left, y_btm),
                (x_right, y_btm),
                (x_right, y_top),
                (x_left, y_top),
                (x_left, y_btm)
            ]
            windows.append(rect)

    return windows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Facade Window Generator")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--draw", action="store_true", help="Preview in Matplotlib")
    group.add_argument("--send", action="store_true", help="Send to AutoCAD")
    group.add_argument("--clear", type=str, help="Delete all objects on this LAYER name")  # New flag!

    args = parser.parse_args()

    # 1. Clear Layer Command
    if args.clear:
        cad_tools.clear_layer(args.clear)

    # 2. Draw/Send Commands
    elif args.draw:
        window_geometry = get_window_rects()
        cad_tools.plot_on_screen(window_geometry)

    elif args.send:
        # Optional: Auto-clear before sending?
        # For safety, let's just send. You can run --clear manually if you want.
        window_geometry = get_window_rects()
        cad_tools.send_to_autocad(window_geometry, layer_name="A-GLAZ")