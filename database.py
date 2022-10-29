"""
DATABASE module
"""

import sqlite3
import logging

logging.basicConfig(format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    level=logging.INFO)


class Database:
    def __init__(self, name):
        self.name = name
        self.connection = self.create_connection_to_db()
        self.cursor = self.create_cursor_to_db()

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
        return self.connection.cursor()

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

    def add_row(self, table_name: str, records_to_added: list[dict]) -> None:
        """
        This method can add row to table in database. Please use it only
        once or every run this method, change records_to_added param to
        avoid duplicate rows
        :param table_name: str
        :param records_to_added: list[dict], example:
        records_to_added = [{"email": "for_test_only@gmail.com",
            "name": "Stefan Muller",
            "book_title": "Star Wars",
            "return_at": "2023-01-08"},
           {"email": "test@gmail.com",
           "name": "Martin Schmidt",
            "book_title": "Sherlock Holmes",
            "return_at": "2021-05-28"}
           ]
        :return: None
        """
        for element in range(len(records_to_added)):
            insert_sql_query = f"""
                INSERT INTO {table_name} (email, name, book_title, return_at) 
                VALUES (
                "{records_to_added[element]["email"]}", 
                "{records_to_added[element]["name"]}", 
                "{records_to_added[element]["book_title"]}", 
                "{records_to_added[element]["return_at"]}"
            )"""

            self.cursor.execute(insert_sql_query)
            self.connection.commit()
