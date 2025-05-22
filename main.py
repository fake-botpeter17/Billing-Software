#!/usr/bin/env python3
"""
Billing Management System - Main Entry Point
"""
import sys
import logging
from app.utils.logger import setup_logger
from app.controllers.billing_controller import BillingController
from PyQt6.QtWidgets import QApplication

def main():
    # Setup logging
    setup_logger()
    logging.info("Starting Billing Management System")
    
    # Initialize Qt Application
    app = QApplication(sys.argv)
    
    # Initialize main controller
    controller = BillingController()
    controller.start()
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
