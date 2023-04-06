""" Tests for Database class """
from os import getenv
from datetime import date, datetime, timedelta
import sqlite3

from dotenv import load_dotenv
import pytest

import database
from my_db_context_manager import MyDatabaseContextManager

load_dotenv()
reminder_days = float(getenv("REMINDER"))
date_shifted = date.today() + timedelta(days=reminder_days)
table_name = "bokser"   # pylint: disable=invalid-name

records = [{"email": "for_test_only@gmail.com",
            "name": "Stefan Muller",
            "book_title": "Star Wars",
            "return_at": "2021-01-08"},
           {"email": "test@gmail.com",
            "name": "Martin Schmidt",
            "book_title": "Sherlock Holmes",
            "return_at": "2024-05-28"},
           {"email": "test2@onet.pl",
            "name": "Jesus Navas",
            "book_title": "Rainmaker",
            "return_at": "2020-03-16"},
           {"email": "for_test_only@gmail.com",
            "name": "Kylian Mbappe",
            "book_title": "Potop",
            "return_at": "2023-02-25"}
           ]

create_table_sql_query = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    name TEXT NOT NULL,
                    book_title TEXT NOT NULL,
                    return_at DATE NOT NULL
                    );
                    """


@pytest.fixture
def create_connection():
    """
    Fixture for create connection to database in memory (for testing
    purpose). Function create table and add rows to db.
    Returns Connection object.
    """
    connection = sqlite3.connect(":memory:")
    database.create_table(connection, table_name)
    database.add_row(connection, table_name, records)
    return connection


def test_check_if_all_row_was_added(create_connection):
    """
    Test counting all positions/rows in name column. It is checking if
    all rows was added to memory database
    """
    count_row_sql_query = f"""SELECT COUNT(name) FROM {table_name}"""
    with MyDatabaseContextManager(create_connection) as connector:
        counter = connector.cursor.execute(count_row_sql_query)
        result = counter.fetchone()[0]
    assert result == 4


def test_check_method_show_all_rows(create_connection):
    """
    Test checks if method show_all_rows display every row from table
    in database
    """
    with MyDatabaseContextManager(create_connection):
        result_db = database.show_all_rows(create_connection, table_name)
        expected_result = [
            (1, 'for_test_only@gmail.com', 'Stefan Muller', 'Star Wars',
             '2021-01-08'),
            (2, 'test@gmail.com', 'Martin Schmidt', 'Sherlock Holmes',
             '2024-05-28'),
            (3, 'test2@onet.pl', 'Jesus Navas', 'Rainmaker',
             '2020-03-16'),
            (4, 'for_test_only@gmail.com', 'Kylian Mbappe', 'Potop',
             '2023-02-25')
            ]

    assert result_db == expected_result


def test_delete_row(create_connection):
    """
    Test checks if method delete_row can remove row from table
    in database
    """
    with MyDatabaseContextManager(create_connection):
        database.delete_row(create_connection, table_name, "Martin Schmidt", "Sherlock Holmes")
        all_rows = database.show_all_rows(create_connection, table_name)
    result = []
    for element in all_rows:
        if "Martin Schmidt" in element:
            result.append(True)
    assert any(result) is False


def test_find_books_debtor(create_connection):
    """
    Test checks method show_who_didnt_back_book. It checks when people
    should return book (return_at column) and compare it with current
    timestamp. If date was exceed then should return these records
    """
    with MyDatabaseContextManager(create_connection):
        debtors = database.show_who_didnt_return_book(create_connection, table_name)
    debtor_book = (3, 'test2@onet.pl', 'Jesus Navas', 'Rainmaker',
                   '2020-03-16')
    assert debtor_book in debtors

records_with_shifted = [
           {"email": "test2@onet.pl",
            "name": "Jesus Navas",
            "book_title": "Rainmaker",
            "return_at": "2020-03-16"},
           {"email": "for_test_only@gmail.com",
            "name": "Kylian Mbappe",
            "book_title": "Potop",
            "return_at": date_shifted}
           ]

@pytest.fixture
def create_connection_for_reminder():
    """
    Fixture for create connection to database in memory (for testing
    purpose). Function create table and add rows to db (dedicated rows for
    checking sending email reminder).
    Returns Connection object.
    """
    connection = sqlite3.connect(":memory:")
    database.create_table(connection, table_name)
    database.add_row(connection, table_name, records_with_shifted)
    return connection


def test_show_reminder(create_connection_for_reminder):
    """
    Function check if email with reminder has been sent. Number of days
    to be reminded is set in .env file as "REMINDER" variable.
    In database in rows should be date when book deptor should get back
    book.
    ********************************************************************
    WARNING: this test failed in specific slot of time (0:00AM - 02:00PM
    in summer time and 0:00AM - 01:00PM (in winter time)
    ********************************************************************
    :param create_connection_for_reminder:
    :return:
    """
    with MyDatabaseContextManager(create_connection_for_reminder):
        data = database.show_rows_x_days_before_return(
            create_connection_for_reminder,
            table_name
            )
    return_date = data[0][4]
    diff = datetime.strptime(return_date, "%Y-%m-%d") - datetime.today()
    counted_reminder_days = diff.days + 1

    assert counted_reminder_days == reminder_days
