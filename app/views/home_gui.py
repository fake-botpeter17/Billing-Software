"""
Home GUI - Main window of the billing system
"""
import logging
from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QTableWidget, QLabel,
    QPushButton, QMenu
)
from PyQt6.QtCore import Qt
from PyQt6 import uic
from PyQt6.QtGui import QIcon
from app.models.user import User
from config.constants import WindowName, BillTableColumn

class HomeGUI(QMainWindow):
    """Main window of the billing system"""
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._init_ui()
        self._setup_connections()

    def _init_ui(self):
        """Initialize the UI"""
        # Load UI file
        uic.loadUi("config/BMS_Home_GUI.ui", self)

        # Set window properties
        aspect_ratio = 16 / 9
        min_height = 900
        min_width = int(min_height * aspect_ratio)
        self.setMinimumSize(min_width, min_height)
        
        # Set window title with user name
        user_name = User().get_name_designation()[0]
        self.setWindowTitle(f"BMS - {user_name}")
        
        # Set window icon
        self.setWindowIcon(QIcon("resources/icons/icon.ico"))

        # Initialize UI components
        self._init_menu_items()
        self._init_bill_table()
        self._init_labels()

        logging.info("Home GUI initialized")

    def _init_menu_items(self):
        """Initialize menu items based on user role"""
        if User().is_admin():
            self.menuSales.setEnabled(True)
            self.menuStock.setEnabled(True)
            self.New_Bill_Tab.setEnabled(True)
        else:
            self.menuSales.setEnabled(False)
            self.menuStock.setEnabled(False)
            self.New_Bill_Tab.setEnabled(True)

    def _init_bill_table(self):
        """Initialize the bill table"""
        self.Bill_Table.setColumnCount(len(BillTableColumn))
        self.Bill_Table.setHorizontalHeaderLabels([
            "ID", "Name", "Quantity", "Price", "Discount", "Total"
        ])
        self._set_column_widths()

    def _set_column_widths(self):
        """Set column widths for bill table"""
        widths = {
            BillTableColumn.ID: 100,
            BillTableColumn.NAME: 200,
            BillTableColumn.QUANTITY: 100,
            BillTableColumn.PRICE: 100,
            BillTableColumn.DISCOUNT: 100,
            BillTableColumn.TOTAL: 100
        }
        for col, width in widths.items():
            self.Bill_Table.setColumnWidth(col.value, width)

    def _init_labels(self):
        """Initialize labels with default values"""
        self.Total_Label.setText("Total: 0.00")
        self.Net_Discount_Label.setText("Discount: 0.00")
        self.Net_Total_Label.setText("Net Total: 0.00")

    def _setup_connections(self):
        """Setup signal connections"""
        self.Bill_Table.cellChanged.connect(self._on_cell_changed)
        self.Print_Button.clicked.connect(self._on_print_clicked)

    def _on_cell_changed(self, row: int, col: int):
        """Handle cell change in bill table"""
        self.controller.handle_cell_change(row, col)

    def _on_print_clicked(self):
        """Handle print button click"""
        self.controller.generate_bill()

    def get_text(self, row: int, col: int) -> str:
        """Get text from table cell"""
        item = self.Bill_Table.item(row, col)
        return item.text() if item else ""

    def set_row_data(self, row: int, data: dict):
        """Set data for entire row"""
        self.Bill_Table.setItem(row, BillTableColumn.ID.value, data['id'])
        self.Bill_Table.setItem(row, BillTableColumn.NAME.value, data['name'])
        self.Bill_Table.setItem(row, BillTableColumn.QUANTITY.value, "1")
        self.Bill_Table.setItem(row, BillTableColumn.PRICE.value, str(data['price']))
        self.Bill_Table.setItem(row, BillTableColumn.DISCOUNT.value, "0")
        self.Bill_Table.setItem(row, BillTableColumn.TOTAL.value, str(data['price']))

    def update_totals(self, total: float, discount: float):
        """Update total and discount labels"""
        self.Total_Label.setText(f"Total: {total:.2f}")
        self.Net_Discount_Label.setText(f"Discount: {discount:.2f}")
        self.Net_Total_Label.setText(f"Net Total: {total - discount:.2f}")

    def show_error(self, title: str, message: str):
        """Show error message box"""
        QMessageBox.critical(self, title, message)

    def show_success(self, title: str, message: str):
        """Show success message box"""
        QMessageBox.information(self, title, message)

    def clear_bill(self):
        """Clear the bill table"""
        self.Bill_Table.setRowCount(0)
        self.update_totals(0, 0)

    def closeEvent(self, event):
        """Handle window close event"""
        if User().is_logging_out():
            event.accept()
            return

        reply = QMessageBox.question(
            self, "Exit?", "Are you sure you want to quit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
