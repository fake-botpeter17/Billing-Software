from escpos.printer import Usb
from datetime import datetime

# Connect to printer
p = Usb(0x154F, 0x154F, interface=1)  # Adjust if needed

# Header
p.set(align='center', bold=True, width=2, height=2)
p.text("Fashion Paradise\n")
p.set(align='center', bold=False, width=1, height=1)
p.text("No. 1, Richwood Avenue, Market Road,\nThaiyur - 603 103.\n\n")

# Bill Info
p.set(align='left')
bill_no = "10023"
bill_date = "02.08.2025"
bill_time = "18:55:46"
billed_by = "Nelson"
p.text(f"Bill No: {bill_no}\n")
p.text(f"Bill Date: {bill_date}    Bill Time: {bill_time}\n")
p.text(f"Billed By: {billed_by}\n\n")

# Item Table Header
p.text("S.No. Name            Rate Qnty Amount\n")
p.text("----------------------------------------\n")

# Items
items = [
    ("1", "Kids Dress", 425.0, 1, 425.0),
    ("2", "Chudi Set", 849.0, 1, 849.0),
    ("3", "Chudi Set", 575.0, 1, 575.0),
    ("4", "Lining Cloth", 40.0, 1, 40.0),
    ("5", "Handkercheif", 20.0, 2, 40.0),
    ("6", "Lining 1.5 meters", 60.0, 1, 60.0)
]

for sno, name, rate, qty, amt in items:
    p.text(f"{sno:<4}{name:<17}{rate:<6}{qty:<5}{amt:<7}\n")

# Totals
p.text("----------------------------------------\n")
p.text("Total        : Rs. 1989.00\n")
p.text("Discount     : Rs. 109.43\n")
p.text("Net Total    : Rs. 1879.57/-\n\n")

# Footer
p.set(align='center')
p.text("Thank you! Visit Again!\n")
p.cut()
