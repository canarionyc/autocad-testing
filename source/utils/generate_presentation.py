import win32com.client
from fpdf import FPDF
import os
from datetime import datetime

# --- CONFIGURATION ---
OUTPUT_DIR = r"C:\CAD_Exports"
DWG_PDF_NAME = "Facade_Design_Plot.pdf"
REPORT_PDF_NAME = "Facade_Report.pdf"
FINAL_PACKAGE = "Facade_Final_Package.pdf"

AUTHOR_NAME = os.getenv("AUTHOR_NAME", "Tomas Gonzalez")
AUTHOR_EMAIL = os.getenv("AUTHOR_EMAIL", "alu0101841946@ull.edu.es")


def add_title_block(doc):
    """Adds title text to the Active Layout (Paper Space) without modifying Model Space."""
    print("Adding Title Block info...")
    try:
        paper_space = doc.PaperSpace
        # Coordinates (X, Y, Z) - Adjust 10,10 to fit your specific Title Block margin
        pt = win32com.client.VARIANT(win32com.client.pythoncom.VT_ARRAY | win32com.client.pythoncom.VT_R8,
                                     (10.0, 10.0, 0.0))

        text_content = f"Designed by: {AUTHOR_NAME} | {AUTHOR_EMAIL} | {datetime.now().strftime('%Y-%m-%d')}"
        text_obj = paper_space.AddText(text_content, pt, 2.5)

        # User requested lowercase attribute
        text_obj.color = 7

    except Exception as e:
        print(f"Title block note: {e}")


def merge_pdfs_acrobat(pdf_list, output_path):
    """Merges PDFs using Adobe Acrobat Pro."""
    try:
        acro_app = win32com.client.Dispatch("AcroExch.App")
        pd_doc_main = win32com.client.Dispatch("AcroExch.PDDoc")

        if not pd_doc_main.Open(pdf_list[0]):
            print(f"Error opening {pdf_list[0]}")
            return

        for i in range(1, len(pdf_list)):
            pd_doc_temp = win32com.client.Dispatch("AcroExch.PDDoc")
            if pd_doc_temp.Open(pdf_list[i]):
                pd_doc_main.InsertPages(pd_doc_main.GetNumPages() - 1, pd_doc_temp, 0, pd_doc_temp.GetNumPages(), 1)
                pd_doc_temp.Close()

        pd_doc_main.Save(1, output_path)
        pd_doc_main.Close()
        acro_app.Exit()
        print(f"Package saved: {output_path}")
    except Exception as e:
        print(f"Acrobat Error: {e}")


def generate_report():
    acad = win32com.client.Dispatch("AutoCAD.Application")
    doc = acad.ActiveDocument

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. GATHER DATA (Read Only)
    print("Scanning Geometry...")
    layer_stats = {}

    for obj in doc.ModelSpace:
        l_name = obj.Layer
        raw_type = obj.ObjectName.replace("AcDb", "")

        # Refine type description (e.g. Check if Polyline is Closed)
        obj_desc = raw_type
        if "Polyline" in raw_type:
            # Check closed status safely
            try:
                if obj.Closed:
                    obj_desc = "Polyline (Closed)"
                else:
                    obj_desc = "Polyline (Open)"
            except:
                pass

        if l_name not in layer_stats:
            layer_stats[l_name] = {'count': 0, 'area': 0.0, 'types': {}}

        # Increment
        layer_stats[l_name]['count'] += 1

        # Track Type Breakdown
        if obj_desc in layer_stats[l_name]['types']:
            layer_stats[l_name]['types'][obj_desc] += 1
        else:
            layer_stats[l_name]['types'][obj_desc] = 1

        # Sum Area
        try:
            layer_stats[l_name]['area'] += obj.Area
        except:
            pass

    # 2. PLOT DRAWING
    add_title_block(doc)
    dwg_pdf_path = os.path.join(OUTPUT_DIR, DWG_PDF_NAME)
    doc.ActiveLayout.ConfigName = "DWG To PDF.pc3"
    doc.Plot.PlotToFile(dwg_pdf_path)

    # 3. GENERATE REPORT (Updated for fpdf2)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", style='B', size=14)
    # Deprecation fix: use 'text=' instead of 'txt='
    pdf.cell(w=0, h=10, text=f"Design Report: {doc.Name}", new_x="LMARGIN", new_y="NEXT", align='C')

    pdf.set_font("Helvetica", size=10)
    pdf.cell(w=0, h=8, text=f"Author: {AUTHOR_NAME}", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)

    # Header
    pdf.set_font("Courier", style='B', size=10)
    header = f"{'Layer':<20} | {'Count':<6} | {'Area (m2)':<10} | {'Composition'}"
    pdf.cell(w=0, h=8, text=header, new_x="LMARGIN", new_y="NEXT")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    # Rows
    pdf.set_font("Courier", size=10)
    for layer, data in layer_stats.items():
        # Composition string
        comp_str = ", ".join([f"{k}:{v}" for k, v in data['types'].items()])

        # Convert area to m2 if drawing is in mm (divide by 1,000,000)
        # Adjust logic if your drawing is already in meters
        area_m2 = data['area'] / 1000000

        row = f"{layer:<20} | {data['count']:<6} | {area_m2:<10.2f} | {comp_str}"
        pdf.cell(w=0, h=8, text=row, new_x="LMARGIN", new_y="NEXT")

    report_pdf_path = os.path.join(OUTPUT_DIR, REPORT_PDF_NAME)
    pdf.output(report_pdf_path)

    # 4. MERGE
    final_path = os.path.join(OUTPUT_DIR, FINAL_PACKAGE)
    merge_pdfs_acrobat([dwg_pdf_path, report_pdf_path], final_path)


if __name__ == "__main__":
    generate_report()