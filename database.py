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

    def create_connection_to_db(self) -> sqlite3.Connection:
        """
        Create connection to database
        :return: sqlite3.Connection
        """
        with sqlite3.connect(f"{self.name}.db") as connection:
            return connection

    def create_cursor_to_db(self) -> sqlite3.Cursor:
        """
        Create database cursor in order to execute SQL statements
        and fetch results from SQL queries
        :return: sqlite3.Cursor
        """
        return self.create_connection_to_db().cursor()

    def create_table(self, table_name: str) -> None:
        """
        Method to create table with specified columns: id, email, name
        book_title, return_at. Command to create table is in SQL.
        :param table_name:
        :return: None
        """
        create_table_sql_query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT NOT NULL,
                            name TEXT NOT NULL,
                            book_title TEXT NOT NULL,
                            return_at DATE NOT NULL
                            );
                            """
        self.cursor.execute(create_table_sql_query)
        logging.info(create_table_sql_query)
        logging.info(f"Table {table_name} was created successfully")


db = Database("baza")
db.create_table("ksiazki")
