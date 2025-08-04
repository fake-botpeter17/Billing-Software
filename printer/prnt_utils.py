from escpos.printer import Usb
from datetime import datetime
from PIL import Image


class ReceiptPrinter:
    def __init__(self, vendor_id, product_id, interface=0):
        try:
            self.printer = Usb(vendor_id, product_id, interface=interface)
        except Exception as e:
            raise RuntimeError(f"Printer connection failed: {e}")

    def print_receipt(
        self,
        store_name,
        address_lines,
        bill_no,
        billed_by,
        items,
        total,
        discount,
        net_total,
        bill_date=None,
        bill_time=None
    ):
        # Defaults to now if not provided
        now = datetime.now()
        bill_date = bill_date or now.strftime("%d.%m.%Y")
        bill_time = bill_time or now.strftime("%H:%M:%S")

        self.printer.set(align='center')
        self.printer.image(Image.open("Resources/bw_logo.png").resize((220, 200)))

        # HEADER
        # self.printer.set(align='center', bold=True, width=2, height=3)
        # self.printer.text(f"{store_name}\n")
        self.printer.set(align='center', bold=False, width=1, height=1)
        for line in address_lines:
            self.printer.text(f"{line}\n")
        self.printer.text("\n")

        # BILL INFO
        self.printer.set(align='left')
        self.printer.text(f"Bill No: {bill_no}\t\t     Billed By: {billed_by}\n")
        self.printer.text(f"Bill Date: {bill_date}        Bill Time: {bill_time}\n\n")

        # TABLE HEADER
        self.printer.text("S.No.      Name        Rate\t Qnty\t Amount\n")
        self.printer.text("------------------------------------------------\n")

        for i, item in enumerate(items, 1):
            name = item['name'][:14]
            rate = f"{item['rate']:.2f}"
            qty = str(item['qty'])
            amt = f"{item['amount']:.2f}"
            self.printer.text(f"{i:^4}   {name:<16}{round(float(rate),2):<6}     {qty:<5} {round(float(amt),2):<7}\n")

        self.printer.text("------------------------------------------------\n")
        self.printer.set('left')
        self.printer.text(f"Total        : Rs. {total:.2f}\n")
        self.printer.text(f"Discount     : Rs. {discount:.2f}\n")
        self.printer.set('left', bold=True)
        self.printer.text(f"Net Total    : Rs. {net_total:.2f}/-\n\n")
        # # FOOTER
        self.printer.set(align='center')
        self.printer.text("Thank you! Visit Again!\n")
        self.printer.cut()

    def test_print(self):
        self.printer.text("Printer connection test passed.\n")
        self.printer.cut()


if __name__ == "__main__":
    items = [
        {"name": "Kids Dress", "rate": 425.0, "qty": 1, "amount": 425.0},
        {"name": "Chudi Set", "rate": 849.0, "qty": 1, "amount": 849.0},
        {"name": "Chudi Set", "rate": 575.0, "qty": 1, "amount": 575.0},
        {"name": "Lining Cloth", "rate": 40.0, "qty": 1, "amount": 40.0},
        {"name": "Handkercheif", "rate": 20.0, "qty": 2, "amount": 40.0},
        {"name": "Lining 1.5 meters", "rate": 60.0, "qty": 1, "amount": 60.0}
    ]

    printer = ReceiptPrinter(0x154F, 0x154F, interface=1)
    printer.print_receipt(
        store_name="Fashion Paradise",
        address_lines=[
            "No. 1, Richwood Avenue, Market Road,",
            "Thaiyur - 603 103."
        ],
        bill_no="10023",
        billed_by="Nelson",
        items=items,
        total=1989.00,
        discount=109.43,
        net_total=1879.57
    )
