"""
Bill Model - Handles bill-related data and operations
"""
from datetime import datetime
from typing import Dict, Generator, Optional
import logging
from .db_manager import DatabaseManager
from app.utils.logger import Logger

class Bill:
    """Bill class for managing bill operations"""
    _instance = None
    _bill_no_gen: Generator
    _bill_no: int = 0
    _items: Dict = {}
    _cart: Dict = {}  # {id:row}
    _row_lookup: Dict = {}  # {row:id}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def get_items() -> Dict:
        """Get all available items from stock"""
        db = DatabaseManager()
        conn = db.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM stock")
            items = cur.fetchall()
            return {item[0]: dict(zip(['id', 'name', 'price', 'quantity'], item)) 
                   for item in items}
        except Exception as e:
            logging.error(f"Error fetching items: {e}")
            return {}
        finally:
            db.return_connection(conn)

    @classmethod
    def contains(cls, item_id: int) -> bool:
        """Check if item is in cart"""
        return item_id in cls._cart

    @classmethod
    def get_cart_items(cls):
        """Get all items in cart"""
        return cls._cart.keys()

    @classmethod
    def get_cart(cls) -> Dict:
        """Get entire cart"""
        return cls._cart

    @classmethod
    def get_item(cls, item_id: int) -> Optional[Dict]:
        """Get specific item details"""
        return cls._items.get(item_id)

    @classmethod
    def get_row_number(cls, item_id: int) -> Optional[int]:
        """Get row number for item"""
        return cls._cart.get(item_id)

    @classmethod
    def is_duplicate_row(cls, row_number: int) -> bool:
        """Check if row already exists"""
        return row_number in cls._row_lookup

    @classmethod
    def add_item(cls, item_id: int, row: int) -> None:
        """Add item to cart"""
        cls._cart[item_id] = row
        cls._row_lookup[row] = item_id

    @classmethod
    def remove_row_item(cls, row_number: int) -> None:
        """Remove item from cart by row number"""
        item = cls._row_lookup.get(row_number)
        if item in cls._cart:
            del cls._cart[item]
        cls._row_lookup.pop(row_number, None)

    @classmethod
    def is_empty(cls) -> bool:
        """Check if cart is empty"""
        return len(cls._cart) == 0

    @staticmethod
    def get_time() -> str:
        """Get current time"""
        return datetime.now().strftime("%H:%M:%S")

    @classmethod
    def next_bill_prep(cls) -> None:
        """Prepare for next bill"""
        cls._cart.clear()
        cls._row_lookup.clear()
        cls._increment_bill_no()

    @classmethod
    def _increment_bill_no(cls) -> None:
        """Increment bill number"""
        cls._bill_no = next(cls._bill_no_gen)

    @classmethod
    def get_bill_no(cls) -> int:
        """Get current bill number"""
        return cls._bill_no

    @staticmethod
    def _bill_number(testing: bool = False) -> Generator:
        """Generate bill numbers"""
        db = DatabaseManager()
        conn = db.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT MAX(bill_no) FROM bills")
            latest_bill = cur.fetchone()[0] or 10000
            while True:
                yield latest_bill + 1
                latest_bill += 1
        finally:
            db.return_connection(conn)

    @classmethod
    def init(cls) -> None:
        """Initialize bill system"""
        cls._bill_no_gen = cls._bill_number()
        cls._bill_no = next(cls._bill_no_gen)
        cls._items = cls.get_items()
