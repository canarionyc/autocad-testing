import win32com.client
from fpdf import FPDF
import os
from datetime import datetime

# --- SETTINGS ---
DWG_PDF_NAME = "Facade_Design_Plot.pdf"
REPORT_PDF_NAME = "Facade_Design_Report.pdf"
OUTPUT_DIR = r"C:\Users\tglla\OneDrive\Desktop\ACAD_Exports"  # Change this to your preferred folder


def generate_presentation():
    # 1. Connect to AutoCAD
    try:
        acad = win32com.client.Dispatch("AutoCAD.Application")
        doc = acad.ActiveDocument
        print(f"Processing: {doc.Name}")
    except Exception as e:
        print("Could not connect to AutoCAD. Is it open?")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # --- PART 1: GATHER STATISTICS ---
    print("Analyzing geometry...")
    layer_stats = {}  # Format: {'LayerName': {'count': 0, 'area': 0.0}}

    model_space = doc.ModelSpace

    for obj in model_space:
        l_name = obj.Layer

        if l_name not in layer_stats:
            layer_stats[l_name] = {'count': 0, 'area': 0.0}

        # Increment Count
        layer_stats[l_name]['count'] += 1

        # Attempt to get Area (Not all objects have Area, e.g., Lines/Text)
        try:
            # We check if the object has an 'Area' property
            area = obj.Area
            layer_stats[l_name]['area'] += area
        except:
            # Object has no area (like a Text object or Line), skip area add
            pass

    # --- PART 2: PLOT THE DRAWING TO PDF ---
    print("Plotting drawing to PDF...")

    # We target the Active Layout (usually Paper Space for presentation)
    layout = doc.ActiveLayout

    # Force the plotter config to built-in PDF driver to ensure it works
    try:
        layout.ConfigName = "DWG To PDF.pc3"
        layout.StandardScale = 0  # 0 = acScaleToFit, or set specific scale
    except Exception as e:
        print(f"Warning: Could not set plotter config. Using current defaults. {e}")

    # PlotToFile requires the full path
    dwg_pdf_full_path = os.path.join(OUTPUT_DIR, DWG_PDF_NAME)

    # The plot method logic usually requires the Plot object
    plot = doc.Plot
    plot.PlotToFile(dwg_pdf_full_path)
    print(f"Drawing saved to: {dwg_pdf_full_path}")

    # --- PART 3: GENERATE PDF REPORT ---
    print("Generating Summary Report...")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"Design Summary: {doc.Name}", ln=1, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=1, align='C')
    pdf.ln(10)

    # Table Header
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(80, 10, "Layer Name", 1)
    pdf.cell(40, 10, "Object Count", 1)
    pdf.cell(60, 10, "Total Area (Units²)", 1)
    pdf.ln()

    # Table Rows
    pdf.set_font("Arial", size=12)
    for layer, data in layer_stats.items():
        pdf.cell(80, 10, layer, 1)
        pdf.cell(40, 10, str(data['count']), 1)
        # Format area to 2 decimal places
        pdf.cell(60, 10, f"{data['area']:.2f}", 1)
        pdf.ln()

    report_full_path = os.path.join(OUTPUT_DIR, REPORT_PDF_NAME)
    pdf.output(report_full_path)
    print(f"Report saved to: {report_full_path}")


if __name__ == "__main__":
    generate_presentation()