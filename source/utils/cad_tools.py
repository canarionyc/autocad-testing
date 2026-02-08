# cad_tools.py
import matplotlib.pyplot as plt
from pyautocad import Autocad, APoint


def plot_on_screen(polygons, title="Geometry Preview"):
    """
    Visualizes a list of closed polygons using Matplotlib.
    Expects polygons as lists of (x,y) tuples.
    """
    print(f"Plotting {len(polygons)} shapes...")

    plt.figure(figsize=(10, 8))

    for i, poly in enumerate(polygons):
        # Unzip x and y coordinates
        x_vals, y_vals = zip(*poly)

        # Plot outline
        plt.plot(x_vals, y_vals, 'b-', linewidth=1.5)

        # Optional: Fill with light blue to indicate 'solid' object
        plt.fill(x_vals, y_vals, 'cyan', alpha=0.3)

        # Label the first one to check orientation if needed
        if i == 0:
            plt.text(x_vals[0], y_vals[0], "Start", fontsize=8, color='red')

    plt.title(title)
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.axis('equal')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()


def clear_layer(layer_name):
    """
    Deletes ALL objects on a specific layer in ModelSpace.
    """
    try:
        acad = Autocad(create_if_not_exists=True)
        print(f"Connected to: {acad.doc.Name}")
    except:
        print("Error: Could not connect to AutoCAD.")
        return

    print(f"Searching for objects on layer '{layer_name}'...")

    # Counter for deleted objects
    count = 0

    # Iterate through ModelSpace (where you draw)
    # Note: We iterate backwards or collect first to avoid issues while deleting
    objects_to_delete = []

    for obj in acad.model:
        try:
            if obj.Layer.upper() == layer_name.upper():
                objects_to_delete.append(obj)
        except:
            # Some objects might not have a Layer property (rare)
            continue

    # Delete them
    for obj in objects_to_delete:
        try:
            obj.Delete()
            count += 1
        except:
            pass

    print(f"Deleted {count} objects from layer '{layer_name}'.")

def send_to_autocad(polygons, layer_name="0"):
    """
    Sends a list of polygons to the active AutoCAD document on a specific layer.
    """
    try:
        acad = Autocad(create_if_not_exists=True)
        print(f"Connected to: {acad.doc.Name}")
    except Exception as e:
        print("Error: Could not connect to AutoCAD. Is it running?")
        return

    print(f"Sending {len(polygons)} objects to layer '{layer_name}'...")

    for poly in polygons:
        # Draw the loop of lines for this polygon
        for i in range(len(poly) - 1):
            p1 = APoint(poly[i][0], poly[i][1])
            p2 = APoint(poly[i + 1][0], poly[i + 1][1])

            line = acad.model.AddLine(p1, p2)

            # Set Layer
            try:
                line.Layer = layer_name
            except:
                # If layer doesn't exist, it defaults to current (usually 0)
                pass

    print("Transfer complete.")