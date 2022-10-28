"""
DATABASE module
"""

import sqlite3
import logging

logging.basicConfig(format="%(asctime)s %(name)s %(levelname)s %(message)s", level=logging.INFO)


class Database:
    def __init__(self, name):
        self.name = name
        self.cursor = self.create_cursor_to_db()
        self.connection = self.create_connection_to_db()

    def __str__(self):
        # ToDo: change this __str__ class
        return f"Database: {self.name}.db"
