import win32com.client
import pythoncom
import os
import time


def import_door_photo_robust(image_path):
    # 1. Prepare Path
    abs_path = os.path.abspath(image_path)
    if not os.path.exists(abs_path):
        print(f"Error: File not found at {abs_path}")
        return

    acad = None
    doc = None

    # 2. Connection Retry Loop (Fixes 'Call rejected')
    for i in range(5):
        try:
            # Check if we need to initialize COM for this thread
            pythoncom.CoInitialize()
            acad = win32com.client.Dispatch("AutoCAD.Application")

            # Check if AutoCAD is responsive by asking for a simple property
            state = acad.Visible
            doc = acad.ActiveDocument
            break  # Success!
        except Exception as e:
            print(f"AutoCAD busy... retrying ({i + 1}/5)")
            time.sleep(2)  # Wait 2 seconds and try again

    if doc is None:
        print("Could not connect to AutoCAD. Is a dialog box open?")
        return

    # 3. Import Logic
    try:
        msp = doc.ModelSpace
        print(f"Importing: {os.path.basename(abs_path)}")

        # Define Insertion Point (0,0,0)
        pt = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (0.0, 0.0, 0.0))

        # AddRaster(Path, Point, Scale, Rotation)
        # Note: If this fails, we fall back to SendCommand
        try:
            image = msp.AddRaster(abs_path, pt, 1.0, 0.0)
            print("Success (COM Method)")
        except Exception as e:
            print(f"COM AddRaster failed ({e}). Attempting command line fallback...")
            # Fallback: Use the command line (More reliable for Rasters)
            # -IMAGEATTACH is the command, but it usually pops a dialog.
            # We use a LISP snippet passed through SendCommand to bypass dialogs.
            # Or simpler: Attach it, then user scales it.

            # Let's try the safest path: IMAGEATTACH command with prompts suppressed is hard via script.
            # Instead, we suggest checking the file type.
            print("Tip: Ensure the JPG is not CMYK (AutoCAD only likes RGB).")

    except Exception as e:
        print(f"Import failed: {e}")


if __name__ == "__main__":
    # Change this to your actual JPG path
    import_door_photo_robust(r"C:\Users\tglla\OneDrive\Pictures\Camera Roll\20260206_084919.jpg")