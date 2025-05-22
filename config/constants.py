"""
Global constants for the Billing Management System
"""
from enum import Enum, auto
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
RESOURCES_DIR = BASE_DIR / "resources"
DATA_DIR = BASE_DIR / "data"
BILLS_DIR = DATA_DIR / "Bills"
BARCODES_DIR = DATA_DIR / "Barcodes"

# Application constants
APP_NAME = "Billing Management System"
APP_VERSION = "2.0.0"
COMPANY_NAME = "Fashion Paradise"

class WindowName(Enum):
    """Enum for window names"""
    MAIN = auto()
    LOGIN = auto()
    REGISTRATION = auto()
    STOCK_UPDATE = auto()
    BILL_GENERATION = auto()

class BillTableColumn(Enum):
    """Enum for bill table columns"""
    ID = 0
    NAME = 1
    QUANTITY = 2
    PRICE = 3
    DISCOUNT = 4
    TOTAL = 5

# Database table names
class Tables(Enum):
    """Enum for database table names"""
    USERS = "users"
    BILLS = "bills"
    STOCK = "stock"
    TRANSACTIONS = "transactions"

# API endpoints
API_BASE_URL = "http://localhost:8000"
API_ENDPOINTS = {
    "authenticate": "/authenticate",
    "stock": "/stock",
    "bills": "/bills",
    "users": "/users"
}
