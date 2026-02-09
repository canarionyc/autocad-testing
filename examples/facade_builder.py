import argparse
import math
import cad_tools

# --- Constants ---
WIDTH = 20.0
X_INSET = 4 * math.sqrt(2)


def get_col_centers():
    return [0.5 * X_INSET, 0.5 * WIDTH, WIDTH - (0.5 * X_INSET)]


def get_window_rects():
    w_side = 1.0
    centers = get_col_centers()
    sill_heights = [2.5, 5.5, 8.5, 11.5]
    windows = []
    for x_c in centers:
        for y_s in sill_heights:
            rect = [(x_c - 0.5, y_s), (x_c + 0.5, y_s), (x_c + 0.5, y_s + 1.0), (x_c - 0.5, y_s + 1.0),
                    (x_c - 0.5, y_s)]
            windows.append(rect)
    return windows


def get_door_rects():
    centers = get_col_centers()
    doors = []
    for x_c in centers:
        rect = [(x_c - 0.5, 0.0), (x_c + 0.5, 0.0), (x_c + 0.5, 2.0), (x_c - 0.5, 2.0), (x_c - 0.5, 0.0)]
        doors.append(rect)
    return doors


def get_stair_windows():
    """
    Generates the two tall stairwell windows.
    Sill: 2.5, Head: 12.5 (Height = 10m)
    X positions: X_INSET + 1.5 and WIDTH - (X_INSET + 1.5)
    """
    w_side = 1.0
    y_sill = 2.5
    y_head = 12.5

    # Calculate X Centers
    x_left_stair = X_INSET + 1.5
    x_right_stair = WIDTH - (X_INSET + 1.5)

    stair_centers = [x_left_stair, x_right_stair]
    stair_windows = []

    for x_c in stair_centers:
        rect = [
            (x_c - 0.5, y_sill),  # Bottom Left
            (x_c + 0.5, y_sill),  # Bottom Right
            (x_c + 0.5, y_head),  # Top Right
            (x_c - 0.5, y_head),  # Top Left
            (x_c - 0.5, y_sill)  # Close
        ]
        stair_windows.append(rect)
    return stair_windows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Full Facade Generator")
    parser.add_argument("--draw", action="store_true")
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--clear", type=str)

    args = parser.parse_args()

    # Calculate All Geometry
    windows = get_window_rects()
    doors = get_door_rects()
    stair_glaz = get_stair_windows()

    if args.clear:
        cad_tools.clear_layer(args.clear)

    if args.draw:
        # Show all layers in the preview
        all_objs = windows + doors + stair_glaz
        cad_tools.plot_on_screen(all_objs, title="Full Facade Preview")

    if args.send:
        # Layer 1: Standard Windows
        # cad_tools.send_to_autocad(windows, layer_name="A-GLAZ")
        # Layer 2: Doors
        # cad_tools.send_to_autocad(doors, layer_name="A-DOOR")
        # Layer 3: Stairwell Windows
        cad_tools.send_to_autocad(stair_glaz, layer_name="A-STAIR-GLAZ")