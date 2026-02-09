import win32com.client
import pythoncom


def cleanup_drawing():
    try:
        # 1. Connect to AutoCAD
        acad = win32com.client.Dispatch("AutoCAD.Application")
        doc = acad.ActiveDocument
        msp = doc.ModelSpace
        print(f"Connected to: {doc.Name}")

        # 2. Ensure "AUDIT_REQUIRED" layer exists
        # We try to add it; if it exists, AutoCAD just returns the existing layer.
        try:
            audit_layer = doc.Layers.Add("AUDIT_REQUIRED")
            audit_layer.color = 30  # Orange color for visibility
        except Exception as e:
            print(f"Layer check note: {e}")

        # Counters for the report
        moved_count = 0
        hidden_pdfs = 0

        # 3. Iterate through Model Space
        # We count backwards or use a list to avoid indexing errors if we were deleting,
        # but for modifying properties, a standard loop is usually fine in COM.
        for obj in msp:

            # --- CHECK 1: Layer 0 ---
            if obj.Layer == "0":
                # Check if it is not a viewport or something critical (optional)
                obj.Layer = "AUDIT_REQUIRED"
                moved_count += 1

            # --- CHECK 2: Hide PDFs ---
            # ObjectName is the reliable COM property for type checking
            # "AcDbPdfReference" is the internal name for a PDF underlay
            if "AcDbPdfReference" in obj.ObjectName:
                obj.Visible = False
                hidden_pdfs += 1

        # 4. Refresh to see changes
        doc.Regen(1)

        print("-" * 30)
        print("CLEANUP REPORT")
        print(f"Objects moved from Layer 0: {moved_count}")
        print(f"PDFs hidden: {hidden_pdfs}")
        print("-" * 30)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    cleanup_drawing()