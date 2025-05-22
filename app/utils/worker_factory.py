"""
Worker Thread Factory Pattern Implementation
"""
from PyQt6.QtCore import QThread, pyqtSignal
import logging

class WorkerThread(QThread):
    """Base worker thread class"""
    error = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('BMS')

class StockUpdateWorker(WorkerThread):
    """Worker for stock updates"""
    updateStock = pyqtSignal(dict)
    
    def run(self):
        try:
            # Stock update logic here
            self.finished.emit()
        except Exception as e:
            self.logger.error(f"Stock update error: {e}")
            self.error.emit(str(e))

class BillGenerationWorker(WorkerThread):
    """Worker for bill generation"""
    billGenerated = pyqtSignal(dict)
    
    def run(self):
        try:
            # Bill generation logic here
            self.finished.emit()
        except Exception as e:
            self.logger.error(f"Bill generation error: {e}")
            self.error.emit(str(e))

class WorkerFactory:
    """Factory for creating worker threads"""
    
    @staticmethod
    def create_worker(worker_type: str) -> WorkerThread:
        """Create a worker thread based on type"""
        if worker_type == "stock_update":
            return StockUpdateWorker()
        elif worker_type == "bill_generation":
            return BillGenerationWorker()
        else:
            raise ValueError(f"Unknown worker type: {worker_type}")
