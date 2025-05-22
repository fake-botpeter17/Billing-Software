"""
Printer Controller - Handles printing operations
"""
import os
import logging
import subprocess
from datetime import date
from typing import Dict
from pathlib import Path
from config.constants import BILLS_DIR, COMPANY_NAME

class PrinterController:
    """Controller for printing operations"""
    def __init__(self):
        self.bills_dir = BILLS_DIR
        os.makedirs(self.bills_dir, exist_ok=True)

    def print_bill(self, bill_data: Dict) -> bool:
        """
        Print bill with given data
        
        Args:
            bill_data: Dictionary containing bill information
            
        Returns:
            bool: True if printing successful, False otherwise
        """
        try:
            # Generate bill content
            content = self._generate_bill_content(bill_data)
            
            # Save bill to PDF
            bill_path = self._save_bill_pdf(content, bill_data['bill_no'])
            
            # Print the PDF
            self._send_to_printer(bill_path)
            
            logging.info(f"Bill {bill_data['bill_no']} printed successfully")
            return True

        except Exception as e:
            logging.error(f"Error printing bill: {e}", exc_info=True)
            return False

    def _generate_bill_content(self, bill_data: Dict) -> str:
        """Generate bill content in HTML format"""
        items_html = self._generate_items_table(bill_data['items'])
        
        return f"""
        <html>
        <body>
            <h1>{COMPANY_NAME}</h1>
            <p>Bill No: {bill_data['bill_no']}</p>
            <p>Date: {date.today().strftime("%d.%m.%Y")}</p>
            <p>Time: {bill_data['date']}</p>
            <p>Cashier: {bill_data['cashier']}</p>
            
            <table>
                <tr>
                    <th>Item</th>
                    <th>Qty</th>
                    <th>Price</th>
                    <th>Disc</th>
                    <th>Total</th>
                </tr>
                {items_html}
            </table>
            
            <p>Total: {bill_data['total']:.2f}</p>
            <p>Discount: {bill_data['discount']:.2f}</p>
            <p>Net Total: {bill_data['net_total']:.2f}</p>
        </body>
        </html>
        """

    def _generate_items_table(self, items: Dict) -> str:
        """Generate HTML table for bill items"""
        rows = []
        for item_id, details in items.items():
            rows.append(f"""
                <tr>
                    <td>{item_id}</td>
                    <td>{details['quantity']}</td>
                    <td>{details['price']:.2f}</td>
                    <td>{details['discount']:.2f}</td>
                    <td>{details['total']:.2f}</td>
                </tr>
            """)
        return "\n".join(rows)

    def _save_bill_pdf(self, content: str, bill_no: int) -> Path:
        """Save bill content as PDF"""
        bill_path = self.bills_dir / f"{bill_no}.pdf"
        
        # Use wkhtmltopdf or similar to convert HTML to PDF
        # This is a placeholder - implement actual PDF generation
        with open(bill_path, 'w') as f:
            f.write(content)
            
        return bill_path

    def _send_to_printer(self, bill_path: Path) -> None:
        """Send PDF to printer"""
        if os.name == 'nt':  # Windows
            os.startfile(str(bill_path), 'print')
        else:  # Linux/Unix
            subprocess.run(['lp', '-o', 'media=Custom.216x1000', 
                          '-o', 'page-left=0', '-o', 'page-right=0',
                          '-o', 'page-top=0', '-o', 'page-bottom=0',
                          str(bill_path)])
