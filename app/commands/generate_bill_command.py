"""
Generate Bill Command - Implements Command pattern for bill generation
"""
from typing import Protocol, Dict
import logging
from app.models.bill import Bill
from app.controllers.printer_controller import PrinterController

class Command(Protocol):
    """Protocol for commands"""
    def execute(self) -> bool:
        """Execute the command"""
        pass

    def undo(self) -> bool:
        """Undo the command"""
        pass

class GenerateBillCommand:
    """Command for bill generation"""
    def __init__(self, bill_data: Dict):
        self.bill_data = bill_data
        self.bill_model = Bill()
        self.printer_controller = PrinterController()
        self.bill_number = None

    def execute(self) -> bool:
        """
        Execute bill generation
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Store bill number for potential undo
            self.bill_number = self.bill_data['bill_no']
            
            # Save bill to database
            if not self._save_bill():
                return False
                
            # Print bill
            if not self.printer_controller.print_bill(self.bill_data):
                return False
                
            # Update stock
            if not self._update_stock():
                return False
                
            # Prepare for next bill
            self.bill_model.next_bill_prep()
            
            logging.info(f"Bill {self.bill_number} generated successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error generating bill: {e}")
            return False

    def undo(self) -> bool:
        """
        Undo bill generation
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.bill_number:
            return False
            
        try:
            # Reverse stock updates
            if not self._reverse_stock_updates():
                return False
                
            # Delete bill from database
            if not self._delete_bill():
                return False
                
            logging.info(f"Bill {self.bill_number} generation undone")
            return True
            
        except Exception as e:
            logging.error(f"Error undoing bill generation: {e}")
            return False

    def _save_bill(self) -> bool:
        """Save bill to database"""
        try:
            # Implementation for saving bill to database
            return True
        except Exception as e:
            logging.error(f"Error saving bill: {e}")
            return False

    def _update_stock(self) -> bool:
        """Update stock quantities"""
        try:
            # Implementation for updating stock
            return True
        except Exception as e:
            logging.error(f"Error updating stock: {e}")
            return False

    def _reverse_stock_updates(self) -> bool:
        """Reverse stock updates"""
        try:
            # Implementation for reversing stock updates
            return True
        except Exception as e:
            logging.error(f"Error reversing stock updates: {e}")
            return False

    def _delete_bill(self) -> bool:
        """Delete bill from database"""
        try:
            # Implementation for deleting bill
            return True
        except Exception as e:
            logging.error(f"Error deleting bill: {e}")
            return False

# Usage example:
"""
# Create and execute command
bill_data = {
    'bill_no': 12345,
    'items': [...],
    'total': 100.00,
    'discount': 10.00,
    'net_total': 90.00
}
command = GenerateBillCommand(bill_data)

# Execute command
if command.execute():
    print("Bill generated successfully")
else:
    print("Bill generation failed")

# Undo if needed
if command.undo():
    print("Bill generation undone")
else:
    print("Failed to undo bill generation")
"""
