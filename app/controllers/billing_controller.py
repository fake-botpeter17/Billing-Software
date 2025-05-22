"""
Billing Controller - Handles billing operations and UI interactions
"""
import logging
from typing import Dict, Optional
from PyQt6.QtWidgets import QMainWindow
from app.models.bill import Bill
from app.models.user import User
from app.views.home_gui import HomeGUI
from app.utils.worker_factory import WorkerFactory

class BillingController:
    """Controller for billing operations"""
    def __init__(self):
        self.bill_model = Bill()
        self.user_model = User()
        self.view = None
        self.worker_factory = WorkerFactory()

    def start(self) -> None:
        """Start the billing system"""
        self.view = HomeGUI(self)
        self.view.show()

    def handle_cell_change(self, row: int, col: int) -> None:
        """Handle changes in bill table cells"""
        try:
            item_id = self.view.get_text(row, col)
            if not item_id:
                return

            item = self.bill_model.get_item(int(item_id))
            if not item:
                self.view.show_error("Invalid Item", "Item not found")
                return

            if self.bill_model.contains(item_id):
                self._handle_duplicate_item(item_id)
            else:
                self._add_new_item(item_id, row)

        except ValueError as e:
            logging.error(f"Error handling cell change: {e}")
            self.view.show_error("Input Error", "Invalid input value")

    def _handle_duplicate_item(self, item_id: int) -> None:
        """Handle duplicate item entry"""
        row = self.bill_model.get_row_number(item_id)
        current_qty = self.view.get_quantity(row)
        self.view.update_quantity(row, current_qty + 1)
        self._update_totals()

    def _add_new_item(self, item_id: int, row: int) -> None:
        """Add new item to bill"""
        item = self.bill_model.get_item(item_id)
        self.bill_model.add_item(item_id, row)
        self.view.set_row_data(row, item)
        self._update_totals()

    def _update_totals(self) -> None:
        """Update bill totals"""
        total = 0
        discount = 0
        for item_id in self.bill_model.get_cart_items():
            row = self.bill_model.get_row_number(item_id)
            item_total = self.view.get_row_total(row)
            item_discount = self.view.get_row_discount(row)
            total += item_total
            discount += item_discount

        self.view.update_totals(total, discount)

    def generate_bill(self) -> Optional[Dict]:
        """Generate final bill"""
        if self.bill_model.is_empty():
            self.view.show_error("Error", "No items in bill")
            return None

        bill_data = {
            'bill_no': self.bill_model.get_bill_no(),
            'items': self._get_bill_items(),
            'total': self.view.get_total(),
            'discount': self.view.get_discount(),
            'net_total': self.view.get_net_total(),
            'date': self.bill_model.get_time(),
            'cashier': self.user_model.get_name_designation()[0]
        }

        # Create worker for bill generation
        worker = self.worker_factory.create_worker("bill_generation")
        worker.billGenerated.connect(self._on_bill_generated)
        worker.error.connect(self._on_bill_error)
        worker.start()

        return bill_data

    def _get_bill_items(self) -> Dict:
        """Get all items in current bill"""
        items = {}
        for item_id in self.bill_model.get_cart_items():
            row = self.bill_model.get_row_number(item_id)
            items[item_id] = {
                'quantity': self.view.get_quantity(row),
                'price': self.view.get_price(row),
                'discount': self.view.get_row_discount(row),
                'total': self.view.get_row_total(row)
            }
        return items

    def _on_bill_generated(self, response: Dict) -> None:
        """Handle successful bill generation"""
        self.bill_model.next_bill_prep()
        self.view.clear_bill()
        self.view.show_success("Success", "Bill generated successfully")

    def _on_bill_error(self, error: str) -> None:
        """Handle bill generation error"""
        self.view.show_error("Error", f"Failed to generate bill: {error}")
