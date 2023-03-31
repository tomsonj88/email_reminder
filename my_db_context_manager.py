"""
Module for database context manager
"""
class MyDatabaseContextManager:
    """
    Context manager for connection to database
    """
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        if isinstance(exc_val, Exception):
            self.connection.rollback()
        else:
            self.connection.close()
