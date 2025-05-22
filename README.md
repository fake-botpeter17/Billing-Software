# Billing Management System

A comprehensive billing and inventory management system built with Python and PyQt6.

## Features

- User Authentication and Authorization
- Bill Generation and Management
- Stock Management
- Barcode Integration
- Printer Support
- Sales Analysis

## Project Structure

```
Billing-Software/
├── app/                           # Application code
│   ├── controllers/               # Business logic
│   ├── models/                    # Data models
│   ├── views/                     # GUI components
│   ├── utils/                     # Utilities
│   ├── observers/                 # Event observers
│   ├── api/                       # API integration
│   └── commands/                  # Command pattern
├── config/                        # Configuration
├── resources/                     # Resources
├── data/                          # Runtime data
└── user_registration/            # Registration module
```

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure database in `config/db_config.json`
4. Run `python main.py`

## Requirements

- Python 3.8+
- PostgreSQL 12+
- PyQt6
- Other dependencies listed in requirements.txt
