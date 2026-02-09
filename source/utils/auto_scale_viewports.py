import win32com.client


def set_viewport_scale():
    acad = win32com.client.Dispatch("AutoCAD.Application")
    doc = acad.ActiveDocument

    # 1. Ensure we are in Paper Space
    doc.ActiveSpace = 0  # 0 = acPaperSpace, 1 = acModelSpace

    print(f"Scanning Layout: {doc.ActiveLayout.Name}...")

    paper_space = doc.PaperSpace
    count = 0

    # 2. Iterate through Paper Space objects
    for obj in paper_space:
        # Check if object is a Viewport
        if "AcDbViewport" in obj.ObjectName:
            # We skip the 'Active Viewport' which is sometimes the Paper itself (ID 1)
            # Viewport ID 1 is the actual "Sheet" definition, we want ID > 1
            # Note: In COM, we catch errors or check properties carefully
            try:
                # Turn it on (sometimes they are off)
                obj.Display(True)

                # Set Scale to 1:50
                # Formula: 1 / 50 = 0.02
                obj.CustomScale = 1 / 50

                # Optional: Lock the Display so you don't mess it up
                obj.DisplayLocked = True

                count += 1
                print(f"Viewport updated to 1:50 and Locked.")
            except Exception as e:
                print(f"Skipped a viewport: {e}")

    if count == 0:
        print("No viewports found! (Did you draw the rectangle with the MVIEW command?)")
    else:
        doc.Regen(1)  # Refresh screen


if __name__ == "__main__":
    set_viewport_scale()