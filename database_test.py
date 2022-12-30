""" Tests for Database class """
from os import getenv
from datetime import date, datetime, timedelta

from dotenv import load_dotenv

from database import Database

load_dotenv()
reminder_days = float(getenv("REMINDER"))
date_shifted = date.today() + timedelta(days=reminder_days)
table_name = "books"
database = Database(":memory:")
database.create_table(table_name)
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
            "return_at": date_shifted}
           ]
database.add_row(table_name, records)


def test_check_if_all_row_was_added():
    """
    Test counting all positions/rows in name column. It is checking if
    all rows was added to memory database
    """
    count_row_sql_query = f"""SELECT COUNT(name) FROM {table_name}"""
    counter = database.cursor.execute(count_row_sql_query)
    result = counter.fetchone()[0]
    assert result == 4


def test_check_method_show_all_rows():
    """
    Test checks if method show_all_rows display every row from table
    in database
    """
    show_all_records_sql_query = f"""SELECT * FROM {table_name}"""
    all_rows = database.cursor.execute(show_all_records_sql_query)
    result = all_rows.fetchall()
    assert database.show_all_rows(table_name) == result


def test_delete_row():
    """
    Test checks if method delete_row can remove row from table
    in database
    """
    database.delete_row(table_name, "Martin Schmidt", "Sherlock Holmes")
    all_rows = database.show_all_rows(table_name)
    result = []
    for element in all_rows:
        if "Martin Schmidt" in element:
            result.append(True)
    assert any(result) is False


def test_find_books_debtor():
    """
    Test checks method show_who_didnt_back_book. It checks when people
    should return book (return_at column) and compare it with current
    timestamp. If date was exceed then should return these records
    """
    debtors = database.show_who_didnt_return_book(table_name)
    debtor_book = (3, 'test2@onet.pl', 'Jesus Navas', 'Rainmaker',
                   '2020-03-16')
    assert debtor_book in debtors


def test_show_reminder():
    reminder_days = float(getenv("REMINDER"))
    data = database.show_rows_x_days_before_return("books")
    return_date = data[0][4]
    diff = datetime.strptime(return_date, "%Y-%m-%d") - datetime.today()
    counted_reminder_days = diff.days + 1
    assert counted_reminder_days == reminder_days
