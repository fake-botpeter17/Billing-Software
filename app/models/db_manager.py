"""
Database Manager Singleton for PostgreSQL connections
"""
import json
import logging
import psycopg2
from psycopg2.pool import SimpleConnectionPool

class DatabaseManager:
    _instance = None
    _pool = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_connection()
        return cls._instance
    
    def _initialize_connection(self):
        try:
            # Load database configuration
            with open('config/db_config.json', 'r') as f:
                config = json.load(f)
            
            # Create connection pool
            self._pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=config['host'],
                database=config['database'],
                user=config['user'],
                password=config['password'],
                port=config['port']
            )
            logging.info("Database connection pool initialized")
            
        except Exception as e:
            logging.error(f"Failed to initialize database connection: {e}")
            raise
    
    def get_connection(self):
        """Get a connection from the pool"""
        return self._pool.getconn()
    
    def return_connection(self, conn):
        """Return a connection to the pool"""
        self._pool.putconn(conn)
    
    def close_all(self):
        """Close all connections in the pool"""
        if self._pool:
            self._pool.closeall()
            logging.info("All database connections closed")
