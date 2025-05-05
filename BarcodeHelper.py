from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code39
from os import path
pathJoiner = path.join

def create_labels_rs_bar(barcodes_with_repetitions, name, direc):
    p = Path(pathJoiner(direc, f"{name}.pdf")).absolute()
    c = canvas.Canvas(pathJoiner(direc, f"{name}.pdf"), pagesize=A4)
    width, height = A4

    top_margin = 14 * mm  # 12 mm
    side_margin = 5 * mm
    vertical_pitch = 21 * mm
    horizontal_pitch = 40 * mm
    label_height = 21 * mm
    label_width = 38 * mm
    labels_across = 5
    labels_down = 13

    x = side_margin
    y = height - top_margin - label_height
    labels_per_page = labels_across * labels_down
    current_label = 0

    for item in barcodes_with_repetitions:
        barcode = str(item["id"])
        repetitions = item["qnty"]
        selling_price = item["sp"]

        for _ in range(repetitions):
            c.saveState()

            # Draw the barcode on the top line
            barcode_widget = code39.Standard39(
                barcode.strip(),
                barWidth=label_width * 0.9,
                barHeight=label_height * 0.5,
                humanReadable=True,
                checksum=False,
            )

            barcode_width = barcode_widget.width
            scale_x = label_width / barcode_width
            barcode_y_offset = 2 * mm  # Add some space above the barcode

            c.translate(
                x, y + label_height * 0.35 + barcode_y_offset
            )  # Adjust the position of the barcode
            c.scale(scale_x, 1)
            barcode_widget.drawOn(c, 0, 0)

            c.restoreState()
            c.saveState()

            # Draw the selling price on the second line
            c.setFont("Helvetica-Bold", 12)
            second_line_text = f"Rs. {selling_price}/-"
            second_line_width = c.stringWidth(second_line_text, "Helvetica-Bold", 12)
            text_y_offset = 3 * mm  # Add some space between the barcode and text

            second_line_x = x + (label_width - second_line_width) / 2
            second_line_y = y + label_height * 0.1 + text_y_offset
            c.drawString(second_line_x, second_line_y, second_line_text)
            c.restoreState()

            if (current_label + 1) % labels_per_page == 0:
                c.showPage()  # Start a new page
                x = side_margin
                y = height - top_margin - label_height
                current_label = 0  # Reset label count
            else:
                if (current_label + 1) % labels_across == 0:
                    x = side_margin
                    y -= vertical_pitch
                else:
                    x += horizontal_pitch

            current_label += 1

    c.save()

    return p


def create_label_reference_pdf(barcodes_with_repetitions: list[dict], name: str, direc) -> None:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

    # Define the PDF file path
    file_path = pathJoiner(direc, f"{name}.pdf")
    p = Path(file_path).absolute()
    
    # Define headers
    headers = ["S. No.", "Name", "Quantity", "Price"]
    
    # Prepare table data
    data = [
        [sno + 1, item["name"], item["qnty"], item["sp"]] for sno, item in enumerate(barcodes_with_repetitions)
    ]
    table_data = [headers] + data  # Include headers as the first row
    
    # Create a PDF document
    pdf = SimpleDocTemplate(file_path, pagesize=letter)
    
    # Create a table
    table = Table(table_data)
    
    # Apply styles to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid lines for the table
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Data font
    ])
    table.setStyle(style)
    
    # Add the table to the PDF document
    elements = [table]
    pdf.build(elements)

    return p




def generatePDFs(bmrp, direc = "Barcodes"):
    from json import loads, dumps
    with open(pathJoiner(direc, "batch_number.json"), "r+") as data:
        json_raw_data = data.read()
        json_data = loads(json_raw_data)
        current_batch = json_data.get('batch') + 1
        json_data['batch'] = current_batch
        data.seek(0)
        data.truncate()
        data.write(dumps(json_data))

    l1 = create_labels_rs_bar(bmrp, name=f"Batch_{current_batch}_Dress", direc = direc)
    l2 = create_label_reference_pdf(bmrp, name=f"Batch_{current_batch}_Reference", direc=direc)

    return {"batch" : current_batch, "paths" : [l1, l2]}