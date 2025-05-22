"""
Stock Controller - Handles stock management operations
"""
import logging
from typing import Dict, List, Optional
from app.models.db_manager import DatabaseManager
from app.utils.worker_factory import WorkerFactory

class StockController:
    """Controller for stock operations"""
    def __init__(self):
        self.db = DatabaseManager()
        self.worker_factory = WorkerFactory()

    def get_stock(self) -> List[Dict]:
        """
        Get current stock information
        
        Returns:
            List of dictionaries containing stock items
        """
        conn = self.db.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, name, quantity, price, batch_number, 
                       expiry_date, category 
                FROM stock
                ORDER BY name
            """)
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
        except Exception as e:
            logging.error(f"Error fetching stock: {e}")
            return []
        finally:
            self.db.return_connection(conn)

    def update_stock(self, item_id: int, updates: Dict) -> bool:
        """
        Update stock item
        
        Args:
            item_id: ID of item to update
            updates: Dictionary containing fields to update
            
        Returns:
            bool: True if update successful, False otherwise
        """
        conn = self.db.get_connection()
        try:
            cur = conn.cursor()
            
            # Build update query
            set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
            query = f"UPDATE stock SET {set_clause} WHERE id = %s"
            
            # Execute update
            values = list(updates.values()) + [item_id]
            cur.execute(query, values)
            conn.commit()
            
            logging.info(f"Stock item {item_id} updated successfully")
            return True
            
        except Exception as e:
            conn.rollback()
            logging.error(f"Error updating stock item {item_id}: {e}")
            return False
        finally:
            self.db.return_connection(conn)

    def add_stock_item(self, item_data: Dict) -> Optional[int]:
        """
        Add new stock item
        
        Args:
            item_data: Dictionary containing item information
            
        Returns:
            int: ID of new item if successful, None otherwise
        """
        conn = self.db.get_connection()
        try:
            cur = conn.cursor()
            
            # Build insert query
            columns = ", ".join(item_data.keys())
            placeholders = ", ".join(["%s"] * len(item_data))
            query = f"INSERT INTO stock ({columns}) VALUES ({placeholders}) RETURNING id"
            
            # Execute insert
            cur.execute(query, list(item_data.values()))
            new_id = cur.fetchone()[0]
            conn.commit()
            
            logging.info(f"New stock item added with ID {new_id}")
            return new_id
            
        except Exception as e:
            conn.rollback()
            logging.error(f"Error adding stock item: {e}")
            return None
        finally:
            self.db.return_connection(conn)

    def delete_stock_item(self, item_id: int) -> bool:
        """
        Delete stock item
        
        Args:
            item_id: ID of item to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        conn = self.db.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM stock WHERE id = %s", [item_id])
            conn.commit()
            
            logging.info(f"Stock item {item_id} deleted successfully")
            return True
            
        except Exception as e:
            conn.rollback()
            logging.error(f"Error deleting stock item {item_id}: {e}")
            return False
        finally:
            self.db.return_connection(conn)

    def update_stock_async(self, updates: List[Dict]) -> None:
        """
        Update multiple stock items asynchronously
        
        Args:
            updates: List of dictionaries containing update information
        """
        worker = self.worker_factory.create_worker("stock_update")
        worker.updateStock.connect(lambda: self._handle_stock_update(updates))
        worker.error.connect(self._handle_stock_error)
        worker.start()

    def _handle_stock_update(self, updates: List[Dict]) -> None:
        """Handle batch stock update"""
        conn = self.db.get_connection()
        try:
            cur = conn.cursor()
            for update in updates:
                item_id = update.pop('id')
                set_clause = ", ".join([f"{k} = %s" for k in update.keys()])
                query = f"UPDATE stock SET {set_clause} WHERE id = %s"
                values = list(update.values()) + [item_id]
                cur.execute(query, values)
            
            conn.commit()
            logging.info("Batch stock update completed successfully")
            
        except Exception as e:
            conn.rollback()
            logging.error(f"Error in batch stock update: {e}")
            raise
        finally:
            self.db.return_connection(conn)

    def _handle_stock_error(self, error: str) -> None:
        """Handle stock update error"""
        logging.error(f"Stock update error: {error}")
        # Implement error handling logic (e.g., notify user, retry operation)
