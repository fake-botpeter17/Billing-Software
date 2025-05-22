"""
Stock Observer - Implements Observer pattern for stock updates
"""
from typing import Protocol, Dict
import logging

class StockObserver(Protocol):
    """Protocol for stock observers"""
    def update(self, item_id: int, changes: Dict) -> None:
        """Update method that observers must implement"""
        pass

class StockUpdateNotifier:
    """Notifier for stock updates"""
    _observers: list = []
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def attach(cls, observer: StockObserver) -> None:
        """
        Attach an observer
        
        Args:
            observer: Observer to attach
        """
        if observer not in cls._observers:
            cls._observers.append(observer)
            logging.info(f"Observer {observer.__class__.__name__} attached")

    @classmethod
    def detach(cls, observer: StockObserver) -> None:
        """
        Detach an observer
        
        Args:
            observer: Observer to detach
        """
        try:
            cls._observers.remove(observer)
            logging.info(f"Observer {observer.__class__.__name__} detached")
        except ValueError:
            logging.warning(f"Observer {observer.__class__.__name__} not found")

    @classmethod
    def notify(cls, item_id: int, changes: Dict) -> None:
        """
        Notify all observers of stock update
        
        Args:
            item_id: ID of updated item
            changes: Dictionary of changes made
        """
        for observer in cls._observers:
            try:
                observer.update(item_id, changes)
            except Exception as e:
                logging.error(f"Error notifying observer {observer.__class__.__name__}: {e}")

class BillTableObserver:
    """Observer for bill table updates"""
    def update(self, item_id: int, changes: Dict) -> None:
        """
        Update bill table when stock changes
        
        Args:
            item_id: ID of updated item
            changes: Dictionary of changes made
        """
        try:
            # Update relevant rows in bill table
            logging.info(f"Updating bill table for item {item_id}")
            # Implement specific update logic here
        except Exception as e:
            logging.error(f"Error updating bill table: {e}")

class StockDisplayObserver:
    """Observer for stock display updates"""
    def update(self, item_id: int, changes: Dict) -> None:
        """
        Update stock display when stock changes
        
        Args:
            item_id: ID of updated item
            changes: Dictionary of changes made
        """
        try:
            # Update stock display
            logging.info(f"Updating stock display for item {item_id}")
            # Implement specific update logic here
        except Exception as e:
            logging.error(f"Error updating stock display: {e}")

# Usage example:
"""
# Create notifier and observers
notifier = StockUpdateNotifier()
bill_observer = BillTableObserver()
display_observer = StockDisplayObserver()

# Attach observers
notifier.attach(bill_observer)
notifier.attach(display_observer)

# When stock updates occur
notifier.notify(item_id=123, changes={'quantity': 10, 'price': 99.99})
"""
