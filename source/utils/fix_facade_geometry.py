import win32com.client
import pythoncom
import time


def fix_facade_geometry_v2():
    print("--- STARTING GEOMETRY FIX ---")

    try:
        # 1. Connect
        acad = win32com.client.Dispatch("AutoCAD.Application")
        doc = acad.ActiveDocument
        msp = doc.ModelSpace
        print(f"Connected to Drawing: {doc.Name}")

        # 2. RUN JOIN (The "Heavy Lifting")
        # We perform this first to merge touching lines
        print("\n[Step 1] Running AutoCAD JOIN command...")
        doc.SendCommand("_SELALL _JOIN \n")

        # Vital: Wait for AutoCAD to actually finish the command
        time.sleep(2)
        print("-> Join command sent. Waiting for processing...")

        # 3. ITERATE & FIX (The "Fine Tuning")
        print("\n[Step 2] Inspecting Polylines...")

        fixed_count = 0
        already_closed = 0
        ignored_count = 0

        # We iterate backwards or use a list to be safe, though not strictly necessary for property edits
        # Using a count loop is sometimes safer with COM collections
        total_objects = msp.Count

        for i in range(total_objects):
            try:
                obj = msp.Item(i)
                obj_name = obj.ObjectName

                # We only care about Polylines (LWPolyline is the standard 2D one)
                if "AcDbPolyline" in obj_name:

                    # --- THE FIX: Force Interface Cast ---
                    # This tells COM: "I know this is an Entity, but treat it as a Polyline"
                    # We try to cast it to a Lightweight Polyline interface
                    try:
                        # Attempt to treat as LWPolyline to access 'Closed'
                        # Note: In some pythoncom versions, simple access works,
                        # but if it fails, we might need to rely on late-binding or CastTo.

                        # Check if it is closed
                        # Logic: If Open (False), make it Closed (True)
                        if obj.Closed == False:
                            obj.Closed = True
                            fixed_count += 1
                            # Optional: Print area to confirm it worked
                            print(f"   -> Fixed Polyline Handle {obj.Handle}. New Area: {obj.Area:.2f}")
                        else:
                            already_closed += 1

                    except AttributeError:
                        # If we get here, it means 'obj' is wrapped as a generic IAcadEntity
                        # We can try to rely on dynamic dispatch to force the property read
                        # Or just pass if it's a 3D polyline or something else
                        print(f"   -> Warning: Could not read 'Closed' on {obj_name} (Handle: {obj.Handle})")

                else:
                    ignored_count += 1

            except Exception as inner_e:
                print(f"   -> Error processing object index {i}: {inner_e}")

        # 4. SUMMARY
        print("\n" + "=" * 30)
        print("GEOMETRY FIX REPORT")
        print("=" * 30)
        print(f"Total Objects Scanned: {total_objects}")
        print(f"Polylines Fixed (Closed): {fixed_count}")
        print(f"Polylines Already OK:     {already_closed}")
        print(f"Other Objects Ignored:    {ignored_count}")
        print("=" * 30)
        print("Please SAVE your drawing.")

    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")


if __name__ == "__main__":
    fix_facade_geometry_v2()