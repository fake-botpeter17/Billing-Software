"""
User Model - Handles user-related data and operations
"""
from typing import Tuple, Optional
import logging
from .db_manager import DatabaseManager

class User:
    """User class for managing user operations"""
    _instance = None
    _name: str = ""
    _designation: str = ""
    _uid: str = ""
    _logging_out: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def update(cls, uid: str, **kwargs) -> None:
        """Update user information"""
        cls._name = kwargs.get("name", "")
        cls._designation = kwargs.get("designation", "")
        cls._uid = uid
        logging.info(f"User updated: {uid}")

    @classmethod
    def get_name_designation(cls) -> Tuple[str, str]:
        """Get user's name and designation"""
        return cls._name, cls._designation

    @classmethod
    def is_admin(cls) -> bool:
        """Check if user is admin"""
        return cls._designation.lower() == "admin"

    @classmethod
    def is_logging_out(cls) -> bool:
        """Check if user is logging out"""
        return cls._logging_out

    @classmethod
    def toggle_logging_out(cls) -> None:
        """Toggle logging out status"""
        cls._logging_out = True
        cls.reset_user()

    @classmethod
    def reset_user(cls) -> None:
        """Reset user information"""
        cls._name = ""
        cls._designation = ""
        cls._uid = ""
        cls._logging_out = False
        logging.info("User reset")
