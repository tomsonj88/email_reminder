"""
DATABASE module
"""
from os import getenv

import logging

logging.basicConfig(format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    level=logging.INFO)

logger_sql = logging.getLogger("SQL_query")
logger_sql.setLevel("INFO")


def create_table(connection, table_name: str) -> None:
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
    cursor = connection.cursor()
    cursor.execute(create_table_sql_query)
    logger_sql.info(create_table_sql_query)
    logging.info(f"Table {table_name} was created successfully")


def add_row(connection, table_name: str, records_to_added: list[dict]) -> None:
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
    cursor = connection.cursor()
    for element in range(len(records_to_added)):
        insert_sql_query = f"""
            INSERT INTO {table_name} (email, name, book_title, return_at)
            VALUES (
            "{records_to_added[element]["email"]}",
            "{records_to_added[element]["name"]}",
            "{records_to_added[element]["book_title"]}",
            "{records_to_added[element]["return_at"]}"
        )"""
        cursor.execute(insert_sql_query)
        logger_sql.info(insert_sql_query)


def delete_row(connection, table_name: str, name: str, book_title: str) -> None:
    """
    Method can delete rows, when table contain specified params: name
    and book_title.
    :param table_name: str
    :param name: str
    :param book_title: str
    :return: None
    """
    delete_sql_query = f"""DELETE FROM {table_name}
        WHERE name="{name}" AND book_title="{book_title}"
    """
    cursor = connection.cursor()
    cursor.execute(delete_sql_query)
    logger_sql.info(delete_sql_query)


def show_all_rows(connection, table_name: str) -> list:
    """
    Show all rows in table specified in params
    :param table_name:
    :return: list
    """
    show_rows_sql_query = f"""SELECT * from {table_name}"""
    cursor = connection.cursor()
    cursor.execute(show_rows_sql_query)
    logger_sql.info(show_rows_sql_query)
    return cursor.fetchall()


def show_who_didnt_return_book(connection, table_name: str) -> list:
    """
    Show rows  with exceeded deadline for book return. If current
    date is later than "return_at" field in database, then these rows
    will be display and return.
    :param table_name: str
    :return: list
    """
    show_rows_sql_query = f"""SELECT * FROM {table_name}
    WHERE return_at < current_timestamp
    """
    cursor = connection.cursor()
    cursor.execute(show_rows_sql_query)
    result = cursor.fetchall()
    logger_sql.info(show_rows_sql_query)
    return result


def show_rows_x_days_before_return(connection, table_name):
    cursor = connection.cursor()
    remind_days_before = getenv("REMINDER")
    show_rows_for_remind_sql_query = f"""SELECT *,
    DATE(return_at, "-{remind_days_before} day") as diff
    FROM {table_name} WHERE diff = DATE()"""
    cursor.execute(show_rows_for_remind_sql_query)
    logger_sql.info(show_rows_for_remind_sql_query)
    result = cursor.fetchall()
    return result
