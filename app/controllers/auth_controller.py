"""
Authentication Controller - Handles user authentication and authorization
"""
import logging
from typing import Optional, Dict
import json
from urllib.request import Request, urlopen
from app.models.user import User
from app.models.bill import Bill
from config.constants import API_BASE_URL, API_ENDPOINTS

class AuthController:
    """Controller for authentication operations"""
    def __init__(self):
        self.user_model = User()
        self.api_base = API_BASE_URL

    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate user with given credentials
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            bool: True if authentication successful, False otherwise
        """
        logging.info(f"Authentication attempt for username='{username}'")
        
        try:
            # Build authentication URL
            auth_url = f"{self.api_base}{API_ENDPOINTS['authenticate']}/{username}/{password}"
            
            # Make authentication request
            req = Request(auth_url)
            with urlopen(req) as response:
                result = json.loads(response.read().decode())

            if result:
                # Update user model with returned data
                self.user_model.update(uid=username, **result)
                logging.info(f"Authentication successful for username='{username}' (admin={self.user_model.is_admin()})")
                
                # Initialize billing system
                Bill().init()
                return True
            else:
                logging.warning(f"Authentication failed for username='{username}' (wrong credentials)")
                return False

        except Exception as e:
            logging.error(f"Authentication error for username='{username}': {e}", exc_info=True)
            raise

    def logout(self) -> None:
        """
        Log out current user
        """
        self.user_model.toggle_logging_out()
        logging.info("User logged out successfully")

    def is_admin(self) -> bool:
        """
        Check if current user is admin
        
        Returns:
            bool: True if user is admin, False otherwise
        """
        return self.user_model.is_admin()

    def get_current_user(self) -> Optional[Dict[str, str]]:
        """
        Get current user information
        
        Returns:
            Dict containing user information or None if no user is logged in
        """
        name, designation = self.user_model.get_name_designation()
        if not name:
            return None
            
        return {
            "name": name,
            "designation": designation
        }
